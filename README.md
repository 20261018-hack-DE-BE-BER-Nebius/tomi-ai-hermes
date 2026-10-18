# Tomi AI Hermes

Python 3.14 and UV service for pinned Britannica/Wikimedia evidence, Nemotron parsing, embedding and reranking through Tomi AI core, LanceDB, and a pinned Hermes comparison agent.

## Submission entry point

This repository contains the comparison pipeline and its reproducible evidence. The live application is at <https://tomi-web.graysky-dd3771ab.swedencentral.azurecontainerapps.io>, with a [public archive](https://tomi-web.graysky-dd3771ab.swedencentral.azurecontainerapps.io/archive/) and [recorded results](https://tomi-web.graysky-dd3771ab.swedencentral.azurecontainerapps.io/archive/results.html); its source is the sibling [tomi-web repository](https://github.com/20261018-hack-DE-BE-BER-Nebius/tomi-web).

| Deliverable | Location |
| --- | --- |
| Setup and provider configuration | This README, [.env.example](.env.example), and [AI Core](https://github.com/20261018-hack-DE-BE-BER-Nebius/tomi-ai-core) |
| Reproducible 100-page selection | [Pinned manifest](resources/upstream/britannica-manifest.json): 100 of 2,573 rows, random without replacement, seed 20261016 |
| Source text, versions and parser receipts | [Portable corpus](resources/corpus/) and [extraction evidence](evidence/) |
| Static website and compiled LaTeX | [Archive](archive/), [100-page compiled volume](archive/pdfs/britannica-100-pages.pdf), and [LaTeX source](archive/latex/main.tex) |
| Per-page comparison analysis | The `match` command writes a 100-page coverage ledger; inspect the saved [evidence](evidence/) and its explicit review state |
| Three reviewed narrow successes and three actual failures | [Reviewed cases](evidence/reviewed-six-cases.json), [explicit questions](evidence/narrow-evaluation-cases.json), and preserved earlier [run evidence](evidence/); assistant review is separate from independent human certification |
| Architecture, pitch and interview preparation | [Public four-language submission documentation](docs/submission/README.md) |
| Submission video and platform walkthrough | [Locally verified videos and coverage mapping](demo/README.md): three-minute submission (180.000 s) and platform walkthrough (279.722656 s); files included in this repository |

The NVIDIA route uses Parse 3.5, Embed VL, Rerank VL and Super VL with Hermes. A separate Astra lexical baseline is explicitly labelled in the application. Model access, an actual inference response, a reviewed comparison, and completion of the whole sample are separate checks; consult the saved receipts for their current status.

All four required models have now produced real outputs through core. The [public Nemotron route](demo/public-workspace-acceptance.json) completed with seven sources and retains an explicit review-required warning; completion does not certify the meaning of every claim. The optional fifth NVIDIA model supplies batch anonymous speaker separation, distinct from the four required challenge models. The reviewed narrow comparisons cover timber shelf-pieces versus shipyard definitions, litre/cubic-decimetre continuity, and bleaching coverage. The earlier broad questions failed and remain available. The [content classification](evidence/page-content-classification.json) accounts for 95 full-text pages, one partial astronomy plate, three visually confirmed blank leaves and one nontext cover. The original 98 accepted nontruncated Parse responses include those three layout-only blanks; acceptance is not certified OCR accuracy.

Hermes calls one read-only evidence tool. The model selects offered span IDs, which are bound to immutable quotes and Unicode offsets before the existing strict source validator runs. Mechanical citation validity does not establish claim entailment. Model-input normalization removes Parse layout controls without changing raw source text, hashes or citation offsets.

The specific participant PDF’s three-minute cut is [tomi-submission-3min.mp4](demo/tomi-submission-3min.mp4), measured at **180.000 seconds**. The separate user-requested [platform walkthrough](demo/tomi-platform-walkthrough.mp4) is **279.722656 seconds**, under five minutes. Both copied files match their recorded SHA-256 values and have successful full-decode receipts. See the [video index](demo/README.md) for hashes, narration, captions, timelines and requirement coverage. Independent visual and technical QA passed; listening and intelligibility remain unverified. Portal submission has not been performed; repository contents do not establish acceptance.

## Install and run

```sh
cp .env.example .env
uv sync --frozen
./scripts/install-hermes.sh
.venv/bin/tomi-ai-hermes serve
```

Set `TOMI_CORE_URL` to the AI-core HTTP base URL. `TOMI_CORE_TOKEN` and `TOMI_SERVICE_TOKEN` are internal service credentials. Keep upstream provider keys exclusively in AI core. Hermes intentionally rejects wheel builds; the installer uses its supported editable checkout pinned to `d923a5eb487a17c0a68801bba9ef0f56c81040a8` (v0.22.2). Run `.venv/bin/...` after installation: a subsequent plain `uv sync` removes runtime-only Hermes packages, so rerun the installer after syncing.

All service configuration is defined in `.env.example`. Configure required model endpoints in AI core and use `nemotron-parse-3.5` as the gateway alias. The bundled public-source corpus imports into an empty local LanceDB store after checksum verification. All source revisions, attribution and parser receipts are preserved.

For Azure deployment, keep `TOMI_DATA_DIR=/data` for receipts and JSON on the persistent file share, but set `TOMI_LANCEDB_URI=az://lancedb/tomi` for native Blob storage. Azure Files/SMB does not support Lance's required safe atomic commits. Set `TOMI_AZURE_STORAGE_ACCOUNT_NAME` and `TOMI_AZURE_STORAGE_ACCOUNT_KEY` from the Hermes service's own Key Vault. The storage account key is separate from inference-provider credentials and is never sent to the agent subprocess. Leave the URI empty for the existing local `TOMI_DATA_DIR/lancedb` default. Shared-key Blob authentication is implemented; Container Apps managed-identity authentication is not asserted. No unsafe commit option or filesystem fallback is enabled. The verified portable seed is written in one atomic document-table batch.

Primary storage contract: <https://github.com/lancedb/lance/blob/main/docs/src/guide/object_store.md#azure-blob-storage-configuration>. LanceDB receives native `az://container/path` plus `storage_options.account_name` and `storage_options.account_key`; URI credentials, query strings, and unsupported remote schemes are rejected.

## Data commands

```sh
.venv/bin/tomi-ai-hermes manifest
.venv/bin/tomi-ai-hermes extract --parquet data/britannica.parquet --output evidence/extraction.json
.venv/bin/tomi-ai-hermes ingest --limit 100 --output evidence/parse.json
.venv/bin/tomi-ai-hermes evaluate --output evidence/evaluation.json
```

`extract` requires the Parquet whose URL, bytes and SHA-256 are in `resources/upstream/britannica-manifest.json`. The immutable manifest selects 100 physical pages from 2,573 rows using seed 20261016. Corpus downloads and bulk inference are explicit operations. `evaluate` performs three intended positive cases and three intended negative cases and records actual outcomes.

Reproduce the narrow reviewed questions with a fresh output directory:

```sh
.venv/bin/python evidence/run-live-evaluation.py cases --cases evidence/narrow-evaluation-cases.json --output /tmp/tomi-new-cases
.venv/bin/python evidence/run-live-evaluation.py sample --output /tmp/tomi-new-sample
```

The runners execute sequentially because both retrieval models share one GPU. Output directories must not already exist. Original transport failures, source-query failures and repaired runs are retained separately; no synthetic success or accuracy score is inserted.

## HTTP interface

`GET /health` is unauthenticated process health and returns 503 after a known storage/seed initialization or access failure. Errors expose only a bounded classification, never storage credentials or the upstream error body. `GET /ready`, `POST /v1/retrieve` and `POST /v1/compare` require `Authorization: Bearer <TOMI_SERVICE_TOKEN>`.

Requests contain `question`, `locale` (`en`, `es`, `de`, `fr`), optional `historical_page_id`, `top_k` (1–10), and `require_semantic`. Retrieval may return a clearly labeled lexical baseline with `status: partial`; comparison requires the complete Nemotron/Hermes route. Source documents, traces, model failures, uncertainty, exact citation spans and receipt hashes accompany results. `/ready` is distinct from process health.

`POST /v1/compare` additionally accepts optional `discovery_query` (1–512 characters). It is used only to discover source candidates; the original `question` remains the synthesis request. This preserves a user's narrow comparison scope after a gateway resolves the search topic. `/v1/retrieve` does not accept this field.

## Containers and checks

```sh
container build -t tomi-ai-hermes:dev .
# Or on a Docker development host:
docker compose up --build
.venv/bin/pytest -q
.venv/bin/ruff check src tests
gitleaks dir . --redact --no-banner
```

`docker-compose.yml` is for local development only; production uses Azure Container Apps. Build context is this repository. Persist `/data`; the image contains the portable public corpus, not a prebuilt vector index. The NVIDIA GPU retrieval container runs on Nebius Linux GPU infrastructure; Apple Container runs the application service.

Install the local pre-commit hook with `pre-commit install`. The hook requires `gitleaks` and scans staged changes with redacted output. The optional `scripts/prepare-retrieval-source.sh`, `scripts/build-retrieval-models.sh` and `scripts/run-retrieval-models.sh` prepare and run the exact organizer recipe on Linux GPU infrastructure; they do not provision cloud resources.
