"""Model claims become evidence only after exact-span validation."""

import json

from tomi_ai_hermes.domain.evidence import Document, EvidenceError, validate_citation

CATEGORIES = {"language", "knowledge", "perspective", "coverage", "unresolved"}


def validate_answer(text: str, documents: list[Document]) -> dict:
    try:
        payload = json.loads(text)
    except ValueError, TypeError:
        raise EvidenceError("Hermes did not return the required JSON answer") from None
    if not isinstance(payload, dict) or not isinstance(payload.get("answer"), str):
        raise EvidenceError("Hermes answer must contain answer text and claims")
    claims = payload.get("claims")
    if not isinstance(claims, list) or len(claims) > 12:
        raise EvidenceError("Hermes claim array is invalid")
    by_id = {doc.document_id: doc for doc in documents}
    for claim in claims:
        if not isinstance(claim.get("text"), str) or claim.get("category") not in CATEGORIES:
            raise EvidenceError("Claim text or change category is invalid")
        refs = claim.get("citations")
        if not isinstance(refs, list) or not 2 <= len(refs) <= 8:
            raise EvidenceError("Every comparative claim requires evidence from both corpora")
        claim["citations"] = [validate_citation(ref, by_id) for ref in refs]
        corpora = {by_id[ref["document_id"]].corpus for ref in refs}
        if corpora != {"britannica", "wikipedia"}:
            raise EvidenceError("Comparative claims must cite historical and modern sources")
        claim["support_status"] = "span_verified_semantics_unreviewed"
    if not claims and not payload.get("abstained"):
        raise EvidenceError("An answer without supported claims must explicitly abstain")
    payload["verification"] = (
        "Exact source spans verified; claim entailment still requires independent review."
    )
    return payload
