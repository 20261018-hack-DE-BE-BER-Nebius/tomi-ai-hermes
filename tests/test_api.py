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
