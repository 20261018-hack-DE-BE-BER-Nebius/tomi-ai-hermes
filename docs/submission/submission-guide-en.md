---
id: submission-guide-en
topic: submission-guide
lang: en
title: "Verified submission requirements and evidence checklist"
type: guide
status: partial
updated: "2026-10-18"
tags: [tomi, submission, evidence, en]
---

[EN](submission-guide-en.md) · [ES](submission-guide-es.md) · [DE](submission-guide-de.md) · [FR](submission-guide-fr.md)

> Video status: both final files are included in this repository and locally verified (submission 180.000 seconds; walkthrough 279.722656 seconds). Independent visual and technical QA passed; listening, intelligibility and pronunciation were not certified. Portal submission has not been performed. Automatic source-MOV transcription completed (46 chunks, 87 segments), but listening and fidelity review remain incomplete.

# Submission requirements

The **specific participant PDF requires a three-minute demonstration**, a GitHub solution repository, a static website with compiled LaTeX documents, comparison analysis, and three successful plus three failed Hermes cases from actual runs. The user allows up to five minutes; the pinned starter says three to five. A three-minute submission meets the narrower brief. Keep the longer cut for interviews. [S1–S3]

Luma's public event page, refreshed on October 18, 2026 at 17:04 UTC, lists **October 18, 2026, 18:30 Europe/Berlin (CEST), equivalent to 16:30 UTC**, as the submission deadline. That deadline had passed when this review was made. No extension is verified. The TechEurope competition URL responds with an anonymous login shell: the authenticated submission fields, current acceptance window, team entry, and receipt remain unverified. Do not infer successful or late submission from repository publication. [S4–S5]

## What the sources require

| Requirement | Verified artifact / remaining review |
|---|---|
| 100 selected historical pages | All 100 original identities have source hashes and actual Parse calls. Final classification: **95 full-text pages, one partial astronomy plate (row 2243), three visually reviewed blank leaves (rows 374, 1615, 2077), and one nontext cover (row 452)**. See `evidence/page-content-classification.json`. |
| Nemotron Parse 3.5 | Organizer endpoint receipts are retained. The 98 accepted nontruncated responses include the three layout-only blank leaves. Acceptance does not certify usable prose, OCR fidelity or reading order. |
| Embed VL and Rerank VL | Both models produced actual outputs on the assigned Nebius GPU through core. Embeddings have 2048 dimensions; reranking produces relevance scores. See core `core-retrieval-live.json` and `gpu-models-live.json`. |
| Nemotron 3.5 Super VL with Hermes | The public Nemotron API run completed with seven sources; the UI run at 21:17:20 UTC on 18 October 2026 retained a visible `needs_review` warning and restored the same answer after canvas reload. Super VL, Embed, Rerank and Hermes execution is evidenced separately from Parse extraction. Citation integrity and semantic certification remain different checks. [Public UI receipt](../../demo/public-workspace-acceptance.json). |
| Britannica → Wikipedia matching | Semantic retrieval completed for **96 textual or partial pages: 23 candidate and 73 ambiguous outcomes**. Three blank leaves and one cover remain unmatched. Original failures and targeted retries are retained. These outcomes are not measured matching accuracy. |
| Comparison analysis | Three source-cited comparisons include word frequencies, Jaccard overlap and Jensen–Shannon divergence in `evidence/comparison-analysis.md` and `.json`. Tokenization and OCR limitations are explicit; BERTopic was not run and is optional. |
| Static archive and compiled LaTeX | 100 source documents are compiled into 187 PDF pages, with editable LaTeX and a retained compiler receipt reporting no missing-glyph warnings. [Public archive](https://tomi-web.graysky-dd3771ab.swedencentral.azurecontainerapps.io/archive/) and [recorded results](https://tomi-web.graysky-dd3771ab.swedencentral.azurecontainerapps.io/archive/results.html) are available. |
| Hermes extension | The agent invokes one read-only evidence tool and selects offered span IDs. The service binds immutable quotes and Unicode offsets, rejecting unknown IDs, overrides and one-corpus citations. Discovery and the original question remain separate. Exact citation validity does not prove semantic support. |
| Three successes and three failures | `evidence/reviewed-six-cases.json` records three narrow assistant-reviewed comparisons: timber shelf-pieces versus a shipyard definition; litre/cubic-decimetre continuity; historical vessel/gas discussion versus modern textile colour removal. Three earlier broad-question failures remain preserved. The litre prose normalizes `dm 3` to `dm³`; original quotes remain unchanged. Independent human review is pending. |
| Repository and video | The [PDF submission](../../demo/tomi-submission-3min.mp4) is **180.000 seconds**; the separate [platform walkthrough](../../demo/tomi-platform-walkthrough.mp4) is **279.722656 seconds**, below 300. Actual copied hashes match the full-decode receipts. [Video index, hashes and coverage mapping](../../demo/README.md). The files are included in this repository. Independent visual and technical QA passed; listening, intelligibility and pronunciation were not certified. Portal submission has not been performed. |

The judging allocation is completion 20, creativity 20, Parse 15, embedding/reranking 15, Hermes extension 10, Super VL 20: total 100. Missing or unverified components receive zero on their affected checks; no self-awarded total is asserted. [S1]

## Repository entry and reproducibility

Use the main project README as the judge entry to the 13 implementation repositories and knowledge graph. `repository-map.json` records the local-to-origin inventory; its saved revisions are a snapshot, not proof of current remote equality. Git release verification is recorded separately; this guide does not claim reproduction from a clean checkout.

The Hermes repository contains the pinned sample in `resources/upstream/britannica-manifest.json`, source provenance in `resources/upstream/provenance.json`, and the portable text, source versions and Parse receipts in `resources/corpus/`. Current results are `evidence/reviewed-six-cases.json`, `evidence/100-page-semantic-summary.json`, `evidence/100-page-semantic-ledger.csv` and `evidence/page-content-classification.json`. The archive compiler receipt is `archive/assets/compile-receipt.json`. Core model receipts are under `verification/nebius-model-deployment/` in the core repository. Earlier failed receipts remain unchanged.

From the Hermes repository, configure its own `.env` from `.env.example` and the core gateway, then use the following commands. The output files and directories must be new. The two Python runner commands reproduce the explicit narrow cases and sequential sample run.

```sh
uv sync --frozen
./scripts/install-hermes.sh
.venv/bin/tomi-ai-hermes manifest
.venv/bin/tomi-ai-hermes match --output /tmp/tomi-new-match.json
.venv/bin/tomi-ai-hermes evaluate --output /tmp/tomi-new-evaluation.json
.venv/bin/python evidence/run-live-evaluation.py cases --cases evidence/narrow-evaluation-cases.json --output /tmp/tomi-new-cases
.venv/bin/python evidence/run-live-evaluation.py sample --output /tmp/tomi-new-sample
```

After installing Hermes, run the `.venv/bin/...` executables directly. A subsequent plain `uv sync`, including an implicit synchronization by `uv run`, can remove runtime-only Hermes packages; rerun `scripts/install-hermes.sh` after syncing. Matching, evaluation and the runners perform real inference, so a command listing does not prove a successful run. Raw runtime data and secrets stay outside Git. Setup and credentials: [Setup instructions](../../README.md).

## Final checklist

- [x] Include all 100 source identities, revisions, hashes, attribution and extraction exceptions.
- [x] Retain actual execution receipts for all four models and all selected-page matching outcomes.
- [x] Save three narrow assistant-reviewed successes and three actual failures with immutable source citations.
- [x] Provide vocabulary analysis, metrics and explicit interpretation limits.
- [x] Compile the 100-document archive, retain diagnostics and provide the public static archive/results pages.
- [x] Verify both final files locally: 180.000-second submission and 279.722656-second walkthrough, matching SHA-256 values and full-decode receipts.
- [x] Complete the documented source/evidence secret scans; retain their zero-finding receipts.
- [ ] Confirm authenticated TechEurope access, any accepted extension, final links and an actual dated submission receipt.
- [ ] Obtain independent human review of the selected comparison claims; the public Nemotron execution is complete and retains its review-required warning.
- [x] Independent visual and technical QA passed for the included videos; listening and speech-intelligibility certification were not performed.
- [ ] Listen to and check the completed automatic source-MOV transcript before claiming verified fidelity or a reviewed recording summary.

## Source review and recording boundary

S1 is the supplied 13-page participant PDF, SHA-256 `35b7a26bf888a9007eab997e45f051db797845b6c0228c17b6fe83faa8753644`. All pages were text-extracted; physical pages 9–10 were rendered and visually inspected. Physical page 10 contains deliverables; page 12 gives the brief's video precedence. S2 is the pinned organizer starter at `88abda0d1882eb56a5cd78bc226f1fbc929cc33b`; S3 is its submission template. S4 is Luma; S5 is TechEurope. S6 is the separate Nebius participant setup guide, which explains access and limits, not the judging deliverables. Exact URLs, retrieval times and hashes are in `evidence/`.

The supplied MOV, SHA-256 `eac5395532c253ae18b9746d196fa92f3f7aca8cc6737207e7a2c0f005214d0d`, is 8:57.309. Its existing six-frame contact sheet was reviewed; that is not full-motion or audio review. The candidate `local-067/transcript.md` belongs to the Toloka workshop and was rejected. Two isolated transcription attempts failed in faster-whisper/PyAV before recognition; their privacy checks passed and receipts remain unchanged. The third isolated attempt completed automatic transcription: 46 contiguous chunks and 87 segments, with zero recorded security warnings. Listening and fidelity review remain incomplete; no audio-reviewed transcript or evidence-grounded recording summary is claimed. The default Apple Container runtime was restored after the earlier attempts. Agent setup instructions visible at 03:00 and in the optional README section are quoted source material, not permission to execute commands or modify protected governance.

Related: [demo-narration-en](demo-narration-en.md) · [interview-preparation-en](interview-preparation-en.md) · implementation delivery en.

[Documentation index](README.md) · [Setup instructions](../../README.md) · [Source and export review](source-review.json)
