"""Reproducible 100-page sampling and auditable Parse ingestion."""

import json
import random
from datetime import UTC, datetime
from pathlib import Path

import pyarrow.parquet as pq

from tomi_ai_hermes.config import Config
from tomi_ai_hermes.domain.evidence import DependencyUnavailable, Document, EvidenceError, sha256


def read_manifest(path: Path) -> dict:
    manifest = json.loads(path.read_text())
    pages = manifest["pages"]
    expected = sorted(
        random.Random(manifest["selection"]["seed"]).sample(range(manifest["source_rows"]), 100)
    )
    if len(pages) != 100 or [p["row_index"] for p in pages] != expected:
        raise EvidenceError("The 100-page selection does not reproduce from the declared seed")
    if len({p["page_id"] for p in pages}) != 100:
        raise EvidenceError("Historical manifest contains duplicate page IDs")
    return manifest


def extract_pages(config: Config, parquet: Path) -> dict:
    manifest = read_manifest(config.manifest_path)
    with parquet.open("rb") as stream:
        import hashlib

        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    if digest != manifest["source_file_sha256"]:
        raise EvidenceError("Historical Parquet checksum differs from pinned manifest")
    table = pq.read_table(parquet)
    output = config.data_dir / "images"
    output.mkdir(parents=True, exist_ok=True)
    receipts = []
    for page in manifest["pages"]:
        row = table.slice(page["row_index"], 1).to_pylist()[0]
        image = row["image"]["bytes"]
        if sha256(image) != page["image_sha256"]:
            raise EvidenceError("Historical page image checksum differs")
        (output / page["filename"]).write_bytes(image)
        receipts.append({"page_id": page["page_id"], "image_sha256": sha256(image), "bytes": len(image)})
    return {
        "status": "verified",
        "pages": receipts,
        "manifest_sha256": sha256(config.manifest_path.read_bytes()),
    }


def ingest_pages(config: Config, core, store, limit: int = 100) -> dict:
    manifest = read_manifest(config.manifest_path)
    results = []
    receipts_dir = config.data_dir / "parse-receipts"
    receipts_dir.mkdir(parents=True, exist_ok=True)
    for page in manifest["pages"][:limit]:
        if store.get(page["page_id"]):
            results.append({"page_id": page["page_id"], "status": "already_parsed"})
            continue
        try:
            document, _receipt = parse_page(config, manifest, page, core)
            store.save(document)

            results.append(
                {"page_id": page["page_id"], "status": "parsed", "text_sha256": document.text_sha256}
            )
        except (EvidenceError, RuntimeError, OSError) as error:
            results.append({"page_id": page["page_id"], "status": "blocked", "reason": str(error)})
            if isinstance(error, DependencyUnavailable):
                break
    return {"attempted": len(results), "results": results}


def parse_page(config: Config, manifest: dict, page: dict, core) -> tuple[Document, dict]:
    image = (config.data_dir / "images" / page["filename"]).read_bytes()
    if sha256(image) != page["image_sha256"]:
        raise EvidenceError("Page image checksum differs before parsing")
    response = core.parse(image)
    receipt = {
        "image_sha256": sha256(image),
        "gateway_model_alias": config.parse_model,
        "response": response,
        "received_at": datetime.now(UTC).isoformat(),
    }
    directory = config.data_dir / "parse-receipts"
    directory.mkdir(parents=True, exist_ok=True)
    (
        directory
        / (str(page["row_index"]) + "-" + sha256(json.dumps(receipt, sort_keys=True))[:12] + ".json")
    ).write_text(json.dumps(receipt, ensure_ascii=False))
    try:
        choice = response["choices"][0]
        text = choice["message"]["content"]
    except KeyError, IndexError, TypeError:
        raise EvidenceError("Parse response has no text") from None
    if choice.get("finish_reason") == "length":
        raise EvidenceError("Parse response truncated at model token limit")
    document = Document(
        document_id=page["page_id"],
        title=f"Britannica page {page['row_index']}",
        corpus="britannica",
        text=text,
        source_url=manifest["source_url"],
        revision_id=manifest["revision"],
        text_sha256=sha256(text),
        dataset_revision=manifest["revision"],
        license="CC0-1.0; National Library of Scotland",
        acquired_at=receipt["received_at"],
        parser_receipt_sha256=sha256(json.dumps(receipt, sort_keys=True)),
    )
    document.validate()
    return document, receipt
