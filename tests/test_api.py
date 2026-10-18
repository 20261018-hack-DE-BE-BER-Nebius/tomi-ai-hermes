from dataclasses import replace

from fastapi.testclient import TestClient

from tomi_ai_hermes.api.server import create_app
from tomi_ai_hermes.config import Config


class StubPipeline:
    def retrieve(self, **kwargs):
        return {"status": "blocked", "blockers": ["fixture: no corpus"], "candidates": []}


def test_authentication_unknown_fields_and_blocked_status():
    app = create_app(replace(Config(), service_token="fixture-only"), StubPipeline(), object())
    client = TestClient(app)
    assert client.get("/health").status_code == 200
    assert client.post("/v1/retrieve", json={"question": "x"}).status_code == 401
    auth = {"Authorization": "Bearer fixture-only"}
    assert (
        client.post("/v1/retrieve", headers=auth, json={"question": "x", "url": "http://private"}).status_code
        == 422
    )
    assert client.post("/v1/retrieve", headers=auth, json={"question": "x"}).status_code == 503


def test_compare_accepts_bounded_discovery_query_without_overwriting_question(tmp_path):
    from tomi_ai_hermes.application.comparison import Comparison

    calls = []

    class Pipeline:
        def retrieve(self, question, locale, page_id, top_k):
            calls.append(question)
            return {"question": question, "status": "candidate", "blockers": []}

    class InspectComparison(Comparison):
        def _answer(self, result):
            assert result["question"] == "Compare only shelf-pieces with shipyards."
            result["status"] = "needs_review"

    config = replace(Config(), service_token="fixture-only", data_dir=tmp_path)
    pipeline = Pipeline()
    app = create_app(config, pipeline, InspectComparison(config, pipeline, None))
    client = TestClient(app)
    auth = {"Authorization": "Bearer fixture-only"}
    body = {"question": "Compare only shelf-pieces with shipyards.", "discovery_query": "shipbuilding techniques"}
    response = client.post("/v1/compare", headers=auth, json=body)
    assert response.status_code == 200
    assert calls == ["shipbuilding techniques"]
    assert response.json()["discovery_question"] == "shipbuilding techniques"
    assert client.post("/v1/retrieve", headers=auth, json=body).status_code == 422
    body["discovery_query"] = "x" * 513
    assert client.post("/v1/compare", headers=auth, json=body).status_code == 422
