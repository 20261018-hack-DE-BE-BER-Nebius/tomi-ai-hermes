import json

import pytest
from test_evidence import document

from tomi_ai_hermes.domain.answers import bind_span_references, validate_answer
from tomi_ai_hermes.domain.evidence import EvidenceError, evidence_span


def offered():
    docs = [document(text="The veffel contains fluid. 😀"), document("wikipedia", "The vessel holds liquid.")]
    evidence = [{"excerpt_spans": [{**evidence_span(doc, 0, len(doc.text)), "span_id": f"d{i}s0"}]}
                for i, doc in enumerate(docs)]
    answer = {"answer": "Both describe vessels.", "abstained": False,
              "claims": [{"text": "Both excerpts describe a vessel containing liquid.", "category": "coverage",
                          "citations": [{"span_id": "d0s0"}, {"span_id": "d1s0"}]}]}
    return docs, evidence, answer


def test_selected_ids_bind_exact_unicode_ocr_then_pass_existing_validator():
    docs, evidence, answer = offered()
    bound = bind_span_references(json.dumps(answer), evidence)
    validated = validate_answer(bound, docs)
    assert validated["claims"][0]["citations"][0]["quote"] == docs[0].text


@pytest.mark.parametrize("reference", [
    {"span_id": "foreign"},
    {"span_id": "d0s0", "quote": "invented"},
    {"span_id": "d0s0", "start_cp": 1},
])
def test_unknown_or_overridden_span_is_rejected(reference):
    _, evidence, answer = offered()
    answer["claims"][0]["citations"][0] = reference
    with pytest.raises(EvidenceError):
        bind_span_references(json.dumps(answer), evidence)


def test_binding_cannot_bypass_both_corpora_requirement():
    docs, evidence, answer = offered()
    answer["claims"][0]["citations"] = [{"span_id": "d0s0"}, {"span_id": "d0s0"}]
    with pytest.raises(EvidenceError, match="historical and modern"):
        validate_answer(bind_span_references(json.dumps(answer), evidence), docs)
