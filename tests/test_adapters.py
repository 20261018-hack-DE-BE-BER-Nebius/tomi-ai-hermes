from dataclasses import replace

import pytest
from test_evidence import document

from tomi_ai_hermes.config import Config
from tomi_ai_hermes.domain.evidence import EvidenceError, sha256
from tomi_ai_hermes.infrastructure.core import CoreClient
from tomi_ai_hermes.infrastructure.store import EvidenceStore
from tomi_ai_hermes.infrastructure.wikipedia import WikipediaClient


def test_embedding_duplicate_index_is_rejected():
    config = replace(Config(), embed_dimensions=2)
    client = CoreClient(config)
    client.request = lambda *args, **kwargs: {
        "model_revision": config.embed_revision,
        "data": [{"index": 0, "embedding": [1, 0]}, {"index": 0, "embedding": [0, 1]}],
    }
    with pytest.raises(EvidenceError, match="duplicated"):
        client.embed(["one", "two"], "document")


def test_wrong_embedding_revision_is_rejected():
    client = CoreClient(Config())
    client.request = lambda *args, **kwargs: {"model_revision": "wrong", "data": []}
    with pytest.raises(EvidenceError, match="revision"):
        client.embed(["one"], "query")


def test_wikipedia_complete_hash_and_pagination():
    config = Config()
    client = WikipediaClient(config)
    text = "Hello 😀 world"

    def request(method, path, params):
        offset = params["offset"]
        return {
            "page_id": "1",
            "offset": offset,
            "text": text[:8] if offset == 0 else text[8:],
            "next_offset": 8 if offset == 0 else None,
            "title": "Example",
            "revision_id": "123",
            "url": "https://en.wikipedia.org/wiki/Example",
            "license": {"spdx": "CC-BY-SA-4.0"},
            "provenance": {"dataset_revision": config.wikipedia_revision, "text_sha256": sha256(text)},
        }

    client.request = request
    assert client.article("1").text == text
    with pytest.raises(EvidenceError):
        client.article("../../private")


def test_lancedb_persists_exact_source(tmp_path):
    store = EvidenceStore(tmp_path, 2, "test-only", "fixture")
    doc = document()
    store.save(doc)
    store.save_vectors([doc], [[1.0, 0.0]])
    assert store.get(doc.document_id).text == doc.text
    assert store.search([1.0, 0.0], 1)[0]["document_id"] == doc.document_id


def test_seed_rejects_tampered_file(tmp_path):
    import json

    from tomi_ai_hermes.application.seed import import_seed

    directory = tmp_path / "seed"
    directory.mkdir()
    (directory / "documents.jsonl").write_text("changed")
    (directory / "manifest.json").write_text(json.dumps({"files": {"documents.jsonl": "0" * 64}}))
    store = EvidenceStore(tmp_path / "db", 2, "fixture", "v1")
    with pytest.raises(EvidenceError, match="checksum"):
        import_seed(store, directory)
