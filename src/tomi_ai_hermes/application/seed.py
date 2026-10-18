"""Portable public-source seed: preserve exact documents and original parser receipts."""

import json
from pathlib import Path

from tomi_ai_hermes.domain.evidence import Document, EvidenceError, sha256


def export_seed(store, data_dir: Path, output: Path) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    documents = store.all()
    receipts = [json.loads(path.read_text()) for path in sorted((data_dir / "parse-receipts").glob("*.json"))]
    payloads = {
        "documents.jsonl": "".join(json.dumps(doc.to_dict(), ensure_ascii=False) + "\n" for doc in documents),
        "parse-receipts.jsonl": "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in receipts),
    }
    manifest = {
        "schema_version": 1,
        "files": {},
        "counts": store.counts(),
        "vectors_included": False,
        "attribution": {
            "britannica": "CC0-1.0; National Library of Scotland",
            "wikipedia": "CC-BY-SA-4.0; Wikipedia contributors; original revision links in each document",
        },
    }
    for name, content in payloads.items():
        (output / name).write_text(content)
        manifest["files"][name] = sha256(content)
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return manifest


def import_seed(store, directory: Path) -> int:
    manifest_path = directory / "manifest.json"
    if not manifest_path.exists() or store.counts()["documents"]:
        return 0
    manifest = json.loads(manifest_path.read_text())
    contents = {}
    for filename in ("documents.jsonl", "parse-receipts.jsonl"):
        content = (directory / filename).read_text()
        if sha256(content) != manifest["files"][filename]:
            raise EvidenceError("Bundled source seed checksum differs")
        contents[filename] = [json.loads(line) for line in content.splitlines() if line]
    receipts = {sha256(json.dumps(receipt, sort_keys=True)) for receipt in contents["parse-receipts.jsonl"]}
    documents = [Document(**row) for row in contents["documents.jsonl"]]
    for document in documents:
        document.validate()
        if document.corpus == "britannica" and document.parser_receipt_sha256 not in receipts:
            raise EvidenceError("Bundled historical document lacks its parser receipt")
    store.save_many(documents)
    return len(documents)
