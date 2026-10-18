# Tomi submission documents

This public folder contains exactly 16 task-created notes in English, Spanish, German and French. It provides reviewer access without requiring access to the private knowledge graph. Repository visibility has not been changed.

| Topic | English | Español | Deutsch | Français |
|---|---|---|---|---|
| Requirements and evidence checklist | [EN](submission-guide-en.md) | [ES](submission-guide-es.md) | [DE](submission-guide-de.md) | [FR](submission-guide-fr.md) |
| Short and extended narration scripts | [EN](demo-narration-en.md) | [ES](demo-narration-es.md) | [DE](demo-narration-de.md) | [FR](demo-narration-fr.md) |
| 20 interview questions and answers | [EN](interview-preparation-en.md) | [ES](interview-preparation-es.md) | [DE](interview-preparation-de.md) | [FR](interview-preparation-fr.md) |
| Source-cited vocabulary analysis | [EN](comparison-analysis-en.md) | [ES](comparison-analysis-es.md) | [DE](comparison-analysis-de.md) | [FR](comparison-analysis-fr.md) |

[Install, configure and run Hermes](../../README.md). The [video index](../../demo/README.md) maps the separate three-minute submission and under-five-minute platform walkthrough to requirements, scenes and inspectable artifacts. The current evidence is available directly in this repository:

- [Three reviewed narrow successes and three actual failures](../../evidence/reviewed-six-cases.json).
- [Complete 100-page outcome ledger](../../evidence/100-page-semantic-summary.json) and [page classification](../../evidence/page-content-classification.json).
- [Comparison metrics and exact source support](../../evidence/comparison-analysis.json).
- [Compiled 100-document archive](../../archive/pdfs/britannica-100-pages.pdf) and [compiler receipt](../../archive/assets/compile-receipt.json).
- [Public archive](https://tomi-web.graysky-dd3771ab.swedencentral.azurecontainerapps.io/archive/) and [recorded-results viewer](https://tomi-web.graysky-dd3771ab.swedencentral.azurecontainerapps.io/archive/results.html).
- [Source-review and export receipt](source-review.json), including the official requirement sources and original/exported note hashes.

The sample contains 95 full-text pages, one partial plate, three blank leaves and one cover. Semantic retrieval produced 23 candidate and 73 ambiguous outcomes for 96 textual/partial pages. These are not measured matching accuracy. Three narrow comparisons have assistant source-support reviews; independent human certification remains pending. Original failed runs are preserved. The [public Nemotron route](../../demo/public-workspace-acceptance.json) completed with seven sources and an explicit `needs_review` warning; the UI restored the same answer after a canvas reload. Public batch diarization is also verified on an official 30-second sample, yielding six segments and five anonymous labels in 34.29 seconds. It is an additional fifth model, not one of the four required challenge models; physical microphone, playback and end-to-end realtime conversation remain unverified.

The [final submission cut](../../demo/tomi-submission-3min.mp4) is locally verified at **180.000 seconds**; the [platform walkthrough](../../demo/tomi-platform-walkthrough.mp4) is **279.722656 seconds**. Both file hashes match their successful full-decode receipts. [Hashes, narration, captions, timelines and coverage](../../demo/README.md) are available locally. The files are included in this repository; independent visual and technical QA passed and portal submission has not been performed. Automatic transcription of the supplied source MOV completed with 46 chunks and 87 segments, but listening/fidelity review remains incomplete. No audio-reviewed transcript, submitted-form receipt or extension to the published deadline is claimed.

These are reviewed public copies. The source receipt records removal of superseded interim page accounting, conversion of private-vault links, removal of local absolute-path links, and the verified ASR-status update. Historical model/source receipts and private notes were not rewritten. No credentials, unrelated vault notes or raw media were exported.
