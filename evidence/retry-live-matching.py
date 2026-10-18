"""Retry failed source/model calls only; retain the first run as immutable evidence."""

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

from tomi_ai_hermes.application.retrieval import Pipeline
from tomi_ai_hermes.config import Config
from tomi_ai_hermes.domain.evidence import plain_ocr
from tomi_ai_hermes.infrastructure.core import CoreClient
from tomi_ai_hermes.infrastructure.store import EvidenceStore
from tomi_ai_hermes.infrastructure.wikipedia import WikipediaClient


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


config = Config.from_env()
store = EvidenceStore.from_config(config)
base = Path("evidence/live-nemotron-matching-20261018T1742Z")
prior = json.loads((base / "progress.json").read_text())
out = Path("evidence/live-nemotron-matching-retry-20261018T1800Z")
out.mkdir(exist_ok=False)
core = CoreClient(config)
wiki = WikipediaClient(config)
failures = []
for label, client in [("core", core), ("wikipedia", wiki)]:
    original = client.request

    def request(*args, _original=original, _label=label, **kwargs):
        try:
            return _original(*args, **kwargs)
        except Exception as error:
            chain = []
            current = error
            while current is not None and len(chain) < 8:
                chain.append({"type": type(current).__name__, "errno": getattr(current, "errno", None)})
                current = current.__cause__ or current.__context__
            failures.append(
                {
                    "at": datetime.now(UTC).isoformat(),
                    "dependency": _label,
                    "path": args[1] if len(args) > 1 else None,
                    "chain": chain,
                }
            )
            save(out / "transport-diagnostics.json", failures)
            raise

    client.request = request
pipeline = Pipeline(config, core, wiki, store)
report = {
    "started_at": datetime.now(UTC).isoformat(),
    "baseline": str(base / "progress.json"),
    "results": [],
    "query_overrides": {"403": "philology Chaldean Ethiopian", "1032": "heart blood physiology"},
    "query_override_reason": "Assistant derived narrow search terms from legible original OCR after misspelled/abbreviated headings found no articles. Raw source text unchanged.",
}
save(out / "progress.json", report)
for previous in prior["results"]:
    if previous["status"] != "blocked":
        continue
    page_id = previous["page_id"]
    row = previous["row_index"]
    doc = store.get(page_id)
    result_row = {
        "page_id": page_id,
        "row_index": row,
        "original_status": previous["status"],
        "original_blockers": previous.get("blockers", []),
        "original_receipt_sha256": previous.get("receipt_sha256"),
        "human_review": "pending",
    }
    text = plain_ocr(doc.text).strip()
    if not text:
        result_row.update(
            status="nontext_blank_leaf",
            candidate_titles=[],
            reason="Original image visually reviewed as blank; normalized Parse response empty. No substitute text or inference.",
        )
    else:
        query = report["query_overrides"].get(str(row), previous["query"])
        result = pipeline.retrieve(query, "en", page_id, 3, require_semantic=True)
        p = out / f"page-{row}.json"
        save(p, result)
        result_row.update(
            status=result["status"],
            query=query,
            receipt_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
            receipt_path=str(p),
            candidates=[
                {
                    "document_id": c["document_id"],
                    "title": c["title"],
                    "score": c["score"],
                    "score_type": c["score_type"],
                }
                for c in result["candidates"]
            ],
            blockers=result["blockers"],
        )
    report["results"].append(result_row)
    save(out / "progress.json", report)
    print(
        json.dumps({"row": row, "status": result_row["status"], "retried": len(report["results"])}),
        flush=True,
    )
report["completed_at"] = datetime.now(UTC).isoformat()
report["counts"] = store.counts()
save(out / "progress.json", report)
