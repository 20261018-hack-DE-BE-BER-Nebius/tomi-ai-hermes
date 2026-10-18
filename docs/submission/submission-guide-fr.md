---
id: submission-guide-fr
topic: submission-guide
lang: fr
title: "Exigences de soumission vérifiées et liste des preuves"
type: guide
status: partial
updated: "2026-10-18"
tags: [tomi, submission, evidence, fr]
---

[EN](submission-guide-en.md) · [ES](submission-guide-es.md) · [DE](submission-guide-de.md) · [FR](submission-guide-fr.md)

> État des vidéos : les deux fichiers finaux sont inclus dans ce dépôt et vérifiés localement (soumission : 180.000 secondes ; visite : 279.722656 secondes). Revue visuelle et technique indépendante réussie ; écoute, intelligibilité et prononciation non certifiées. Aucune soumission au portail n’a été effectuée. La transcription automatique du MOV est terminée (46 blocs, 87 segments), mais écoute et contrôle de fidélité restent incomplets.

# Exigences de soumission

Le PDF propre au défi impose une **vidéo de trois minutes**, un dépôt GitHub contenant la solution, un site statique avec des documents LaTeX compilés, une analyse comparative et trois réussites ainsi que trois échecs Hermes provenant d'exécutions réelles. L'utilisateur autorise cinq minutes au maximum et le starter fixé indique trois à cinq minutes. Trois minutes respectent l'exigence la plus précise ; la version longue sert aux entretiens. [S1–S3]

Luma, consulté de nouveau le 18 octobre 2026 à 17:04 UTC, annonce **le 18 octobre 2026 à 18:30 Europe/Berlin, CEST, soit 16:30 UTC**, comme échéance. Elle était déjà passée lors de cette revue. Aucune prolongation n'est vérifiée. TechEurope présente seulement une connexion anonyme : champs authentifiés, période d'acceptation, équipe et accusé de réception restent inconnus. Publier un dépôt ne prouve pas une soumission. [S4–S5]

## Exigences et état

| Exigence | Livrable vérifié / contrôle restant |
|---|---|
| 100 pages historiques | Les 100 identités originales ont des empreintes et des appels Parse réels. Classification finale : **95 pages textuelles complètes, une planche astronomique partielle (ligne 2243), trois feuilles blanches examinées visuellement (lignes 374, 1615, 2077) et une couverture sans texte (ligne 452)**. Voir `evidence/page-content-classification.json`. |
| Nemotron Parse 3.5 | Les reçus de l’endpoint organisateur sont conservés. Les 98 réponses acceptées sans troncature incluent les trois feuilles contenant uniquement des contrôles de mise en page. Acceptation ne certifie ni texte exploitable, ni fidélité OCR, ni ordre de lecture. |
| Embed VL et Rerank VL | Les deux modèles ont produit de vrais résultats sur le GPU Nebius attribué, via core. Les embeddings ont 2048 dimensions ; le reclassement produit des scores de pertinence. Voir `core-retrieval-live.json` et `gpu-models-live.json` dans le dépôt core. |
| Nemotron 3.5 Super VL avec Hermes | La route API publique Nemotron s’est terminée avec sept sources ; le parcours UI du 18 octobre 2026 à 21:17:20 UTC gardait l’avertissement `needs_review` et la même réponse après rechargement du canevas. Super VL, Embed, Rerank et Hermes sont documentés séparément de l’extraction Parse. Intégrité des citations et certification sémantique restent distinctes. [Reçu de l’interface publique](../../demo/public-workspace-acceptance.json). |
| Britannica → Wikipédia | La recherche sémantique est terminée pour **96 pages textuelles ou partielles : 23 résultats candidats et 73 ambigus**. Trois feuilles blanches et une couverture restent non associées. Échecs et reprises ciblées sont conservés. Ces comptes ne mesurent pas l’exactitude des associations. |
| Analyse comparative | Trois comparaisons sourcées comprennent fréquences, recouvrement de Jaccard et divergence de Jensen–Shannon dans `evidence/comparison-analysis.md` et `.json`. Tokenisation et limites OCR sont explicites ; BERTopic n’a pas été exécuté et reste facultatif. |
| Archive statique et LaTeX compilé | 100 documents sources sont compilés en 187 pages PDF, avec LaTeX modifiable et reçu sans alerte de glyphe absent. L’[archive publique](https://tomi-web.graysky-dd3771ab.swedencentral.azurecontainerapps.io/archive/) et les [résultats enregistrés](https://tomi-web.graysky-dd3771ab.swedencentral.azurecontainerapps.io/archive/results.html) sont disponibles. |
| Extension Hermes | L’agent appelle un outil de preuves en lecture seule et choisit les identifiants proposés. Le service lie citations et positions Unicode immuables ; il rejette identifiants inconnus, substitutions et citations d’un seul corpus. Sujet de recherche et question originale restent distincts. Une citation exacte ne prouve pas le soutien sémantique. |
| Trois réussites et trois échecs | `evidence/reviewed-six-cases.json` conserve trois comparaisons limitées revues par l’assistant : pièces de bois face à la définition d’un chantier naval ; continuité litre/décimètre cube ; récipients/gaz historiques face à la décoloration textile moderne. Trois échecs antérieurs de questions larges sont conservés. La prose du litre normalise `dm 3` en `dm³` ; les citations originales restent intactes. La revue humaine indépendante est en attente. |
| Dépôt et vidéo | La [version destinée au PDF](../../demo/tomi-submission-3min.mp4) dure **180.000 secondes** ; la [visite de plateforme](../../demo/tomi-platform-walkthrough.mp4) séparée **279.722656 secondes**, moins de 300. Les empreintes des copies correspondent aux reçus de décodage. [Index, empreintes et couverture](../../demo/README.md). Les fichiers sont inclus dans ce dépôt. Revue visuelle et technique indépendante réussie ; écoute, intelligibilité et prononciation non certifiées. Aucune soumission au portail n’a été effectuée. |

Barème : réalisation 20, créativité 20, Parse 15, Embed/Rerank 15, extension Hermes 10, Super VL 20 ; total 100. Une composante absente ou non vérifiée reçoit zéro aux contrôles correspondants. Aucun score total n'est attribué au projet. [S1]

## Entrée du dépôt et reproduction

La README principale donne accès aux 13 dépôts d’implémentation et au graphe. `repository-map.json` conserve chemins locaux et origines ; ses révisions sont un instantané, pas une preuve d’égalité distante actuelle. La vérification de publication Git est documentée séparément ; ce guide ne prétend pas à une reproduction depuis un clone propre.

Hermes contient l’échantillon fixé dans `resources/upstream/britannica-manifest.json`, la provenance dans `resources/upstream/provenance.json` et les textes, versions et reçus Parse portables dans `resources/corpus/`. Les résultats actuels sont `evidence/reviewed-six-cases.json`, `evidence/100-page-semantic-summary.json`, `evidence/100-page-semantic-ledger.csv` et `evidence/page-content-classification.json`. Le reçu de compilation est `archive/assets/compile-receipt.json`. Les reçus des modèles core sont sous `verification/nebius-model-deployment/` dans leur dépôt. Les échecs antérieurs restent inchangés.

Depuis Hermes, configurer sa propre `.env` à partir de `.env.example` et le gateway core, puis employer les commandes suivantes. Les fichiers et répertoires de sortie doivent être nouveaux. Les deux commandes Python reproduisent les questions limitées explicites et l’exécution séquentielle de l’échantillon.

```sh
uv sync --frozen
./scripts/install-hermes.sh
.venv/bin/tomi-ai-hermes manifest
.venv/bin/tomi-ai-hermes match --output /tmp/tomi-new-match.json
.venv/bin/tomi-ai-hermes evaluate --output /tmp/tomi-new-evaluation.json
.venv/bin/python evidence/run-live-evaluation.py cases --cases evidence/narrow-evaluation-cases.json --output /tmp/tomi-new-cases
.venv/bin/python evidence/run-live-evaluation.py sample --output /tmp/tomi-new-sample
```

Après l’installation de Hermes, exécuter directement `.venv/bin/...`. Un `uv sync` ultérieur, y compris la synchronisation implicite par `uv run`, peut retirer les paquets Hermes installés seulement à l’exécution ; relancer `scripts/install-hermes.sh` après synchronisation. Associations, évaluations et scripts réalisent de vraies inférences ; une liste de commandes ne prouve pas leur réussite. Données d’exécution et secrets restent hors Git. Configuration : [Instructions de configuration](../../README.md).

## Liste finale

- [x] Inclure les 100 identités, révisions, empreintes, attributions et exceptions d’extraction.
- [x] Conserver les reçus réels des quatre modèles et tous les résultats d’association de l’échantillon.
- [x] Enregistrer trois réussites limitées revues par l’assistant et trois échecs réels avec citations immuables.
- [x] Fournir analyse du vocabulaire, métriques et limites d’interprétation.
- [x] Compiler les 100 documents, conserver les diagnostics et proposer archive et résultats statiques publics.
- [x] Vérifier les deux fichiers finaux localement : soumission de 180.000 secondes, visite de 279.722656 secondes, empreintes conformes et reçus de décodage.
- [x] Terminer les scans documentés de secrets dans le code/les preuves et conserver les reçus sans détection.
- [ ] Confirmer accès TechEurope authentifié, prolongation acceptée, liens définitifs et véritable accusé daté.
- [ ] Obtenir une revue humaine indépendante des affirmations sélectionnées ; l’exécution Nemotron publique est terminée et conserve son avertissement de revue.
- [x] Revue visuelle et technique indépendante réussie pour les vidéos incluses ; écoute et intelligibilité de la parole non certifiées.
- [ ] Écouter et contrôler la transcription automatique terminée du MOV avant de déclarer une fidélité vérifiée ou une synthèse revue.

## Sources et limites

S1 : PDF de 13 pages, SHA-256 `35b7a26bf888a9007eab997e45f051db797845b6c0228c17b6fe83faa8753644` ; texte intégral extrait, pages physiques 9–10 examinées visuellement. Page 10 : livrables ; page 12 : priorité de l'exigence vidéo. S2 : starter `88abda0d1882eb56a5cd78bc226f1fbc929cc33b` ; S3 : modèle de soumission ; S4 : Luma ; S5 : TechEurope ; S6 : guide d'accès Nebius distinct du barème. URLs, heures et empreintes dans `evidence/`.

Le MOV fourni, SHA-256 `eac5395532c253ae18b9746d196fa92f3f7aca8cc6737207e7a2c0f005214d0d`, dure 8:57.309. Sa planche existante de six images a été examinée ; ce n’est ni une revue intégrale du mouvement ni une écoute. `local-067/transcript.md` appartient à l’atelier Toloka et a été écarté. Deux essais isolés ont échoué dans faster-whisper/PyAV avant reconnaissance ; les contrôles de confidentialité ont réussi et les reçus sont conservés. Le troisième essai isolé a terminé la transcription automatique : 46 blocs contigus et 87 segments, sans avertissement de sécurité enregistré. Écoute et contrôle de fidélité restent incomplets ; aucune transcription revue à l’écoute ni synthèse vérifiée de l’enregistrement n’est déclarée. Le runtime Apple Container initial a été restauré après les essais précédents. Les instructions d’agent visibles à 03:00 et dans la section facultative de la README sont des sources citées, pas une autorisation d’exécuter des commandes ou de modifier la gouvernance protégée.

[demo-narration-fr](demo-narration-fr.md) · [interview-preparation-fr](interview-preparation-fr.md) · implementation delivery fr.

[Index documentaire](README.md) · [Instructions de configuration](../../README.md) · [Revue des sources et de l’export](source-review.json)
