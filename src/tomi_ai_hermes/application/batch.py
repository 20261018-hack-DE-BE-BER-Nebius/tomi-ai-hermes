"""Account for every selected physical page, including covers and unavailable model stages."""

from datetime import UTC, datetime

from tomi_ai_hermes.application.ingest import read_manifest
from tomi_ai_hermes.application.retrieval import Pipeline
from tomi_ai_hermes.domain.evidence import plain_ocr
from tomi_ai_hermes.infrastructure.core import CoreClient
from tomi_ai_hermes.infrastructure.wikipedia import WikipediaClient


def match_sample(config, store) -> dict:
    manifest = read_manifest(config.manifest_path)
    pipeline = Pipeline(config, CoreClient(config), WikipediaClient(config), store)
    rows, unavailable = [], None
    for page in manifest["pages"]:
        document = store.get(page["page_id"])
        row = {
            "page_id": page["page_id"],
            "row_index": page["row_index"],
            "match_status": "not_run",
            "accepted_article_ids": [],
            "review_state": "pending",
        }
        if document is None:
            row.update(
                match_status="unreadable_or_nontext",
                reason="No accepted OCR document; inspect parser receipts and page review",
            )
        elif unavailable:
            row["reason"] = unavailable
        else:
            query = plain_ocr(document.text).strip().split("\n")[0][:256]
            result = pipeline.retrieve(query, "en", document.document_id, 3, require_semantic=True)
            row.update(match_status=result["status"], result=result)
            if result["status"] == "blocked" and any("v1/embeddings" in b for b in result["blockers"]):
                unavailable = "Embedding gateway unavailable; remaining matching calls were not made"
        rows.append(row)
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "sample_size": len(rows),
        "pages": rows,
        "all_matches_reviewed": False,
        "selection": manifest["selection"],
    }
