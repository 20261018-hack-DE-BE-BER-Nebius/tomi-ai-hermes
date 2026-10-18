"""Candidate discovery, actual model calls and explicit match uncertainty."""

import time
from datetime import UTC, datetime

from tomi_ai_hermes.config import Config
from tomi_ai_hermes.domain.evidence import (
    DependencyUnavailable,
    EvidenceError,
    injection_markers,
    lexical_metrics,
    plain_ocr,
)
from tomi_ai_hermes.domain.queries import candidate_query


class Pipeline:
    def __init__(self, config: Config, core, wikipedia, store):
        self.config, self.core, self.wikipedia, self.store = config, core, wikipedia, store

    def _call(self, traces: list, name: str, action):
        started = time.monotonic()
        try:
            result = action()
        except (DependencyUnavailable, EvidenceError) as error:
            traces.append(
                {
                    "tool": name,
                    "status": "failed",
                    "duration_ms": round((time.monotonic() - started) * 1000),
                    "error": str(error),
                    "occurred_at": datetime.now(UTC).isoformat(),
                }
            )
            raise
        traces.append(
            {
                "tool": name,
                "status": "completed",
                "duration_ms": round((time.monotonic() - started) * 1000),
                "occurred_at": datetime.now(UTC).isoformat(),
            }
        )
        return result

    def retrieve(
        self,
        question: str,
        locale: str = "en",
        historical_page_id: str | None = None,
        top_k: int = 5,
        require_semantic: bool = True,
    ) -> dict:
        result = {
            "status": "running",
            "question": question,
            "locale": locale,
            "candidates": [],
            "historical": None,
            "traces": [],
            "blockers": [],
            "metrics": None,
            "uncertainty": [],
        }
        try:
            self._retrieve_into(result, question, historical_page_id, top_k, require_semantic)
        except (DependencyUnavailable, EvidenceError) as error:
            result["status"] = "blocked"
            result["blockers"].append(str(error))
        return result

    def _retrieve_into(
        self, result: dict, question: str, page_id: str | None, top_k: int, require_semantic: bool
    ):
        traces = result["traces"]
        histories = self.store.all("britannica")
        if not histories:
            raise DependencyUnavailable("historical_corpus", "No parsed historical pages; run ingest first")
        historical = (
            self.store.get(page_id)
            if page_id
            else self._select_history(question, histories, result, require_semantic)
        )
        if not historical or historical.corpus != "britannica":
            raise EvidenceError("Historical page ID is absent from the pinned, parsed sample")
        historical.validate()
        result["historical"] = historical.to_dict()
        query = candidate_query(question)
        result["candidate_query"] = query
        hits = self._call(traces, "wikipedia.search", lambda: self.wikipedia.search(query, max(top_k, 8)))
        documents = self._fetch_candidates(hits, result)
        # Short BM25 queries can rank specialist companies above an encyclopedia
        # entry. Retain an exact-title entry already verified in this snapshot.
        exact = self._call(
            traces,
            "wikipedia.cached_exact_title",
            lambda: [
                doc for doc in self.store.all("wikipedia")
                if doc.title.casefold() == query.casefold()
                and doc.dataset_revision == self.config.wikipedia_revision
            ],
        )
        identities = {doc.document_id for doc in documents}
        documents.extend(doc for doc in exact if doc.document_id not in identities)
        if not documents:
            raise DependencyUnavailable("wikipedia", "No complete, hash-verified candidates")
        try:
            self._semantic(result, historical, documents, top_k)
        except DependencyUnavailable as error:
            if require_semantic:
                raise
            result["status"] = "partial"
            result["retrieval_method"] = "lexical_bm25"
            result["challenge_ready"] = False
            result["blockers"].append(str(error))
            result["candidates"] = [
                dict(doc.to_dict(), score=None, score_type="unranked_lexical_candidate")
                for doc in documents[:top_k]
            ]
            result["metrics"] = lexical_metrics(historical.text, documents[0].text)
            result["uncertainty"].append(
                "Lexical baseline only: Nemotron semantic matching has not completed."
            )

    def _semantic(self, result, historical, documents, top_k):
        traces = result["traces"]
        # Parse control tokens describe layout, not article meaning. Keep raw
        # sources immutable for citations and normalize only model inputs.
        texts = [plain_ocr(doc.text)[:5000] for doc in documents]
        query = result["candidate_query"] + "\n" + plain_ocr(historical.text)[:1000]
        result["semantic_input"] = {
            "query": query,
            "normalization": "remove Parse layout control tokens only; raw evidence unchanged",
            "historical_prefix_characters": 1000,
            "candidate_prefix_characters": 5000,
        }
        vectors = self._call(
            traces,
            "nemotron.embed.document",
            lambda: self.core.embed(texts, "document"),
        )
        self.store.save_vectors(documents, vectors)
        vector = self._call(
            traces, "nemotron.embed.query", lambda: self.core.embed([query], "query")
        )[0]
        neighbors = self._call(traces, "lancedb.search", lambda: self.store.search(vector, len(documents)))
        distances = {row["document_id"]: row["_distance"] for row in neighbors}
        ranked = self._call(
            traces,
            "nemotron.rerank",
            lambda: self.core.rerank(query, texts, top_k),
        )
        result["candidates"] = [
            dict(
                documents[row["index"]].to_dict(),
                score=row["relevance_score"],
                vector_distance=distances.get(documents[row["index"]].document_id),
                score_type="raw_logit",
            )
            for row in ranked
        ]
        self._decide(result, historical)
        result["retrieval_method"] = "nemotron_embed_lancedb_rerank"
        result["challenge_ready"] = True

    def _select_history(self, question, documents, result, require_semantic):
        try:
            return self._historical(question, documents, result["traces"])
        except DependencyUnavailable:
            if require_semantic:
                raise
            import re

            words = set(candidate_query(question).split())
            scored = [
                (
                    len(
                        words
                        & set(
                            re.findall(
                                r"[^\W\d_]+", re.sub(r"(?<=\w)-(?=\w)", "", plain_ocr(doc.text.casefold()))
                            )
                        )
                    ),
                    doc,
                )
                for doc in documents
            ]
            score, selected = max(scored, key=lambda pair: pair[0])
            if score == 0:
                raise DependencyUnavailable(
                    "historical_corpus", "No lexical overlap with parsed historical pages"
                )
            result["uncertainty"].append(
                "Historical page selected by lexical overlap; semantic selection unavailable."
            )
            return selected

    def _historical(self, question: str, documents: list, traces: list):
        vector = self._call(traces, "nemotron.embed.query", lambda: self.core.embed([question], "query"))[0]
        for offset in range(0, len(documents), 16):
            batch = documents[offset : offset + 16]
            embeddings = self._call(
                traces,
                "nemotron.embed.history",
                lambda batch=batch: self.core.embed([plain_ocr(doc.text)[:5000] for doc in batch], "document"),
            )
            self.store.save_vectors(batch, embeddings)
        neighbors = self._call(traces, "lancedb.historical", lambda: self.store.search(vector, 200))
        history_ids = {doc.document_id for doc in documents}
        return next(
            (self.store.get(row["document_id"]) for row in neighbors if row["document_id"] in history_ids),
            None,
        )

    def _fetch_candidates(self, hits: list[dict], result: dict) -> list:
        documents = []
        for hit in hits:
            try:
                document = self._call(
                    result["traces"],
                    "wikipedia.article",
                    lambda hit=hit: self.wikipedia.article(str(hit["page_id"])),
                )
                self.store.save(document)
                documents.append(document)
            except (DependencyUnavailable, EvidenceError) as error:
                result["uncertainty"].append(str(error))
        return documents

    def _decide(self, result: dict, historical):
        candidates = result["candidates"]
        margin = candidates[0]["score"] - candidates[1]["score"] if len(candidates) > 1 else None
        result["status"] = "ambiguous" if margin is None or margin < self.config.match_margin else "candidate"
        result["uncertainty"].append(
            "Reranker logits are relevance scores, not calibrated probabilities; human match review is pending."
        )
        if result["status"] == "ambiguous":
            result["uncertainty"].append(
                "Top candidate margin is insufficient or only one candidate was returned."
            )
        result["match_margin"] = margin
        result["metrics"] = lexical_metrics(historical.text, candidates[0]["text"])
        markers = injection_markers(historical.text) + [
            marker for doc in candidates for marker in injection_markers(doc["text"])
        ]
        if markers:
            result["uncertainty"].append(
                "Untrusted source instruction markers detected: " + ", ".join(sorted(set(markers)))
            )
