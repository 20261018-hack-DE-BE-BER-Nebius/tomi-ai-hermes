"""Sequential, checkpointed real evaluation; this runner never declares successes."""

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

from tomi_ai_hermes.application.comparison import Comparison
from tomi_ai_hermes.application.evaluation import CASES
from tomi_ai_hermes.application.ingest import read_manifest
from tomi_ai_hermes.application.retrieval import Pipeline
from tomi_ai_hermes.config import Config
from tomi_ai_hermes.domain.evidence import plain_ocr
from tomi_ai_hermes.infrastructure.agent import HermesAgent
from tomi_ai_hermes.infrastructure.core import CoreClient
from tomi_ai_hermes.infrastructure.store import EvidenceStore
from tomi_ai_hermes.infrastructure.wikipedia import WikipediaClient


def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def main():
    args = argparse.ArgumentParser()
    args.add_argument("mode", choices=["cases", "sample"])
    args.add_argument("--output", type=Path, required=True)
    args.add_argument("--cases", type=Path, help="Explicit evaluation questions and optional discovery query")
    options = args.parse_args()
    options.output.mkdir(parents=True, exist_ok=False)
    config = Config.from_env()
    store = EvidenceStore.from_config(config)
    pipeline = Pipeline(config, CoreClient(config), WikipediaClient(config), store)
    report = {
        "started_at": datetime.now(UTC).isoformat(),
        "mode": options.mode,
        "execution": "real sequential model and source calls, no mock transport",
        "models": {
            "agent_alias": config.agent_model,
            "embed_alias": config.embed_model,
            "embed_revision": config.embed_revision,
            "embed_dimensions": config.embed_dimensions,
            "rerank_alias": config.rerank_model,
            "rerank_revision": config.rerank_revision,
        },
        "results": [],
        "human_review": "pending",
        "successful_cases_claimed": 0,
    }
    save(options.output / "progress.json", report)
    if options.mode == "cases":
        comparison = Comparison(config, pipeline, HermesAgent(config))
        cases = json.loads(options.cases.read_text()) if options.cases else CASES
        for case in cases:
            page_id = "britannica:309f765b1ecc83e0a7f7762e44b4a927a7555443:train:" + str(case["row"])
            result = comparison.run(
                case["question"], "en", page_id, top_k=3, discovery_query=case.get("discovery_query")
            )
            original = config.data_dir / "runs" / (result["run_id"] + ".json")
            raw = original.read_bytes()
            digest = hashlib.sha256(raw).hexdigest()
            if digest != result["receipt_sha256"]:
                raise ValueError("Persisted comparison receipt integrity mismatch")
            (options.output / (case["id"] + ".json")).write_bytes(raw)
            report["results"].append(
                {
                    "case": case["id"],
                    "intended": case["intended"],
                    "status": result["status"],
                    "run_id": result["run_id"],
                    "receipt_sha256": digest,
                    "claim_count": len(result["claims"]),
                    "blockers": result["blockers"],
                    "human_review": "pending",
                }
            )
            save(options.output / "progress.json", report)
            print(json.dumps(report["results"][-1]), flush=True)
    else:
        manifest = read_manifest(config.manifest_path)
        report["selection"] = manifest["selection"]
        report["sample_size"] = len(manifest["pages"])
        for page in manifest["pages"]:
            document = store.get(page["page_id"])
            row = {
                "page_id": page["page_id"],
                "row_index": page["row_index"],
                "human_review": "pending",
                "accepted_article_ids": [],
            }
            if document is None:
                row.update(
                    status="unreadable_or_nontext", reason="No accepted OCR record; original page retained"
                )
            else:
                query = plain_ocr(document.text).strip().split("\n")[0][:256]
                row["query_method"] = "production baseline: first normalized OCR line, at most256 characters"
                result = pipeline.retrieve(query, "en", document.document_id, 3, require_semantic=True)
                receipt = options.output / ("page-" + str(page["row_index"]) + ".json")
                save(receipt, result)
                row.update(
                    status=result["status"],
                    query=query,
                    receipt_sha256=hashlib.sha256(receipt.read_bytes()).hexdigest(),
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
            report["results"].append(row)
            save(options.output / "progress.json", report)
            print(
                json.dumps(
                    {
                        "row_index": row["row_index"],
                        "status": row["status"],
                        "completed": len(report["results"]),
                    }
                ),
                flush=True,
            )
    report["completed_at"] = datetime.now(UTC).isoformat()
    report["counts"] = store.counts()
    save(options.output / "progress.json", report)


if __name__ == "__main__":
    main()
