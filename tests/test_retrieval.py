from dataclasses import replace

from test_evidence import document

from tomi_ai_hermes.application.retrieval import Pipeline
from tomi_ai_hermes.config import Config
from tomi_ai_hermes.domain.evidence import evidence_span


def test_semantic_inputs_remove_layout_tokens_without_changing_citation_source():
    historical = document(text="<x_0.1><y_0.2>Timber frames support ships.<class_Text>")
    modern = document("wikipedia", "Shipbuilding uses timber frames.")
    inputs = []

    class Core:
        def embed(self, texts, input_type):
            inputs.append((input_type, texts))
            return [[1.0, 0.0] for _ in texts]

        def rerank(self, query, texts, top_k):
            inputs.append(("rerank", [query, *texts]))
            return [{"index": 0, "relevance_score": 1.0}]

    class Store:
        def save_vectors(self, documents, vectors):
            assert documents == [modern]

        def search(self, vector, limit):
            return [{"document_id": modern.document_id, "_distance": 0.0}]

    result = {"traces": [], "candidate_query": "shipbuilding", "uncertainty": []}
    Pipeline(Config(), Core(), None, Store())._semantic(result, historical, [modern], 1)
    assert inputs[1] == ("query", ["shipbuilding\nTimber frames support ships."])
    assert all("<x_" not in text and "<class_" not in text for _, texts in inputs for text in texts)
    assert historical.text.startswith("<x_0.1>")
    start = historical.text.index("Timber")
    assert evidence_span(historical, start, start + 6)["quote"] == "Timber"
    assert result["retrieval_method"] == "nemotron_embed_lancedb_rerank"


def test_exact_title_candidate_survives_bm25_omission_but_not_wrong_snapshot():
    config = Config()
    history = document()
    exact = replace(document("wikipedia"), title="Shipbuilding", dataset_revision=config.wikipedia_revision)
    stale = replace(exact, document_id="wikipedia:stale", dataset_revision="other-snapshot")
    specialist = replace(exact, document_id="wikipedia:company", title="Shipbuilding Company")

    class Store:
        def all(self, corpus):
            return [history] if corpus == "britannica" else [specialist, stale, exact]

        def get(self, identity):
            return history

    class Wiki:
        def search(self, query, limit):
            return [{"page_id": "company"}]

    pipeline = Pipeline(config, None, Wiki(), Store())
    pipeline._fetch_candidates = lambda hits, result: [specialist]
    seen = []
    pipeline._semantic = lambda result, historical, documents, top_k: seen.extend(documents)
    pipeline.retrieve("Compare shipbuilding methods and vocabulary.", historical_page_id=history.document_id)
    assert seen == [specialist, exact]


def test_blank_parse_pages_remain_in_corpus_but_are_not_sent_to_embedding_provider():
    blank = document(text="<x_0.1><y_0.2><class_Picture>\n")
    prose = replace(document(text="<x_0.1>Timber ships<class_Text>"), document_id="britannica:2")
    submitted = []
    saved = []

    class Core:
        def embed(self, texts, input_type):
            submitted.append((input_type, texts))
            assert all(text.strip() for text in texts)
            return [[1.0, 0.0] for _ in texts]

    class Store:
        def save_vectors(self, docs, vectors):
            saved.extend(docs)

        def search(self, vector, limit):
            return [{"document_id": prose.document_id}]

        def get(self, identity):
            return prose

    selected = Pipeline(Config(), Core(), None, Store())._historical("ships", [blank, prose], [])
    assert selected == prose
    assert saved == [prose]
    assert submitted == [("query", ["ships"]), ("document", ["Timber ships"])]
    assert blank.text == "<x_0.1><y_0.2><class_Picture>\n"
