---
id: interview-preparation-en
topic: interview-preparation
lang: en
title: "Twenty NVIDIA and Nebius interview questions with evidence-bounded answers"
type: guide
status: conditional-draft
updated: "2026-10-18"
tags: [tomi, interview, evidence, en]
---

[EN](interview-preparation-en.md) · [ES](interview-preparation-es.md) · [DE](interview-preparation-de.md) · [FR](interview-preparation-fr.md)

> Publication status: the final submission video is pending. Automatic transcription of the source MOV completed (46 chunks, 87 segments); listening and fidelity review remain incomplete. Existing interim video duration does not certify final publication.

# Interview preparation

These are likely questions, not an organizer-provided interview. Answers use the verified baseline and must be refreshed from receipts when pending work completes. [submission-guide-en](submission-guide-en.md) defines the requirements; implementation delivery en links the actual application evidence.

1. **What problem does Tomi solve?** Tomi compares historical Britannica with a pinned Wikipedia snapshot. It links narrowly stated differences or continuity to inspectable source passages and records when the evidence cannot answer a broader question.

2. **What did your team build beyond the starter?** We built the Python pipeline, the Hermes evidence tool and citation binding, a Rust model gateway and backend, multilingual interfaces, a reproducible corpus and a compiled LaTeX archive. We also repaired real storage, retrieval and model-protocol failures and retained their receipts.

3. **Why use all four Nemotron models?** Parse 3.5 turns scanned pages into layout-aware text. Embed VL produces normalized 2048-dimensional representations; LanceDB searches them. Rerank VL rescores candidate relevance with raw logits. Super VL performs the Hermes tool conversation and writes comparisons. All four have real execution evidence; their roles are complementary.

4. **Why Nebius?** Nebius provides distinct services: the organizer’s shared Parse endpoint and Wikipedia index, Token Factory for Super VL, and the team’s assigned GPU for the combined Embed/Rerank container. Azure hosts the application services. These are separate deployments and credentials.

5. **How did you choose the 100 pages?** The manifest fixes 100 rows from 2,573 using random sampling without replacement and seed 20261016. It records the immutable dataset revision and every image hash. Difficult, blank and illustrated pages remain in the sample.

6. **Did all 100 pages work?** All 100 received real Parse calls. Final content accounting is 95 full-text pages,1 partial astronomy plate,3 visually confirmed blank leaves and 1 nontext cover. The 98 accepted nontruncated responses include the 3 layout-only blank outputs; acceptance never meant perfect OCR.

7. **How do you measure extraction quality?** We verify source hashes, response provenance, truncation and selected scan comparisons. Three empty normalized outputs were checked against the actual images and classified as blanks. We have not measured a complete, human-labelled character-error rate or reading-order accuracy.

8. **Why not match by title alone?** The pipeline retrieves complete articles from the organizer’s pinned snapshot, verifies hashes, removes layout control tokens only for model inputs, then uses Embed, LanceDB and Rerank. An exact-title cached article from the same verified snapshot supplements poor BM 25 recall. Raw text stays unchanged for citations.

9. **What is your matching accuracy?** We do not have a defensible labelled-set matching accuracy. Candidate scores, margins, ambiguity, source coverage and reviewed examples are reported separately. The 100-page run and transport retries retain failures instead of turning successful API responses into accuracy claims.

10. **How does LanceDB fit?** LanceDB stores the team’s source documents and model vectors. The organizer’s BM 25 index is separate. We verified native Azure Blob writes because Azure Files cannot support safe Lance commits. The early 183-document, zero-vector cloud probe is historical; later real-vector counts belong to their own run receipts.

11. **What comparisons do you compute?** We compute vocabulary Jaccard overlap, Jensen–Shannon divergence and word-frequency summaries. These describe text distributions, not historical truth. OCR noise, stopwords and unequal article length or coverage can dominate; BERTopic was optional and no run is claimed.

12. **What makes Hermes an agent here?** Hermes executes a real model-driven tool loop: Super VL calls our single read-only evidence function, receives bounded source spans and returns selected span IDs in structured claims. The tool trace is retained. The process has no shell, filesystem or browsing tools; deterministic source validation follows the agent response.

13. **How do you prevent hallucinated citations?** Only offered span IDs can be selected. The server binds them to immutable source quotes and Unicode-codepoint offsets, then applies the existing strict validator. Unknown IDs, overrides and citations from just one corpus are rejected. We separately review whether a valid span actually supports the claim.

14. **What are your failure cases?** The three selected actual failures are broad shipbuilding, measurement and bleaching questions: candidate recall, policy-versus-definition mismatch and corrupt OCR prevented useful full comparisons. We also retain missing-page, unsupported-GPS and instruction-attack runs. Later narrow successes do not erase the earlier failures.

15. **How do you handle prompt injection?** OCR and retrieved text remain untrusted data. The agent receives no provider key and has only a bounded read-only tool. Actual instruction-attack runs abstained; regression tests reject unauthorized evidence references. This is evidence of specific guards, not proof of immunity to every attack.

16. **What actually works in the public application?** The saved public baseline verified an Astra stream, seven sources, steering, cancellation, stored conversation events and logout. The four-model Hermes route has separate actual execution and reviewed-case receipts. Its public acceptance is a separate release check, not inferred from the earlier Astra result.

17. **What multimodal features have you verified?** Public endpoints returned an actual PNG and issued a realtime session. Session issuance is not microphone capture, playback or a completed voice conversation. Physical audio/video interaction and diarization are not claimed here without their separate current acceptance receipt.

18. **What is your deployment and security posture?** Six application services run on Azure and only the web is public; required retrieval inference runs on Nebius. Provider keys are confined to core. Reviewed secret scans are clean. Known limits include the administrative PostgreSQL runtime role and ephemeral Covenant history; this is not production or LTS sign-off.

19. **What would you improve next?** Priorities are independent relevance labels, OCR and entry-segmentation review, score calibration, more robust broad-question comparisons and a restricted database role. The discovered blank leaves show why transport success and usable content must be assessed separately.

20. **Is the project finished and submitted?** Three narrow cases have assistant source-support reviews and three actual failures are preserved. Sample-wide matching has a separate ledger and retry evidence; independent human certification is pending. Repository publication and a video are not submission receipts. The published deadline was 18 October 2026 at 18:30 CEST; extension and portal acceptance remain unverified.

Evidence references: `submission-guide/evidence/source-review.json`; Hermes `evidence/100-page-extraction.json`, `page-visual-review.json`, `six-case-evaluation.json`, `azure-blob-runtime-probe.json`; backend `verification/public-acceptance.json`, `public-multimodal.json`; IaC `verification/security-deployment-review.json`. All paths are relative to the repositories listed in `submission-guide/repository-map.json`. Preserve the distinction between current proof, implementation, and planned work.

`Hermes/evidence/reviewed-six-cases.json`; `Hermes/evidence/live-nemotron-matching-20261018T1742Z/progress.json`; `core/verification/nebius-model-deployment/core-retrieval-live.json`; `core/verification/nebius-model-deployment/gpu-models-live.json`.

Final semantic classification:95 full-text Parse pages,1 partial astronomy plate(row2243),3 blank leaves(rows374,1615,2077) and1 nontext cover(row452)=100 original pages. All three blank images were visually inspected. The98 accepted nontruncated Parse responses include those3 layout-only blanks; acceptance is not usable prose or OCR accuracy. Original receipts remain unchanged. `Hermes/evidence/page-content-classification.json` contains all100 identities and hashes.


All 100 original pages are accounted for. Real semantic retrieval completed for 96 text-bearing or partial pages:23 candidate outcomes and 73 ambiguous outcomes. Three blank leaves and one nontext cover remain unmatched; the partial astronomy plate is included among the 96. Original transport failures and targeted retries are preserved. These counts are not measured matching accuracy.

`Hermes/evidence/100-page-semantic-summary.json` · `Hermes/evidence/100-page-semantic-ledger.csv` · `Hermes/evidence/page-content-classification.json`

[Documentation index](README.md) · [Setup instructions](../../README.md) · [Source and export review](source-review.json)
