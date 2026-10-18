---
id: comparison-analysis-de
topic: comparison-analysis
lang: de
title: "Wortschatzanalyse dreier tatsächlicher Vergleiche"
type: analysis
status: evidence-reviewed
updated: "2026-10-18"
tags: [tomi, comparison, evidence, de]
---

[EN](comparison-analysis-en.md) · [ES](comparison-analysis-es.md) · [DE](comparison-analysis-de.md) · [FR](comparison-analysis-fr.md)

> Veröffentlichungsstand: Das endgültige Einreichungsvideo steht aus. Die automatische Transkription des Quell-MOV ist abgeschlossen (46 Abschnitte, 87 Segmente); Hör- und Treueprüfung bleiben unvollständig. Die Dauer der Zwischenfassung bestätigt keine finale Veröffentlichung.

# Wortschatzanalyse dreier tatsächlicher Vergleiche

Gemessen werden die vollständige historische Seite und der vollständige moderne Artikel, der im jeweiligen begrenzten erfolgreichen Vergleich zitiert wurde. Es sind deskriptive Maße, keine Modellwerte oder Zuordnungsgenauigkeit. Die Quellenstützung wurde vom Assistenten geprüft; unabhängige menschliche Zertifizierung fehlt.

| Historische Zeile | Moderner Artikel | Historische Wörter | Moderne Wörter | Jaccard | Jensen–Shannon |
|---|---|---:|---:|---:|---:|
| 13 | Shipbuilding | 1419 | 5593 | 0.109744 | 0.472972 |
| 104 | Litre | 1460 | 1903 | 0.118505 | 0.514112 |
| 115 | Textile bleaching | 1220 | 1145 | 0.096398 | 0.546280 |

Der Tokenizer entfernt Parse-Layoutsteuerzeichen, vereinheitlicht Groß-/Kleinschreibung und zählt Folgen von Unicode-Buchstaben. Stoppwörter bleiben enthalten; OCR, Wortstämme und historische Schreibungen werden nicht korrigiert. Jaccard teilt gemeinsamen Wortschatz durch die Vereinigungsmenge. Jensen–Shannon nutzt normalisierte Häufigkeiten und Logarithmen zur Basis2; hier liegt es zwischen0 und1.

| Historische Zeile | Wort | Historische Anzahl / je1000 | Moderne Anzahl / je1000 |
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

## Auslegung
Der Schiffbaufall vergleicht Holzteile mit einer Werftdefinition, keinen bewiesenen historischen Übergang. Der moderne Artikel ist fast viermal länger; Rohzahlen unterscheiden sich nicht nur wegen Wortschatzänderungen. Liter belegt begrenzte Begriffskontinuität, ohne korrupte Umrechnungen zu übernehmen. Bleiche vergleicht Themenumfang. Das OCR-Token veffel bleibt unverändert und ist keine bestätigte historische Schreibweise. Funktionswörter dominieren; geringe Überlappung beweist kein neues Wissen.

## Genaue Quellenstützung
Die Tabelle nennt Unicode-Spannen, Revisionen und ursprüngliche Laufbelege. Vollständige Zitate und Texthashes stehen in comparison-analysis.json. Die drei ursprünglichen Fehler breiter Fragen bleiben in reviewed-six-cases.json. BERTopic wurde nicht ausgeführt; keine kausale Veränderung, vollständige Übereinstimmung oder kalibrierte Wahrscheinlichkeit wird behauptet.

| Source | Span | Revision | Link |
|---|---|---|---|
| britannica:309f765b1ecc83e0a7f7762e44b4a927a7555443:train:13 | 1720:2520 | 309f765b1ecc83e0a7f7762e44b4a927a7555443 | [source](https://huggingface.co/datasets/NationalLibraryOfScotland/encyclopaedia_britannica_illustrated/tree/309f765b1ecc83e0a7f7762e44b4a927a7555443) |
| wikipedia:187377 | 0:800 | 1348971360 | [source](https://en.wikipedia.org/w/index.php?oldid=1348971360) |
| britannica:309f765b1ecc83e0a7f7762e44b4a927a7555443:train:104 | 157:485 | 309f765b1ecc83e0a7f7762e44b4a927a7555443 | [source](https://huggingface.co/datasets/NationalLibraryOfScotland/encyclopaedia_britannica_illustrated/tree/309f765b1ecc83e0a7f7762e44b4a927a7555443) |
| wikipedia:18094 | 0:800 | 1341552788 | [source](https://en.wikipedia.org/w/index.php?oldid=1341552788) |
| britannica:309f765b1ecc83e0a7f7762e44b4a927a7555443:train:115 | 537:863 | 309f765b1ecc83e0a7f7762e44b4a927a7555443 | [source](https://huggingface.co/datasets/NationalLibraryOfScotland/encyclopaedia_britannica_illustrated/tree/309f765b1ecc83e0a7f7762e44b4a927a7555443) |
| wikipedia:11501704 | 0:800 | 1338304831 | [source](https://en.wikipedia.org/w/index.php?oldid=1338304831) |

`tomi-ai-hermes/evidence/comparison-analysis.json` · `tomi-ai-hermes/evidence/reviewed-six-cases.json`

[submission-guide-de](submission-guide-de.md)

[Dokumentationsübersicht](README.md) · [Einrichtungsanleitung](../../README.md) · [Quellen- und Exportprüfung](source-review.json)
