from dataclasses import replace
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from tomi_ai_hermes.api.server import create_app
from tomi_ai_hermes.config import Config
from tomi_ai_hermes.infrastructure.store import EvidenceStore


def test_local_storage_default_remains_independent_of_receipts(tmp_path):
    config = replace(Config(), data_dir=tmp_path / "receipts")
    assert config.evidence_storage() == (tmp_path / "receipts/lancedb", {})
    separate = replace(config, lancedb_uri=str(tmp_path / "vectors"))
    assert separate.evidence_storage() == (tmp_path / "vectors", {})


def test_native_blob_uri_and_secret_options_reach_lancedb(monkeypatch, tmp_path):
    config = replace(
        Config(),
        data_dir=tmp_path,
        lancedb_uri="az://lancedb/tomi",
        azure_storage_account_name="fixtureaccount",
        azure_storage_account_key="fixture-storage-secret",
    )
    connect = MagicMock()
    monkeypatch.setattr("tomi_ai_hermes.infrastructure.store.lancedb.connect", connect)
    EvidenceStore.from_config(config)
    connect.assert_called_once_with(
        "az://lancedb/tomi",
        storage_options={"account_name": "fixtureaccount", "account_key": "fixture-storage-secret"},
    )
    assert connect.return_value.create_table.call_count == 2
    assert not (tmp_path / "lancedb").exists()
    assert "fixture-storage-secret" not in repr(config)


@pytest.mark.parametrize(
    "uri", ["az://lancedb/tomi?sig=secret", "az://user:secret@lancedb/tomi", "https://storage/tomi"]
)
def test_storage_credentials_cannot_be_embedded_in_uri(uri):
    with pytest.raises(ValueError, match="URI"):
        replace(Config(), lancedb_uri=uri).evidence_storage()


def test_missing_blob_credentials_are_explicit():
    with pytest.raises(ValueError, match="account name and key"):
        replace(Config(), lancedb_uri="az://lancedb/tomi").evidence_storage()


def test_atomic_commit_initialization_failure_is_redacted_and_unhealthy(monkeypatch):
    def fail(_):
        raise NotImplementedError("unsafe filesystem; private-storage-key")

    monkeypatch.setattr(EvidenceStore, "from_config", fail)
    client = TestClient(create_app(replace(Config(), service_token="fixture-token")))
    auth = {"Authorization": "Bearer fixture-token"}
    for path, body in [("/health", None), ("/ready", None), ("/v1/retrieve", {"question": "astronomy"})]:
        response = client.post(path, headers=auth, json=body) if body else client.get(path, headers=auth)
        assert response.status_code == 503
        assert response.json()["error_code"] == "evidence_storage_unavailable"
        assert response.json()["error_type"] == "NotImplementedError"
        assert "private-storage-key" not in response.text
    assert client.get("/ready").status_code == 401


def test_seed_initialization_error_cannot_report_healthy(monkeypatch):
    monkeypatch.setattr(EvidenceStore, "from_config", lambda _: MagicMock())

    def fail(*_):
        raise ValueError("Bundled source seed checksum differs")

    monkeypatch.setattr("tomi_ai_hermes.api.server.import_seed", fail)
    client = TestClient(create_app(replace(Config(), service_token="fixture-token")))
    assert client.get("/health").status_code == 503


def test_storage_secret_never_enters_agent_worker(monkeypatch, tmp_path):
    import json
    from types import SimpleNamespace

    from tomi_ai_hermes.infrastructure.agent import HermesAgent

    received = {}

    def run(*args, **kwargs):
        received.update(kwargs)
        return SimpleNamespace(returncode=0, stdout='{"abstained":true}')

    monkeypatch.setattr("tomi_ai_hermes.infrastructure.agent.subprocess.run", run)
    config = replace(
        Config(),
        data_dir=tmp_path,
        azure_storage_account_key="private-storage-key",
        service_token="inbound-token",
    )
    HermesAgent(config).compare("Compare", "en", {})
    assert "private-storage-key" not in received["input"]
    assert "inbound-token" not in received["input"]
    assert "azure_storage_account_key" not in json.loads(received["input"])["config"]
    assert not any("AZURE" in key for key in received["env"])
