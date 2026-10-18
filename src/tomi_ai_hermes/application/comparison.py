"""Persist genuine comparison receipts including failures and missing dependencies."""

import json
import uuid
from datetime import UTC, datetime

from tomi_ai_hermes.domain.answers import validate_answer
from tomi_ai_hermes.domain.evidence import (
    DependencyUnavailable,
    Document,
    EvidenceError,
    excerpt_spans,
    sha256,
)


class Comparison:
    def __init__(self, config, pipeline, agent):
        self.config, self.pipeline, self.agent = config, pipeline, agent

    def run(
        self, question: str, locale: str = "en", historical_page_id: str | None = None, top_k: int = 5
    ) -> dict:
        result = self.pipeline.retrieve(question, locale, historical_page_id, top_k)
        result["run_id"] = str(uuid.uuid4())
        result["created_at"] = datetime.now(UTC).isoformat()
        result["answer"], result["claims"], result["citations"] = "", [], []
        if result["status"] != "blocked":
            self._answer(result)
        self._persist(result)
        return result

    def _answer(self, result: dict):
        documents = [Document(**result["historical"])]
        for row in result["candidates"]:
            documents.append(Document(**{k: v for k, v in row.items() if k in Document.__dataclass_fields__}))
        evidence_docs = [
            dict({k: v for k, v in doc.to_dict().items() if k != "text"}, excerpt_spans=excerpt_spans(doc))
            for doc in documents[:3]
        ]
        evidence = {
            "documents": evidence_docs,
            "uncertainty": result["uncertainty"],
            "metrics": result["metrics"],
        }
        try:
            response = self.agent.compare(result["question"], result["locale"], evidence)
            result["traces"].extend(response.get("tool_calls", []))
            answer = validate_answer(response["final_response"], documents)
            result.update(answer)
            result["status"] = "abstained" if answer.get("abstained") else "needs_review"
            result["citations"] = [ref for claim in answer["claims"] for ref in claim["citations"]]
            result["agent_receipt"] = {k: v for k, v in response.items() if k != "final_response"}
        except (DependencyUnavailable, EvidenceError) as error:
            result["status"] = "blocked"
            result["blockers"].append(str(error))

    def _persist(self, result: dict):
        directory = self.config.data_dir / "runs"
        directory.mkdir(parents=True, exist_ok=True)
        serialized = json.dumps(result, sort_keys=True, ensure_ascii=False)
        (directory / (result["run_id"] + ".json")).write_text(serialized)
        result["receipt_sha256"] = sha256(serialized)
        if result["status"] in {"needs_review", "abstained"}:
            proof = {"run_id": result["run_id"], "receipt_sha256": result["receipt_sha256"]}
            (self.config.data_dir / "readiness.json").write_text(json.dumps(proof))
