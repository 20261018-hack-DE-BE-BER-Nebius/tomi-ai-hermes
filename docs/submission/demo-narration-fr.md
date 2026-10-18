---
id: demo-narration-fr
topic: demo-narration
lang: fr
title: "Narration Tomi : soumission de trois minutes et entretien étendu"
type: guide
status: evidence-draft
updated: "2026-10-18"
tags: [tomi, submission, evidence, fr]
---

[EN](demo-narration-en.md) · [ES](demo-narration-es.md) · [DE](demo-narration-de.md) · [FR](demo-narration-fr.md)

> État des vidéos : les deux fichiers finaux sont inclus dans ce dépôt et vérifiés localement (soumission : 180.000 secondes ; visite : 279.722656 secondes). Revue visuelle et technique indépendante réussie ; écoute, intelligibilité et prononciation non certifiées. Aucune soumission au portail n’a été effectuée. La transcription automatique du MOV est terminée (46 blocs, 87 segments), mais écoute et contrôle de fidélité restent incomplets.

# Tomi

## Narration de soumission de trois minutes

Tomi relie l’Encyclopaedia Britannica historique à Wikipédia et montre ce qui étaye chaque comparaison.

Nous avons choisi cent pages de manière reproductible et vérifié chaque empreinte d’image. Toutes ont reçu de véritables appels Nemotron Parse. Quatre-vingt-dix-huit réponses complètes ont été acceptées, dont trois feuilles blanches ; une planche astronomique reste partielle et une couverture n’a pas de prose exploitable. Un OCR accepté n’est pas une transcription parfaite.

Les quatre modèles NVIDIA imposés fonctionnent. Embed et Rerank utilisent le GPU Nebius attribué. LanceDB stocke et recherche les vecteurs. Nemotron Super VL utilise notre outil de preuves Hermes via la gateway Rust.

Voici trois résultats limités et étayés. Les pièces historiques sont en bois, tandis que le texte moderne définit un chantier naval. Les deux sources associent le litre à un décimètre cube. L’exemple du blanchiment oppose récipients et gaz historiques à l’objectif moderne de décoloration.

Nos premières questions larges ont échoué. La recherche a trouvé des entreprises navales, les politiques de mesure ont remplacé les définitions, et l’OCR du blanchiment ne permettait pas une comparaison complète des procédés. Ces vrais échecs restent à côté des questions limitées réussies.

Hermes sélectionne uniquement les passages proposés. Le serveur les relie aux citations et positions Unicode exactes. Les citations invalides sont rejetées. Même valide, une citation exige encore une vérification du soutien documentaire ; elle ne rend pas automatiquement l’affirmation vraie.

Les 100 pages originales sont comptabilisées. La recherche sémantique réelle a terminé 96 pages textuelles ou partielles :23 résultats candidats et 73 ambigus. Trois feuilles blanches et une couverture sans texte restent non associées ; la planche partielle figure parmi les 96. Échecs initiaux et reprises ciblées sont conservés. Ces comptes ne mesurent pas l’exactitude des associations.

L’archive compilée contient cent documents sur 187 pages PDF. L’application multilingue montre sources et outils ; des tests publics ont vérifié streaming, orientation, annulation et événements enregistrés.

Tomi rend les réponses utiles vérifiables et conserve les raisons des échecs.

## Narration d’entretien étendue

Tomi compare l’Encyclopaedia Britannica historique à Wikipédia. L’objectif est de rendre les preuves et l’incertitude vérifiables, sans considérer une réponse fluide comme une preuve suffisante.

Nous avons sélectionné cent pages avec un manifeste reproductible et vérifié les empreintes. Chaque image a reçu un véritable appel Nemotron Parse 3.5. Quatre-vingt-dix-huit réponses complètes ont été acceptées sans troncature, dont trois feuilles blanches contenant seulement des contrôles de mise en page. Une planche astronomique a nécessité des recadrages et reste partielle ; une couverture n’a pas de prose exploitable. Nous conservons toutes les identités et tentatives. Ce sont des résultats d’extraction, pas une exactitude OCR certifiée.

La chaîne requise utilise désormais les quatre modèles NVIDIA. Les candidats proviennent de l’instantané Wikimedia fixé, avec texte complet, révision et empreintes vérifiées. Embed représente le contenu ; LanceDB stocke et recherche les vecteurs ; Rerank réévalue la pertinence. Ces deux modèles fonctionnent sur notre GPU Nebius attribué. Super VL utilise le véritable outil de preuves Hermes via la gateway Rust. Les identifiants fournisseur restent dans core.

Trois comparaisons limitées ont passé une vérification des sources par l’assistant. Le cas naval compare des pièces historiques en bois à la définition moderne d’un chantier naval. Le cas de mesure associe le litre au décimètre cube dans les deux textes. La réponse normalise la typographie du symbole cubique, mais les citations restent exactes. Le blanchiment compare récipients et gaz historiques au but moderne de décoloration. Ce sont des observations limitées, pas des affirmations générales de progrès scientifique.

Les questions larges initiales ont échoué. La recherche navale favorisait des entreprises ; les candidats de mesure traitaient de politiques plutôt que de définitions ; l’OCR du blanchiment ne permettait pas une comparaison complète des procédés. Nous conservons ces échecs et les questions limitées ultérieures, avec sujets explicites et traces de modèles. Aucune certification humaine indépendante n’est annoncée.

Nous avons aussi reproduit des erreurs de copie des citations. L’outil réparé propose des identifiants immuables de passages. Super VL choisit ces identifiants ; le serveur les lie aux citations et positions Unicode exactes puis applique le même validateur strict. Identifiants inconnus, modifications et références d’un seul corpus sont rejetés. Une citation valide exige toujours une vérification sémantique. La question originale reste distincte de la recherche pour préserver la portée demandée.

Les 100 pages originales sont comptabilisées. La recherche sémantique réelle a terminé 96 pages textuelles ou partielles :23 résultats candidats et 73 ambigus. Trois feuilles blanches et une couverture sans texte restent non associées ; la planche partielle figure parmi les 96. Échecs initiaux et reprises ciblées sont conservés. Ces comptes ne mesurent pas l’exactitude des associations. Les logits de pertinence ne sont pas des probabilités de vérité ; aucune exactitude sur un jeu annoté n’est annoncée. Vocabulaire et fréquences normalisées décrivent les textes avec des limites dues à l’OCR et aux couvertures inégales.

L’archive contient les PDF compilés de cent documents sur 187 pages, du LaTeX modifiable et une visionneuse statique. L’application prend en charge quatre langues. Des tests publics ont validé streaming, orientation, annulation, événements enregistrés et déconnexion. Génération d’image et émission de session realtime ont été testées ; microphone physique et lecture audio ne l’ont pas été.

Six services fonctionnent sur Azure, seul le web étant public. Azure Blob natif permet les écritures LanceDB. Les limites restantes comprennent le rôle administratif de base de données et les questions larges. Le résultat est un processus fonctionnel et vérifiable avec réussites et échecs, sans promettre d’associer toute source ni de répondre à toute question.

## Limites de production et de preuve

Le PDF impose trois minutes. Les vidéos finales incluses durent 180.000 et 279.722656 secondes, avec empreintes conformes et reçus de décodage complet. Le script anglais étendu de préparation reste sous600mots. Les quatre modèles imposés ont réellement été exécutés ; la comparaison Nemotron publique s’est terminée avec sept sources et un avertissement de revue. L’échantillon complet est traité avec ambiguïtés explicites. L’assistant a revu les six cas ; la certification humaine indépendante reste en attente. Aucun dépôt au portail, prix ou fidélité audio physique n’est revendiqué.

[submission-guide-fr](submission-guide-fr.md) · [interview-preparation-fr](interview-preparation-fr.md)

`Hermes/evidence/reviewed-six-cases.json` · `Hermes/evidence/live-nemotron-matching-20261018T1742Z/progress.json` · `Hermes/archive/assets/compile-receipt.json`

Classification sémantique finale :95 pages textuelles Parse,1 planche astronomique partielle(ligne2243),3 feuilles blanches(lignes374,1615,2077) et1 couverture sans texte(ligne452)=100 originaux. Les trois feuilles ont été inspectées visuellement. Les98 réponses Parse complètes acceptées comprennent ces3 sorties de mise en page ; acceptation ne signifie ni prose exploitable ni exactitude OCR. Reçus conservés. `Hermes/evidence/page-content-classification.json` contient100 identités et empreintes.


Les 100 pages originales sont comptabilisées. La recherche sémantique réelle a terminé 96 pages textuelles ou partielles :23 résultats candidats et 73 ambigus. Trois feuilles blanches et une couverture sans texte restent non associées ; la planche partielle figure parmi les 96. Échecs initiaux et reprises ciblées sont conservés. Ces comptes ne mesurent pas l’exactitude des associations.

`Hermes/evidence/100-page-semantic-summary.json` · `Hermes/evidence/100-page-semantic-ledger.csv` · `Hermes/evidence/page-content-classification.json`

[Index documentaire](README.md) · [Instructions de configuration](../../README.md) · [Revue des sources et de l’export](source-review.json)
