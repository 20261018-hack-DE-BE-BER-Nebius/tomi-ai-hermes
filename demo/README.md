# Tomi demonstration videos

**Status: final files included in this repository and locally verified.** Both MP4s and their narration, captions, scene timelines and verification receipts are present. Their actual file hashes match the copied receipts, which record successful full decoding. Independent visual and technical QA passed. Listening, intelligibility and pronunciation were not certified; these checks do not establish factual support.

| Cut | Local file | Measured duration | Requirement | Verification |
|---|---|---:|---|---|
| Challenge submission | [tomi-submission-3min.mp4](tomi-submission-3min.mp4) | **180.000 seconds** | The specific participant PDF requires three minutes. | [Receipt](tomi-submission-3min-verification.json) |
| Full platform walkthrough | [tomi-platform-walkthrough.mp4](tomi-platform-walkthrough.mp4) | **279.722656 seconds** (4:39.723) | Under the user’s five-minute limit of 300 seconds. | [Receipt](tomi-platform-walkthrough-verification.json) |

| File | Bytes | Verified SHA-256 |
|---|---:|---|
| `tomi-submission-3min.mp4` | 7,447,272 | `90defe04b5fb1db0e609d2d5cdb8f692c07a23899b7cd30160b24b961c442442` |
| `tomi-platform-walkthrough.mp4` | 11,292,364 | `4e8738ae4caacfe8d681cce64d96e8c9fd0efdd9f9cdfefb7099516b5a9103e1` |

These are separate deliverables. The longer walkthrough does not replace the PDF’s three-minute submission. Both receipts identify 1920×1080 H.264 video, AAC audio and the synthetic macOS Daniel English narration. The replacement renders apply per-scene loudness normalization followed by 5 dB attenuation for AAC headroom. Caption timing uses phrase-level estimates within measured scene audio. Listening and speech-intelligibility review were not performed. Portal submission has not been performed.

## Requirement-to-video and artifact coverage

Scene IDs refer to the copied render timelines. `S` identifies the submission cut; `W` identifies the walkthrough. The mapping describes the recorded scene script and supporting artifacts. Independent visual and technical QA passed; a scene or completed decode does not prove that every narrated interaction was exercised.

| Requirement or capability | Submission scenes | Walkthrough scenes | Inspectable artifact |
|---|---|---|---|
| Problem and research workflow | S1, S8 | W1, W5–W7 | [Setup and application entry](../README.md), [actual public workspace receipt](public-workspace-acceptance.json) |
| Reproducible 100-page sample and actual Parse calls | S2 | W2 | [Pinned manifest](../resources/upstream/britannica-manifest.json), [source classification](../evidence/page-content-classification.json), [portable source/Parse receipts](../resources/corpus/) |
| Parse, Embed, Rerank and Super VL with Hermes | S3, S6 | W4–W6 | [Actual cases and receipt references](../evidence/reviewed-six-cases.json) |
| Three narrow supported comparisons | S4 | W8 | [Reviewed cases](../evidence/reviewed-six-cases.json), [explicit questions](../evidence/narrow-evaluation-cases.json) |
| Three actual failed broad comparisons | S5 | W9 | [Preserved failures](../evidence/reviewed-six-cases.json) |
| Evidence tool and immutable citation binding | S6 | W6 | [Comparison implementation](../src/tomi_ai_hermes/application/comparison.py), [strict answer validation](../src/tomi_ai_hermes/domain/answers.py) |
| All-page matching outcomes and uncertainty | S7 | W10 | [100-page ledger](../evidence/100-page-semantic-summary.json), [CSV](../evidence/100-page-semantic-ledger.csv) |
| Vocabulary and source-supported comparison analysis | S7 | W10 | [Analysis](../evidence/comparison-analysis.md), [metrics and citations](../evidence/comparison-analysis.json) |
| Static scans, editable LaTeX and compiled PDFs | S7 | W3 | [Archive](../archive/), [compiled volume](../archive/pdfs/britannica-100-pages.pdf), [compiler receipt](../archive/assets/compile-receipt.json) |
| Model selection, streaming, sources and tool traces | S8, brief overview | W1, W5, W6 | Rendered scene metadata is present; independent visual and technical QA passed. Source/case receipts remain independently inspectable. |
| Canvas, 3D graph, saved history, export, steering and cancellation | S8, brief overview | W7 | Rendered scene metadata is present; no claim that every interaction was demonstrated by a static frame. |
| Image generation | Outside the short cut’s recorded scene list | W11 | Independent walkthrough visual and technical QA passed; generated illustrations are separate from historical evidence. |
| Batch speaker separation and realtime boundary | Outside the short cut’s recorded scene list | W12 | Independent walkthrough visual and technical QA passed; no identity recognition or physical microphone/playback demonstration is claimed. |
| Pitch deck, architecture and repository handoff | S8 | W13 | [Documentation index](../docs/submission/README.md), [setup](../README.md) |

The challenge evidence accounts for 95 full-text pages, one partial plate, three blank leaves and one cover. Semantic retrieval yielded 23 candidate and 73 ambiguous outcomes across 96 textual/partial pages. Three narrow successes were reviewed against their sources by the assistant; independent human certification remains pending. Neither the video nor those selected examples establishes general matching accuracy.

## Full platform scene timeline

| Scene | Start | Scripted content |
|---|---|---|
| W1 — A workspace for evidence | 00:00.000 | Public web entry, model selection, EN/ES/DE/FR, themes and anonymous demo session. |
| W2 — A reproducible sample | 00:18.207 | Fixed selection, hashes, real Parse receipts, blank/cover/partial-page exceptions. |
| W3 — From scans to documents | 00:39.847 | Original scan, individual PDFs, combined volume and editable LaTeX. |
| W4 — Four required models | 01:01.300 | Model roles, Nebius retrieval GPU, Token Factory, core credential boundary and native Blob/LanceDB storage. |
| W5 — Ask with a clear subject | 01:26.980 | Narrow Nemotron comparison, original question versus discovery topic, streaming progress and review state. |
| W6 — Follow the evidence | 01:45.792 | Historical/modern source cards, revisions, traces, offered spans and citation validation. |
| W7 — Explore the workspace | 02:05.474 | Canvas, 3D graph, history/reload, export, steering and cancellation. |
| W8 — Three narrow successes | 02:26.874 | Shipbuilding, litre and textile-bleaching comparisons with the scope of source review. |
| W9 — Three clear failures | 02:48.640 | Candidate mismatch, policy-versus-definition mismatch and OCR limitations. |
| W10 — The full sample ledger | 03:09.899 | 96 semantic outcomes, 23 candidates, 73 ambiguous results, four unmatched nontext pages and comparison metrics. |
| W11 — Visual creation | 03:35.142 | Generated ship illustration, labelled as generated content. |
| W12 — The fifth NVIDIA model | 03:50.905 | Scripted view of batch anonymous speaker segments; realtime issuance and physical-audio limits stay explicit. |
| W13 — An inspectable handoff | 04:14.912 | Pitch deck, editable Mermaid, architecture and artifact/repository access. |

The copied timeline records both single captures and multi-capture montages, including the third failure in both cuts and language, source-activity and canvas views in the walkthrough. This timeline follows the copied scene metadata; see [walkthrough timeline](tomi-platform-walkthrough-timeline.json) and [submission timeline](tomi-submission-3min-timeline.json). OpenClaw/Covenant has no dedicated scene in those records, and no additional standalone agent demonstration is implied. Physical microphone use, playback and an end-to-end realtime voice conversation are outside the current demonstrated-video claim.

## Independent review result

The [independent review](independent-qa.json) passed for these exact hashes. Both files passed full decoding, stream/size/hash checks and numeric audio measurements. The measured audio peaks are **−3.662232 dBFS** for the walkthrough and **−4.485327 dBFS** for the submission cut. All 33 montage captures and both closing frames were reviewed; the final architecture scene was additionally checked at its start, middle and end. The third failure is visible in both videos, and the incorrect model-catalog crop was removed.

This is visual and technical verification. No listening, speech intelligibility, pronunciation or auditory synchronization certification was performed. Speaker analysis shown in progress immediately before its completed result is an intentional flow step.

## Included video package

| Cut | Narration | Captions | Timeline | Verification |
|---|---|---|---|---|
| Walkthrough | [Text](tomi-platform-walkthrough-narration.txt) | [SRT](tomi-platform-walkthrough.srt) | [Scenes](tomi-platform-walkthrough-timeline.json) | [JSON](tomi-platform-walkthrough-verification.json) |
| Submission | [Text](tomi-submission-3min-narration.txt) | [SRT](tomi-submission-3min.srt) | [Scenes](tomi-submission-3min-timeline.json) | [JSON](tomi-submission-3min-verification.json) |

The locally verified files and their sidecars are included in this repository. Git publication verification is tracked separately in the release evidence. The source MOV’s automatic transcription completed separately; listening/fidelity review remains incomplete and is not a review of these final videos.

## Reviewer and setup documents

- [English interview answers](../docs/submission/interview-preparation-en.md), [Español](../docs/submission/interview-preparation-es.md), [Deutsch](../docs/submission/interview-preparation-de.md), [Français](../docs/submission/interview-preparation-fr.md).
- [Primary installation and setup instructions](../README.md), [configuration example](../.env.example), and [reviewed Hermes installer](../scripts/install-hermes.sh).
- [English submission guide](../docs/submission/submission-guide-en.md), [Español](../docs/submission/submission-guide-es.md), [Deutsch](../docs/submission/submission-guide-de.md), [Français](../docs/submission/submission-guide-fr.md).
- [Source-review receipt and original requirement sources](../docs/submission/source-review.json).
