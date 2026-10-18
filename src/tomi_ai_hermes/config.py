"""One configuration boundary; upstream provider keys never enter this service."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlsplit

from dotenv import load_dotenv


@dataclass(frozen=True)
class Config:
    host: str = "0.0.0.0"
    port: int = 8083
    core_url: str = "http://127.0.0.1:8081"
    core_token: str = field(default="", repr=False)
    service_token: str = field(default="", repr=False)
    wikipedia_url: str = "https://port8000-rks0xavparpzq59.tunnel.applications.uk-south2.nebius.cloud"
    wikipedia_revision: str = "417c267bb457fa645c22eb3b5c77764963194c70"
    dataset_base_url: str = "https://huggingface.co/datasets"
    data_dir: Path = Path("data")
    lancedb_uri: str = ""
    azure_storage_account_name: str = ""
    azure_storage_account_key: str = field(default="", repr=False)
    seed_dir: Path = Path("resources/corpus")
    manifest_path: Path = Path("resources/upstream/britannica-manifest.json")
    agent_model: str = "nemotron-3.5-super-vl"
    embed_model: str = "nemotron-3-embed-vl"
    rerank_model: str = "nemotron-3-rerank-vl"
    parse_model: str = "nemotron-parse-3.5"
    parse_max_tokens: int = 8744
    embed_dimensions: int = 2048
    embed_revision: str = "582e3bf72aee355e3c59ed89de53543c5b0657ee"
    rerank_revision: str = "b8a9987b05b75db5ad949c825cbcbf6eb7c48b5a"
    timeout_seconds: float = 120
    max_article_chars: int = 500_000
    match_margin: float = 0.5
    max_iterations: int = 5

    def evidence_storage(self) -> tuple[str | Path, dict[str, str]]:
        if not self.lancedb_uri:
            return self.data_dir / "lancedb", {}
        parsed = urlsplit(self.lancedb_uri)
        if not parsed.scheme:
            return Path(self.lancedb_uri), {}
        if (
            parsed.scheme != "az"
            or not parsed.netloc
            or parsed.username
            or parsed.password
            or parsed.port
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError("LanceDB URI must be a local path or az://container/path without credentials")
        if not self.azure_storage_account_name or not self.azure_storage_account_key:
            raise ValueError("Azure Blob storage requires the configured storage account name and key")
        return self.lancedb_uri, {
            "account_name": self.azure_storage_account_name,
            "account_key": self.azure_storage_account_key,
        }

    @classmethod
    def from_env(cls, path: str | None = ".env") -> Config:
        if path:
            load_dotenv(path, override=False)
        values = {}
        for name, descriptor in cls.__dataclass_fields__.items():
            key = "TOMI_" + name.upper()
            raw = os.environ.get(key)
            if raw is None:
                continue
            default = descriptor.default
            values[name] = type(default)(raw) if not isinstance(default, Path) else Path(raw)
        config = cls(**values)
        for url in (config.core_url, config.wikipedia_url, config.dataset_base_url):
            parsed = urlsplit(url)
            if parsed.scheme not in {"https", "http"} or not parsed.netloc or parsed.username:
                raise ValueError("Service URLs must be HTTP(S) URLs without credentials")
            if parsed.query or parsed.fragment:
                raise ValueError("Service base URLs cannot contain queries or fragments")
        return config
