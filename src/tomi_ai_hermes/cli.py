"""Operations are explicit: serving never downloads corpora or triggers bulk inference."""

import argparse
import json
from pathlib import Path

import uvicorn

from tomi_ai_hermes.application.ingest import extract_pages, ingest_pages, read_manifest
from tomi_ai_hermes.config import Config
from tomi_ai_hermes.infrastructure.core import CoreClient
from tomi_ai_hermes.infrastructure.store import EvidenceStore


def main():
    parser = argparse.ArgumentParser(description="Tomi challenge pipeline")
    parser.add_argument("command", choices=["serve", "manifest", "extract", "ingest", "evaluate", "match"])
    parser.add_argument("--parquet", type=Path)
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    config = Config.from_env()
    if args.command == "serve":
        from tomi_ai_hermes.api.server import create_app

        uvicorn.run(create_app(config), host=config.host, port=config.port, access_log=False)
        return
    result = execute(args, config)
    serialized = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized)
    print(serialized)


def execute(args, config):
    if args.command == "manifest":
        manifest = read_manifest(config.manifest_path)
        return {
            "pages": len(manifest["pages"]),
            "selection": manifest["selection"],
            "revision": manifest["revision"],
        }
    if args.command == "extract":
        if args.parquet is None:
            raise ValueError("extract requires --parquet")
        return extract_pages(config, args.parquet)
    store = EvidenceStore.from_config(config)
    if args.command == "ingest":
        if not 1 <= args.limit <= 100:
            raise ValueError("--limit must be between 1 and 100")
        return ingest_pages(config, CoreClient(config), store, args.limit)
    if args.command == "match":
        from tomi_ai_hermes.application.batch import match_sample

        return match_sample(config, store)
    from tomi_ai_hermes.application.evaluation import evaluate

    return evaluate(config, store)
