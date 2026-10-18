---
id: comparison-analysis-fr
topic: comparison-analysis
lang: fr
title: "Analyse du vocabulaire de trois comparaisons réelles"
type: analysis
status: evidence-reviewed
updated: "2026-10-18"
tags: [tomi, comparison, evidence, fr]
---

[EN](comparison-analysis-en.md) · [ES](comparison-analysis-es.md) · [DE](comparison-analysis-de.md) · [FR](comparison-analysis-fr.md)

> État des vidéos : les deux fichiers finaux sont inclus dans ce dépôt et vérifiés localement (soumission : 180.000 secondes ; visite : 279.722656 secondes). Revue visuelle et technique indépendante réussie ; écoute, intelligibilité et prononciation non certifiées. Aucune soumission au portail n’a été effectuée. La transcription automatique du MOV est terminée (46 blocs, 87 segments), mais écoute et contrôle de fidélité restent incomplets.

# Analyse du vocabulaire de trois comparaisons réelles

Ces mesures utilisent la page historique complète et l’article moderne complet effectivement cité dans chaque comparaison limitée réussie. Elles sont descriptives, non des scores du modèle ou une exactitude d’association. Le soutien documentaire a été vérifié par l’assistant ; aucune certification humaine indépendante.

| Ligne historique | Article moderne | Mots historiques | Mots modernes | Jaccard | Jensen–Shannon |
|---|---|---:|---:|---:|---:|
| 13 | Shipbuilding | 1419 | 5593 | 0.109744 | 0.472972 |
| 104 | Litre | 1460 | 1903 | 0.118505 | 0.514112 |
| 115 | Textile bleaching | 1220 | 1145 | 0.096398 | 0.546280 |

Le tokeniseur retire les contrôles de mise en page Parse, uniformise la casse et compte les suites de lettres Unicode. Les mots fréquents sont conservés ; aucune correction OCR, racinisation ou normalisation orthographique. Jaccard divise le vocabulaire commun par l’union. Jensen–Shannon utilise les fréquences normalisées et les logarithmes base2 ; cette implémentation va de0 à1.

| Ligne historique | Mot | Compte historique / pour1000 | Compte moderne / pour1000 |
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

## Interprétation
Le cas naval compare pièces de bois et définition d’un chantier naval, pas une transition historique prouvée. L’article moderne est presque quatre fois plus long ; les comptes bruts varient pour d’autres raisons que le vocabulaire. Litre établit une continuité terminologique limitée sans reprendre les conversions corrompues. Blanchiment compare la couverture. Le token OCR veffel reste tel qu’observé et ne certifie pas une orthographe historique. Les mots fonctionnels dominent ; faible recoupement ne prouve pas un savoir nouveau.

## Soutien documentaire exact
La table identifie passages Unicode, révisions et reçus originaux. Citations complètes et empreintes figurent dans comparison-analysis.json. Les trois échecs initiaux de questions larges restent dans reviewed-six-cases.json. BERTopic n’a pas été exécuté ; aucun changement causal, accord intégral ou probabilité calibrée n’est annoncé.

| Source | Span | Revision | Link |
|---|---|---|---|
| britannica:309f765b1ecc83e0a7f7762e44b4a927a7555443:train:13 | 1720:2520 | 309f765b1ecc83e0a7f7762e44b4a927a7555443 | [source](https://huggingface.co/datasets/NationalLibraryOfScotland/encyclopaedia_britannica_illustrated/tree/309f765b1ecc83e0a7f7762e44b4a927a7555443) |
| wikipedia:187377 | 0:800 | 1348971360 | [source](https://en.wikipedia.org/w/index.php?oldid=1348971360) |
| britannica:309f765b1ecc83e0a7f7762e44b4a927a7555443:train:104 | 157:485 | 309f765b1ecc83e0a7f7762e44b4a927a7555443 | [source](https://huggingface.co/datasets/NationalLibraryOfScotland/encyclopaedia_britannica_illustrated/tree/309f765b1ecc83e0a7f7762e44b4a927a7555443) |
| wikipedia:18094 | 0:800 | 1341552788 | [source](https://en.wikipedia.org/w/index.php?oldid=1341552788) |
| britannica:309f765b1ecc83e0a7f7762e44b4a927a7555443:train:115 | 537:863 | 309f765b1ecc83e0a7f7762e44b4a927a7555443 | [source](https://huggingface.co/datasets/NationalLibraryOfScotland/encyclopaedia_britannica_illustrated/tree/309f765b1ecc83e0a7f7762e44b4a927a7555443) |
| wikipedia:11501704 | 0:800 | 1338304831 | [source](https://en.wikipedia.org/w/index.php?oldid=1338304831) |

`tomi-ai-hermes/evidence/comparison-analysis.json` · `tomi-ai-hermes/evidence/reviewed-six-cases.json`

[submission-guide-fr](submission-guide-fr.md)

[Index documentaire](README.md) · [Instructions de configuration](../../README.md) · [Revue des sources et de l’export](source-review.json)
