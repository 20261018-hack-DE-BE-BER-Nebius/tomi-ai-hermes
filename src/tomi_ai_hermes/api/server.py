"""Authenticated internal evidence API. Health is liveness; readiness is challenge capability."""

import hmac
import importlib.util
import json
import re
from typing import Literal

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from tomi_ai_hermes.application.comparison import Comparison
from tomi_ai_hermes.application.retrieval import Pipeline
from tomi_ai_hermes.application.seed import import_seed
from tomi_ai_hermes.config import Config
from tomi_ai_hermes.domain.evidence import sha256
from tomi_ai_hermes.infrastructure.agent import HermesAgent
from tomi_ai_hermes.infrastructure.core import CoreClient
from tomi_ai_hermes.infrastructure.store import EvidenceStore
from tomi_ai_hermes.infrastructure.wikipedia import WikipediaClient


class Request(BaseModel):
    model_config = ConfigDict(extra="forbid")
    question: str = Field(min_length=1, max_length=2000)
    locale: Literal["en", "es", "de", "fr"] = "en"
    historical_page_id: str | None = Field(default=None, max_length=150)
    top_k: int = Field(default=5, ge=1, le=10)
    require_semantic: bool = False


def create_app(
    config: Config | None = None, pipeline: Pipeline | None = None, comparison: Comparison | None = None
):
    config = config or Config.from_env()
    storage_error = None
    if pipeline is None:
        try:
            store = EvidenceStore.from_config(config)
            import_seed(store, config.seed_dir)
            pipeline = Pipeline(config, CoreClient(config), WikipediaClient(config), store)
        except (OSError, RuntimeError, ValueError) as error:
            storage_error = type(error).__name__
    comparison = comparison or (Comparison(config, pipeline, HermesAgent(config)) if pipeline else None)
    app = FastAPI(title="Tomi evidence service", version="1.0.0", docs_url=None, redoc_url=None)

    def unavailable(error=None):
        nonlocal storage_error
        if error is not None:
            storage_error = type(error).__name__
        return JSONResponse(
            {
                "status": "blocked",
                "service": "tomi-ai-hermes",
                "error_code": "evidence_storage_unavailable",
                "error_type": storage_error,
                "blockers": ["Evidence storage initialization or access failed"],
            },
            status_code=503,
        )

    def authorize(authorization: str = Header(default="")):
        if not config.service_token or config.service_token == "changeme":
            raise HTTPException(503, "Internal service authentication is not configured")
        if not hmac.compare_digest(authorization, "Bearer " + config.service_token):
            raise HTTPException(401, "Invalid service credential")

    @app.get("/health")
    def health():
        if storage_error:
            return unavailable()
        return {"status": "ok", "service": "tomi-ai-hermes"}

    @app.get("/ready", dependencies=[Depends(authorize)])
    def ready():
        if storage_error:
            return unavailable()
        try:
            counts = pipeline.store.counts()
        except (OSError, RuntimeError, ValueError) as error:
            return unavailable(error)
        installed = importlib.util.find_spec("run_agent") is not None
        proof_path = config.data_dir / "readiness.json"
        verified = False
        if proof_path.exists():
            proof = json.loads(proof_path.read_text())
            run_id = proof.get("run_id", "")
            if re.fullmatch(r"[a-f0-9-]{36}", run_id):
                receipt_path = config.data_dir / "runs" / (run_id + ".json")
                verified = receipt_path.exists() and sha256(receipt_path.read_text()) == proof.get(
                    "receipt_sha256"
                )
        status = (
            "ready"
            if counts["historical_pages"] > 0 and counts["vectors"] > 0 and installed and verified
            else "blocked"
        )
        return JSONResponse(
            {
                "status": status,
                "counts": counts,
                "hermes_installed": installed,
                "inference_verified": verified,
                "message": "Run evaluation to establish model and evidence readiness.",
            },
            status_code=200 if status == "ready" else 503,
        )

    @app.post("/v1/retrieve", dependencies=[Depends(authorize)])
    def retrieve(request: Request):
        if storage_error:
            return unavailable()
        try:
            result = pipeline.retrieve(**request.model_dump())
        except (OSError, RuntimeError, ValueError) as error:
            return unavailable(error)
        return JSONResponse(result, status_code=503 if result["status"] == "blocked" else 200)

    @app.post("/v1/compare", dependencies=[Depends(authorize)])
    def compare(request: Request):
        if storage_error:
            return unavailable()
        values = request.model_dump(exclude={"require_semantic"})
        try:
            result = comparison.run(**values)
        except (OSError, RuntimeError, ValueError) as error:
            return unavailable(error)
        return JSONResponse(result, status_code=503 if result["status"] == "blocked" else 200)

    return app
