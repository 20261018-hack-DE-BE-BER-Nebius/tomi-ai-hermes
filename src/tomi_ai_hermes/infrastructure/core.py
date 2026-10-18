"""Nemotron adapters use the authenticated Rust gateway exclusively."""

import base64
import math

from tomi_ai_hermes.config import Config
from tomi_ai_hermes.domain.evidence import EvidenceError
from tomi_ai_hermes.infrastructure.http import JSONClient

PARSE_PROMPT = "</s><s><predict_bbox><predict_classes><output_markdown><predict_text_in_pic>"


class CoreClient(JSONClient):
    def __init__(self, config: Config):
        super().__init__(config.core_url, config.timeout_seconds, config.core_token)
        self.config = config

    def parse(self, image: bytes) -> dict:
        content = [
            {"type": "text", "text": PARSE_PROMPT},
            {
                "type": "image_url",
                "image_url": {"url": "data:image/jpeg;base64," + base64.b64encode(image).decode()},
            },
        ]
        return self.request(
            "POST",
            "v1/parse",
            json={
                "model": self.config.parse_model,
                "messages": [{"role": "user", "content": content}],
                "max_tokens": self.config.parse_max_tokens,
                "temperature": 0,
                "skip_special_tokens": False,
                "add_special_tokens": False,
            },
        )

    def embed(self, texts: list[str], input_type: str) -> list[list[float]]:
        result = self.request(
            "POST",
            "v1/embeddings",
            json={"model": self.config.embed_model, "input": texts, "input_type": input_type},
        )
        if result.get("model_revision") != self.config.embed_revision:
            raise EvidenceError("Embedding model revision differs from pinned organizer model")
        rows = result.get("data", [])
        if len(rows) != len(texts):
            raise EvidenceError("Embedding count differs from request")
        vectors = {}
        for row in rows:
            index, vector = row.get("index"), row.get("embedding")
            if type(index) is not int or not 0 <= index < len(texts) or index in vectors:
                raise EvidenceError("Embedding index is invalid or duplicated")
            if not isinstance(vector, list) or len(vector) != self.config.embed_dimensions:
                raise EvidenceError("Embedding dimension differs from configured model")
            if any(type(x) not in {float, int} or not math.isfinite(x) for x in vector):
                raise EvidenceError("Embedding contains nonfinite values")
            if abs(sum(x * x for x in vector) - 1) > 0.02:
                raise EvidenceError("Embedding is not unit normalized")
            vectors[index] = vector
        return [vectors[i] for i in range(len(texts))]

    def rerank(self, question: str, texts: list[str], top_n: int) -> list[dict]:
        result = self.request(
            "POST",
            "v1/rerank",
            json={
                "model": self.config.rerank_model,
                "query": question,
                "documents": texts,
                "top_n": min(top_n, len(texts)),
            },
        )
        if result.get("model_revision") != self.config.rerank_revision:
            raise EvidenceError("Reranker model revision differs from pinned organizer model")
        if result.get("score_type") not in {"raw_logit", "logit"}:
            raise EvidenceError("Reranker score semantics differ")
        rows = result.get("results", result.get("data", []))
        if not rows:
            raise EvidenceError("Reranker returned no candidates")
        seen = set()
        for row in rows:
            index, score = row.get("index"), row.get("relevance_score")
            if type(index) is not int or not 0 <= index < len(texts) or index in seen:
                raise EvidenceError("Reranker index is invalid or duplicated")
            if type(score) not in {float, int} or not math.isfinite(score):
                raise EvidenceError("Reranker score is not finite")
            seen.add(index)
        return sorted(rows, key=lambda row: row["relevance_score"], reverse=True)
