---
id: demo-narration-en
topic: demo-narration
lang: en
title: "Tomi narration: three-minute submission and extended interview"
type: guide
status: evidence-draft
updated: "2026-10-18"
tags: [tomi, submission, evidence, en]
---

[EN](demo-narration-en.md) · [ES](demo-narration-es.md) · [DE](demo-narration-de.md) · [FR](demo-narration-fr.md)

> Publication status: the final submission video is pending. Automatic transcription of the source MOV completed (46 chunks, 87 segments); listening and fidelity review remain incomplete. Existing interim video duration does not certify final publication.

# Tomi

## Three-minute submission narration

Tomi connects historical Encyclopaedia Britannica with Wikipedia and shows what supports each comparison.

We selected one hundred pages reproducibly and checked every image hash. All received real Nemotron Parse calls. Ninety-eight full-page responses were accepted, including three blank leaves; one astronomy plate remains partial and one cover has no usable prose. Accepted OCR is not perfect transcription.

All four required NVIDIA models now run. Embed and Rerank use the assigned Nebius GPU. LanceDB stores and searches vectors. Nemotron Super VL operates our Hermes evidence tool through the Rust core gateway.

Here are three narrow, source-supported results. Historical shelf-pieces are made of timber, while the modern text defines a shipyard. Both sources associate the litre with a cubic decimetre. The bleaching example contrasts historical discussion of vessels and gas with the modern purpose of removing colour.

Our first broad versions failed. Search retrieved shipbuilding companies, measurement policy displaced unit definitions, and noisy bleaching OCR could not support a full process comparison. Those actual failures remain beside the successful narrow questions.

Hermes selects only offered evidence spans. The server binds them to exact quotes and Unicode offsets. Invalid citations fail validation. A valid citation still needs a source-support review; it does not make a claim true automatically.

All 100 original pages are accounted for. Real semantic retrieval completed for 96 text-bearing or partial pages:23 candidate outcomes and 73 ambiguous outcomes. Three blank leaves and one nontext cover remain unmatched; the partial astronomy plate is included among the 96. Original transport failures and targeted retries are preserved. These counts are not measured matching accuracy.

The compiled archive contains all hundred source documents across 187 PDF pages. Our multilingual application shows sources and tool activity; public tests verified streaming, steering, cancellation and stored events.

Tomi makes useful answers inspectable—and preserves the reasons an answer fails.

## Extended interview narration

Tomi is a workspace for comparing historical Encyclopaedia Britannica with Wikipedia. Its purpose is to make evidence and uncertainty inspectable, rather than treating a fluent answer as sufficient proof.

We selected one hundred historical pages with a reproducible manifest and checked their image hashes. Every image received a real Nemotron Parse 3.5 call. Ninety-eight full-page outputs were accepted without truncation, including three blank leaves containing only layout controls. An astronomy plate required crops and remains partial. One cover contains no usable prose. We retain all hundred identities and every failed attempt. These are extraction outcomes, not certified OCR accuracy.

The required pipeline now uses all four NVIDIA models. Candidate articles come from the organizer's pinned Wikimedia snapshot with complete text, revision metadata and checked hashes. Nemotron Embed represents the content; LanceDB stores and searches the vectors; Nemotron Rerank scores candidate relevance. Both retrieval models run on our assigned Nebius GPU. Nemotron Super VL powers the actual Hermes evidence tool through our Rust gateway. Provider credentials remain inside core.

Three narrow comparisons have passed an assistant review against their cited sources. The shipbuilding case contrasts historical shelf-pieces made of timber with the modern definition of a shipyard. The measurement case finds the litre associated with a cubic decimetre in both texts. Its prose normalizes the typography of the cubic symbol; its raw citations stay exact. The bleaching case compares historical discussion of vessels and gas with the modern purpose of removing colour. These are limited observations, not broad claims of scientific progress.

The earlier broad versions failed. Our first shipbuilding search favored companies over the main article. Measurement candidates discussed metrication policy instead of unit definitions. Corrupt bleaching OCR did not support a full comparison of techniques. We preserve these genuine failures and the later narrow questions, with explicit discovery topics and model traces. A separate human certification has not been claimed.

We also reproduced citation-copy errors. The repaired Hermes tool now offers immutable span identifiers. Super VL selects those identifiers; the server resolves each to its exact source quote and Unicode offsets, then runs the same strict validator. Unknown identifiers, quotation overrides and one-corpus references fail. A structurally valid citation still needs an entailment review. The original question remains separate from the discovery query so retrieval does not erase the user's requested scope.

All 100 original pages are accounted for. Real semantic retrieval completed for 96 text-bearing or partial pages:23 candidate outcomes and 73 ambiguous outcomes. Three blank leaves and one nontext cover remain unmatched; the partial astronomy plate is included among the 96. Original transport failures and targeted retries are preserved. These counts are not measured matching accuracy. Relevance logits are not probabilities of truth, and we do not have a labelled-set accuracy estimate. Vocabulary overlap and normalized frequencies help describe the texts, but OCR noise and unequal article coverage limit interpretation.

The archive has compiled PDFs for all hundred source documents, totaling 187 pages, alongside editable LaTeX and a static viewer. The application supports English, Spanish, German and French. Public tests verified streaming, steering, cancellation, stored conversation events and logout. Image generation and realtime session issuance were also tested; physical microphone use and playback were not.

Six application services run on Azure, with only the web service public. Native Azure Blob storage supports LanceDB writes. Outstanding engineering limits include the database's administrative runtime role and broad-question reliability. The result is a working, inspectable comparison workflow with preserved successes and failures—not a claim that every source can be matched or every question answered.

## Production and evidence limits

The participant PDF requires three minutes. Measure the final rendered duration; word counts are not playback evidence. The English extended script stays below600words. The current model evidence is actual; sample-wide matching is complete with explicit ambiguity. The six-case review is by the assistant, with independent human certification pending. Public deployment and public NVIDIA path acceptance are separate checks. No submission receipt, award or physical audio fidelity is claimed.

[submission-guide-en](submission-guide-en.md) · [interview-preparation-en](interview-preparation-en.md)

`Hermes/evidence/reviewed-six-cases.json` · `Hermes/evidence/live-nemotron-matching-20261018T1742Z/progress.json` · `Hermes/archive/assets/compile-receipt.json`

Final semantic classification:95 full-text Parse pages,1 partial astronomy plate(row2243),3 blank leaves(rows374,1615,2077) and1 nontext cover(row452)=100 original pages. All three blank images were visually inspected. The98 accepted nontruncated Parse responses include those3 layout-only blanks; acceptance is not usable prose or OCR accuracy. Original receipts remain unchanged. `Hermes/evidence/page-content-classification.json` contains all100 identities and hashes.


All 100 original pages are accounted for. Real semantic retrieval completed for 96 text-bearing or partial pages:23 candidate outcomes and 73 ambiguous outcomes. Three blank leaves and one nontext cover remain unmatched; the partial astronomy plate is included among the 96. Original transport failures and targeted retries are preserved. These counts are not measured matching accuracy.

`Hermes/evidence/100-page-semantic-summary.json` · `Hermes/evidence/100-page-semantic-ledger.csv` · `Hermes/evidence/page-content-classification.json`

[Documentation index](README.md) · [Setup instructions](../../README.md) · [Source and export review](source-review.json)
