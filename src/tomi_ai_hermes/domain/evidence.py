"""Deterministic evidence identities, spans and lexical metrics (no I/O)."""

import hashlib
import math
import re
from collections import Counter
from dataclasses import asdict, dataclass


class EvidenceError(ValueError):
    """Data failed an evidence invariant; never silently substitute it."""


class DependencyUnavailable(RuntimeError):
    def __init__(self, component: str, detail: str):
        self.component = component
        self.detail = detail
        super().__init__(f"{component}: {detail}")


def sha256(data: bytes | str) -> str:
    return hashlib.sha256(data.encode("utf-8") if isinstance(data, str) else data).hexdigest()


@dataclass(frozen=True)
class Document:
    document_id: str
    title: str
    corpus: str
    text: str
    source_url: str
    revision_id: str
    text_sha256: str
    dataset_revision: str
    license: str
    acquired_at: str
    parser_receipt_sha256: str = ""
    source_kind: str = "prose"
    parse_status: str = "parsed"

    def validate(self) -> None:
        if not self.text or sha256(self.text) != self.text_sha256:
            raise EvidenceError("Source text is empty or its checksum differs")
        if self.corpus not in {"britannica", "wikipedia"}:
            raise EvidenceError("Unsupported corpus")
        if not self.document_id or not self.dataset_revision:
            raise EvidenceError("Source identity and dataset revision are required")

    def to_dict(self) -> dict:
        self.validate()
        return asdict(self)


def evidence_span(document: Document, start: int, end: int) -> dict:
    document.validate()
    if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(document.text):
        raise EvidenceError("Evidence offsets must index raw Unicode code points")
    quote = document.text[start:end]
    return {
        "document_id": document.document_id,
        "text_sha256": document.text_sha256,
        "start_cp": start,
        "end_cp": end,
        "quote": quote,
        "offset_basis": "raw_codepoints",
        "source_url": document.source_url,
        "revision_id": document.revision_id,
    }


def validate_citation(citation: dict, documents: dict[str, Document]) -> dict:
    document = documents.get(citation.get("document_id"))
    if document is None:
        raise EvidenceError("Citation refers to a source not retrieved in this run")
    span = evidence_span(document, citation.get("start_cp"), citation.get("end_cp"))
    if citation.get("quote") != span["quote"]:
        raise EvidenceError("Citation quote does not match the exact source span")
    return span


def lexical_metrics(historical: str, modern: str) -> dict:
    counts = [
        Counter(re.findall(r"[^\W\d_]+", text.casefold()))
        for text in (plain_ocr(historical), plain_ocr(modern))
    ]
    vocab = set(counts[0]) | set(counts[1])
    total = [sum(c.values()) for c in counts]
    distributions = [{w: c[w] / max(n, 1) for w in vocab} for c, n in zip(counts, total)]
    midpoint = {w: (distributions[0][w] + distributions[1][w]) / 2 for w in vocab}
    divergence = sum(
        p[w] * math.log2(p[w] / midpoint[w]) / 2 for p in distributions for w in vocab if p[w] > 0
    )
    return {
        "historical_words": total[0],
        "modern_words": total[1],
        "vocabulary_jaccard": len(set(counts[0]) & set(counts[1])) / max(len(vocab), 1),
        "jensen_shannon_divergence": divergence,
        "historical_top_words": counts[0].most_common(15),
        "modern_top_words": counts[1].most_common(15),
        "interpretation": "Lexical differences alone do not establish a change in factual knowledge.",
    }


def injection_markers(text: str) -> list[str]:
    patterns = {
        "instruction_override": r"ignore (?:all |any )?(?:previous|prior) (?:instructions|context)",
        "role_impersonation": r"(?:^|\n)\s*(?:system|assistant|developer)\s*:",
        "secret_request": r"(?:reveal|print|send|exfiltrate).{0,50}(?:api.?key|secret|token)",
    }
    return [name for name, pattern in patterns.items() if re.search(pattern, text, re.IGNORECASE)]


def plain_ocr(text: str) -> str:
    """Remove Parse's layout control tokens for metrics; preserve stored raw text and hashes."""
    return re.sub(r"<(?:[xy]_[^>]+|class_[^>]+)>", "", text)


def excerpt_spans(document: Document, limit: int = 12) -> list[dict]:
    """Give the agent existing valid spans so it need not invent offsets."""
    candidates = []
    for match in re.finditer(r"(?:(?!<(?:[xy]_|class_))[^<>]){30,800}", document.text):
        start, end = match.span()
        while start < end and document.text[start].isspace():
            start += 1
        while end > start and document.text[end - 1].isspace():
            end -= 1
        if end > start:
            candidates.append(evidence_span(document, start, end))
        if len(candidates) >= limit:
            break
    return candidates
