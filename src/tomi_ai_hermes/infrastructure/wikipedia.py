"""The organizer's pinned Wikimedia Structured Contents API, including complete pagination."""

import re
from datetime import UTC, datetime

from tomi_ai_hermes.config import Config
from tomi_ai_hermes.domain.evidence import Document, EvidenceError, sha256
from tomi_ai_hermes.infrastructure.http import JSONClient


class WikipediaClient(JSONClient):
    def __init__(self, config: Config):
        super().__init__(config.wikipedia_url, config.timeout_seconds)
        self.config = config

    def search(self, query: str, top_k: int) -> list[dict]:
        result = self.request(
            "POST",
            "v1/search",
            json={"query": " ".join(query.split()[:64])[:512], "top_k": top_k, "excerpt_chars": 1000},
        )
        if result.get("corpus_revision") != self.config.wikipedia_revision:
            raise EvidenceError("Wikipedia search corpus revision differs from the pinned snapshot")
        return result["hits"]

    def article(self, page_id: str) -> Document:
        if not re.fullmatch(r"[0-9]{1,20}", page_id):
            raise EvidenceError("Wikipedia page ID must be numeric")
        pieces, offset, first = [], 0, None
        while True:
            page = self.request(
                "GET", f"v1/articles/{page_id}", params={"offset": offset, "max_chars": 20000}
            )
            first = first or page
            self._validate_page(page, first, page_id, offset)
            pieces.append(page["text"])
            offset += len(page["text"])
            if offset > self.config.max_article_chars:
                raise EvidenceError("Wikipedia article exceeds configured complete-text limit")
            if page.get("next_offset") is None:
                break
            if page["next_offset"] != offset or not page["text"]:
                raise EvidenceError("Wikipedia pagination is incomplete or cyclic")
        return self._document(first, "".join(pieces))

    def _validate_page(self, page: dict, first: dict, page_id: str, offset: int):
        provenance = page.get("provenance", {})
        if str(page.get("page_id")) != page_id or page.get("offset") != offset:
            raise EvidenceError("Wikipedia article identity or offset differs")
        if provenance.get("dataset_revision") != self.config.wikipedia_revision:
            raise EvidenceError("Wikipedia article dataset revision differs")
        if provenance.get("text_sha256") != first.get("provenance", {}).get("text_sha256"):
            raise EvidenceError("Wikipedia checksum changed during pagination")
        if page.get("license", {}).get("spdx") != "CC-BY-SA-4.0":
            raise EvidenceError("Wikipedia attribution metadata is missing")

    def _document(self, page: dict, text: str) -> Document:
        provenance = page["provenance"]
        if sha256(text) != provenance["text_sha256"]:
            raise EvidenceError("Complete Wikipedia text checksum differs")
        doc = Document(
            document_id="wikipedia:" + str(page["page_id"]),
            title=page["title"],
            corpus="wikipedia",
            text=text,
            source_url=provenance.get("revision_url") or page["url"],
            revision_id=str(page["revision_id"]),
            text_sha256=provenance["text_sha256"],
            dataset_revision=self.config.wikipedia_revision,
            license="CC-BY-SA-4.0; Wikipedia contributors",
            acquired_at=datetime.now(UTC).isoformat(),
        )
        doc.validate()
        return doc
