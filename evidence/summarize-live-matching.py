"""Merge immutable attempts into an explicit100-page outcome ledger, without accuracy claims."""

import csv
import hashlib
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

root = Path.cwd()
baseline_dir = Path("evidence/live-nemotron-matching-20261018T1742Z")
retry_dir = Path("evidence/live-nemotron-matching-retry-20261018T1800Z")
entry_dir = Path("evidence/live-nemotron-matching-entry-retry")
baseline = json.loads((baseline_dir / "progress.json").read_text())
retry = json.loads((retry_dir / "progress.json").read_text())
entry = json.loads((entry_dir / "progress.json").read_text())
classification = json.loads(Path("evidence/page-content-classification.json").read_text())
classes = {r["row_index"]: r["classification"] for r in classification["pages"]}
latest = {r["row_index"]: (dict(r), baseline_dir) for r in baseline["results"]}
for group, directory in [(retry, retry_dir), (entry, entry_dir)]:
    for row in group["results"]:
        latest[row["row_index"]] = (dict(row), directory)
rows = []
for source in baseline["results"]:
    index = source["row_index"]
    row, directory = latest[index]
    kind = classes[index]
    status = row["status"]
    receipt = None
    raw_result = None
    if status not in ["nontext_blank_leaf", "unreadable_or_nontext"]:
        receipt = directory / f"page-{index}.json"
        raw = receipt.read_bytes()
        if hashlib.sha256(raw).hexdigest() != row["receipt_sha256"]:
            raise ValueError("Receipt checksum mismatch")
        raw_result = json.loads(raw)
    if kind in ["blank_leaf", "nontext_cover"]:
        status = kind
    text = "Candidate relevance unreviewed; score is not accuracy."
    if kind == "blank_leaf":
        text = "Original image visually verified as blank; no inferred prose."
    elif kind == "nontext_cover":
        text = "Cover retained; no usable prose or inferred match."
    elif kind == "partial_plate":
        text = "Four-crop partial OCR retained; candidate does not repair missing plate content."
    elif index in [13, 104, 115]:
        text = "Separate narrow comparison reviewed; baseline match quality still requires adjudication."
    rows.append(
        {
            "row_index": index,
            "page_id": source["page_id"],
            "source_classification": kind,
            "status": status,
            "candidate_titles": [x["title"] for x in row.get("candidates", [])],
            "candidates": row.get("candidates", []),
            "review_state": text,
            "query": row.get("query"),
            "match_margin": raw_result.get("match_margin") if raw_result else None,
            "receipt_path": str(receipt) if receipt else None,
            "receipt_sha256": row.get("receipt_sha256"),
            "original_attempt_status": source["status"],
            "original_attempt_blockers": source.get("blockers", []),
            "final_blockers": row.get("blockers", []),
            "inference_tools": [
                t["tool"]
                for t in raw_result.get("traces", [])
                if t["status"] == "completed" and t["tool"].startswith(("nemotron.", "lancedb."))
            ]
            if raw_result
            else [],
        }
    )
if len(rows) != 100 or len({r["page_id"] for r in rows}) != 100:
    raise ValueError("100 distinct original pages required")
counts = dict(Counter(r["status"] for r in rows))
completed = sum(r["status"] in ["candidate", "ambiguous"] for r in rows)
summary = f"All 100 original pages accounted for. Real semantic retrieval completed for {completed} textual/partial pages: {counts.get('candidate', 0)} candidates and {counts.get('ambiguous', 0)} ambiguous outcomes. Three blank leaves and one nontext cover remain unmatched. One of the 96 textual pages is a partial astronomy plate. Candidate scores are uncalibrated; matching accuracy and full-page relevance remain unreviewed. Initial transport failures and targeted retries are retained."
report = {
    "reviewed_at": datetime.now(UTC).isoformat(),
    "summary": summary,
    "counts": counts,
    "content_counts": classification["counts"],
    "semantic_completed_pages": completed,
    "initial_attempt_counts": dict(Counter(r["status"] for r in baseline["results"])),
    "attempts": [str(d / "progress.json") for d in [baseline_dir, retry_dir, entry_dir]],
    "counts_store_native": entry["counts"],
    "accuracy": None,
    "accuracy_reason": "No adjudicated complete ground-truth match set; API success is not article relevance.",
    "query_method": "Initial first normalized OCR line; explicit targeted retries for misspelled/abbreviated headers 403,1032,2171. Multiple-entry pages can have partial-topic candidates.",
    "pages": rows,
}
for p in [Path("evidence/100-page-semantic-summary.json"), Path("archive/assets/matching-summary.json")]:
    p.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
with Path("evidence/100-page-semantic-ledger.csv").open("w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "row_index",
            "page_id",
            "source_classification",
            "status",
            "candidate_titles",
            "query",
            "match_margin",
            "review_state",
            "receipt_path",
            "receipt_sha256",
        ],
    )
    writer.writeheader()
    for row in rows:
        writer.writerow(
            {k: (" | ".join(row[k]) if k == "candidate_titles" else row[k]) for k in writer.fieldnames}
        )
print(
    json.dumps(
        {
            "counts": counts,
            "semantic_completed_pages": completed,
            "native_counts": entry["counts"],
            "summary_path": str(root / "evidence/100-page-semantic-summary.json"),
        }
    )
)
