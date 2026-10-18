---
id: comparison-analysis-en
topic: comparison-analysis
lang: en
title: "Vocabulary analysis of three actual comparisons"
type: analysis
status: evidence-reviewed
updated: "2026-10-18"
tags: [tomi, comparison, evidence, en]
---

[EN](comparison-analysis-en.md) · [ES](comparison-analysis-es.md) · [DE](comparison-analysis-de.md) · [FR](comparison-analysis-fr.md)

> Publication status: the final submission video is pending. Automatic transcription of the source MOV completed (46 chunks, 87 segments); listening and fidelity review remain incomplete. Existing interim video duration does not certify final publication.

# Vocabulary analysis of three actual comparisons

These measurements use the complete historical page and the complete modern article actually cited in each narrow successful comparison. They are descriptive measurements, not a model score or matching-accuracy estimate. The comparisons have an assistant source-entailment review; independent human certification is pending.

| Historical row | Modern article | Historical words | Modern words | Jaccard | Jensen–Shannon |
|---|---|---:|---:|---:|---:|
| 13 | Shipbuilding | 1419 | 5593 | 0.109744 | 0.472972 |
| 104 | Litre | 1460 | 1903 | 0.118505 | 0.514112 |
| 115 | Textile bleaching | 1220 | 1145 | 0.096398 | 0.546280 |

The tokenizer removes Parse layout control tokens, casefolds text and counts Unicode-letter runs. It keeps stopwords and does not repair OCR, stem words or normalize historical spelling. Jaccard measures shared vocabulary divided by the vocabulary union. Jensen–Shannon divergence uses normalized frequencies and base2 logarithms; it is bounded from0 to1 for this implementation.

| Historical row | Word | Historical count / per1000 | Modern count / per1000 |
|---|---|---:|---:|
| 13 | `timber` | 2 / 1.409 | 4 / 0.715 |
| 13 | `ship` | 12 / 8.457 | 35 / 6.258 |
| 13 | `shipbuilding` | 0 / 0.000 | 41 / 7.331 |
| 104 | `litre` | 2 / 1.370 | 39 / 20.494 |
| 104 | `cubic` | 5 / 3.425 | 19 / 9.984 |
| 104 | `brit` | 33 / 22.603 | 0 / 0.000 |
| 115 | `veffel` | 4 / 3.279 | 0 / 0.000 |
| 115 | `gas` | 3 / 2.459 | 0 / 0.000 |
| 115 | `bleaching` | 2 / 1.639 | 37 / 32.314 |

## Interpretation
Shipbuilding compares timber shelf-pieces with the definition of a shipyard, not a proven historical transition. The modern article is nearly four times longer, so raw counts differ for reasons beyond vocabulary change. Litre establishes limited terminology continuity; corrupted historical conversion figures were not adopted. Bleaching compares topic coverage. The OCR token veffel is retained as observed and must not be treated as verified historical spelling. Common function words dominate top frequencies, and low overlap does not establish new knowledge.

## Exact source support
The rows below identify raw Unicode spans, source revisions and original run receipts. Full citation objects and text hashes are in comparison-analysis.json. The three original broad-question failures remain in reviewed-six-cases.json. BERTopic was not run; no causal change, full-page agreement or calibrated probability is claimed.

| Source | Span | Revision | Link |
|---|---|---|---|
| britannica:309f765b1ecc83e0a7f7762e44b4a927a7555443:train:13 | 1720:2520 | 309f765b1ecc83e0a7f7762e44b4a927a7555443 | [source](https://huggingface.co/datasets/NationalLibraryOfScotland/encyclopaedia_britannica_illustrated/tree/309f765b1ecc83e0a7f7762e44b4a927a7555443) |
| wikipedia:187377 | 0:800 | 1348971360 | [source](https://en.wikipedia.org/w/index.php?oldid=1348971360) |
| britannica:309f765b1ecc83e0a7f7762e44b4a927a7555443:train:104 | 157:485 | 309f765b1ecc83e0a7f7762e44b4a927a7555443 | [source](https://huggingface.co/datasets/NationalLibraryOfScotland/encyclopaedia_britannica_illustrated/tree/309f765b1ecc83e0a7f7762e44b4a927a7555443) |
| wikipedia:18094 | 0:800 | 1341552788 | [source](https://en.wikipedia.org/w/index.php?oldid=1341552788) |
| britannica:309f765b1ecc83e0a7f7762e44b4a927a7555443:train:115 | 537:863 | 309f765b1ecc83e0a7f7762e44b4a927a7555443 | [source](https://huggingface.co/datasets/NationalLibraryOfScotland/encyclopaedia_britannica_illustrated/tree/309f765b1ecc83e0a7f7762e44b4a927a7555443) |
| wikipedia:11501704 | 0:800 | 1338304831 | [source](https://en.wikipedia.org/w/index.php?oldid=1338304831) |

`tomi-ai-hermes/evidence/comparison-analysis.json` · `tomi-ai-hermes/evidence/reviewed-six-cases.json`

[submission-guide-en](submission-guide-en.md)

[Documentation index](README.md) · [Setup instructions](../../README.md) · [Source and export review](source-review.json)
