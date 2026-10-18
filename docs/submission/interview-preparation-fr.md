---
id: interview-preparation-fr
topic: interview-preparation
lang: fr
title: "Vingt questions NVIDIA et Nebius avec réponses étayées"
type: guide
status: conditional-draft
updated: "2026-10-18"
tags: [tomi, interview, evidence, fr]
---

[EN](interview-preparation-en.md) · [ES](interview-preparation-es.md) · [DE](interview-preparation-de.md) · [FR](interview-preparation-fr.md)

> État des vidéos : les deux fichiers finaux sont inclus dans ce dépôt et vérifiés localement (soumission : 180.000 secondes ; visite : 279.722656 secondes). Revue visuelle et technique indépendante réussie ; écoute, intelligibilité et prononciation non certifiées. Aucune soumission au portail n’a été effectuée. La transcription automatique du MOV est terminée (46 blocs, 87 segments), mais écoute et contrôle de fidélité restent incomplets.

# Préparation à l'entretien

Questions probables, et non questionnaire officiel. Les réponses décrivent la base vérifiée ; actualiser les points en attente uniquement avec des preuves réelles. Exigences : [submission-guide-fr](submission-guide-fr.md). Preuves applicatives : implementation delivery fr.

1. **Quel problème résout Tomi ?** Tomi compare Britannica historique à un instantané Wikipédia fixé. Il relie des différences ou continuités limitées à des passages vérifiables et indique quand les sources ne permettent pas de répondre à une question large.

2. **Qu'avez-vous construit au-delà du starter ?** Nous avons construit pipeline Python, outil Hermes et liaison des citations, gateway et backend Rust, interfaces multilingues, corpus reproductible et archive LaTeX compilée. Nous avons aussi corrigé de vrais défauts de stockage, recherche et protocole tout en conservant leurs reçus.

3. **Pourquoi quatre modèles Nemotron ?** Parse 3.5 transforme les scans en texte structuré. Embed VL produit des vecteurs normalisés de 2048 dimensions, recherchés par LanceDB. Rerank VL réévalue la pertinence avec des logits bruts. Super VL mène le dialogue Hermes et rédige les comparaisons. Les quatre ont des preuves réelles et des rôles complémentaires.

4. **Pourquoi Nebius ?** Nebius fournit des services distincts : Parse et index Wikipédia partagés, Token Factory pour Super VL et GPU attribué pour Embed/Rerank. Azure héberge l’application. Déploiements et identifiants restent distincts.

5. **Comment avez-vous choisi 100 pages ?** Le manifeste fixe 100 lignes sur 2.573 par échantillonnage aléatoire sans remplacement, graine 20261016. Il conserve la révision immuable et chaque empreinte d’image. Pages difficiles, blanches et illustrées restent dans l’échantillon.

6. **Les 100 ont-elles fonctionné ?** Les 100 ont reçu de vrais appels Parse. Bilan final :95 pages textuelles complètes,1 planche partielle,3 feuilles blanches vérifiées visuellement et 1 couverture sans texte. Les 98 réponses complètes acceptées comprennent 3 sorties de mise en page seule ; acceptation n’a jamais signifié OCR parfait.

7. **Comment mesurez-vous la qualité d'extraction ?** Nous vérifions empreintes, provenance, troncature et certains scans. Trois sorties normalisées vides ont été confrontées aux images et classées blanches. Aucun taux complet d’erreur de caractères ni précision d’ordre de lecture annotés humainement n’a été mesuré.

8. **Pourquoi le titre ne suffit-il pas ?** Les articles complets viennent du snapshot fixé et leurs empreintes sont vérifiées. Les contrôles de mise en page sont supprimés uniquement des entrées modèles, puis interviennent Embed, LanceDB et Rerank. Un article déjà vérifié avec titre exact dans le même snapshot complète un faible rappel BM 25. Les citations brutes restent inchangées.

9. **Quelle est votre précision d'association ?** Nous n’avons pas d’exactitude défendable sur un jeu annoté. Scores, marges, ambiguïtés, couverture et exemples revus sont séparés. Le traitement des 100 pages et ses reprises conservent les échecs, sans transformer des réponses API réussies en mesure d’exactitude.

10. **Quel rôle joue LanceDB ?** LanceDB conserve nos documents et vecteurs ; l’index BM 25 partagé est distinct. Des écritures Azure Blob natives ont été vérifiées, car Azure Files ne permet pas les commits Lance sûrs. La première sonde 183-documents/zéro-vecteur est historique ; les comptes ultérieurs ont leurs propres reçus.

11. **Quelles analyses calculez-vous ?** Nous calculons chevauchement Jaccard, divergence Jensen–Shannon et fréquences. Ils décrivent des distributions textuelles, pas la vérité historique. OCR, mots fréquents, longueur et couverture peuvent dominer. BERTopic était facultatif ; aucune exécution n’est revendiquée.

12. **Qu'est-ce qui fait de Hermes un agent ?** Hermes exécute une véritable boucle d’outils pilotée par modèle : Super VL appelle l’unique fonction de preuves en lecture, reçoit des passages bornés puis retourne des IDs dans des affirmations structurées. La trace est conservée. Aucun outil shell, fichiers ou navigation ; un code déterministe valide ensuite les sources.

13. **Comment empêchez-vous les citations inventées ?** Seuls les IDs proposés peuvent être choisis. Le serveur les relie aux citations et positions Unicode immuables puis applique le validateur strict. IDs inconnus, modifications et références d’un seul corpus sont rejetés. Le soutien sémantique est vérifié séparément.

14. **Quels sont les cas d'échec ?** Les trois échecs retenus sont des questions larges sur navires, mesures et blanchiment : faible rappel, politiques plutôt que définitions et OCR corrompu ont empêché des comparaisons complètes utiles. Page absente, GPS indisponible et attaque d’instructions restent aussi documentés. Les réussites limitées ultérieures ne les effacent pas.

15. **Comment traitez-vous l'injection ?** OCR et textes récupérés sont des données non fiables. L’agent ne reçoit aucune clé et dispose d’un seul outil borné en lecture. Les attaques réelles ont conduit à l’abstention ; les tests rejettent les références non autorisées. Cela prouve des protections précises, pas une immunité universelle.

16. **Que fonctionne-t-il réellement en public ?** La comparaison Nemotron dans l’interface publique s’est terminée le 18 octobre 2026 à 21:17:20 UTC avec sept sources et un avertissement `needs_review` visible ; recharger le canevas a restauré la même réponse. Le reçu API core distinct de 21:08:42 UTC documente les exécutions réelles de Super VL, Embed, Rerank et Hermes sur le corpus issu de Parse. Une exécution terminée ne certifie pas le soutien sémantique de chaque affirmation. Les contrôles Astra antérieurs, orientation, annulation, événements enregistrés et déconnexion restent des preuves séparées. [Reçu de l’interface publique](../../demo/public-workspace-acceptance.json).

17. **Quelle multimodalité est vérifiée ?** La génération publique a retourné un vrai PNG et l’émission d’une session realtime a réussi. Le cinquième modèle NVIDIA supplémentaire, `nvidia/Nemotron-3-Diarization`, a traité un échantillon officiel de 30 secondes via la route publique par lots : HTTP 200 en 34.29 secondes, six segments et cinq étiquettes anonymes, également visibles dans l’interface. Ce ne sont ni des identités reconnues ni une mesure d’exactitude des locuteurs. Ce modèle complète les quatre modèles imposés. Microphone physique, lecture audio et conversation realtime de bout en bout restent non vérifiés.

18. **Quel déploiement et quelle sécurité ?** Six services tournent sur Azure, seul le web est public ; la recherche imposée fonctionne sur Nebius. Les clés restent dans core. Les scans de secrets contrôlés sont propres. Rôle PostgreSQL administratif et historique Covenant éphémère restent des limites ; aucune validation production ou LTS.

19. **Qu'amélioreriez-vous ensuite ?** Priorités : labels indépendants de pertinence, revue OCR et segmentation, calibration, questions larges plus robustes et rôle de base de données restreint. Les feuilles blanches montrent pourquoi transport réussi et contenu utilisable doivent être évalués séparément.

20. **Le projet est-il terminé et soumis ?** Trois cas limités ont été vérifiés par l’assistant contre leurs sources, et trois vrais échecs sont conservés. L’échantillon possède un registre et des reprises distincts ; la certification humaine indépendante reste absente. Dépôt et vidéo ne sont pas des accusés. Échéance :18 octobre 2026 à 18:30 CEST ; prolongation et acceptation non vérifiées.

Références : `submission-guide/evidence/source-review.json` ; Hermes `evidence/100-page-extraction.json`, `page-visual-review.json`, `six-case-evaluation.json`, `azure-blob-runtime-probe.json` ; backend `verification/public-acceptance.json`, `public-multimodal.json` ; IaC `verification/security-deployment-review.json`. Dépôts et chemins : `submission-guide/repository-map.json`. Distinguer preuve actuelle, implémentation et travail prévu.

`Hermes/evidence/reviewed-six-cases.json`; `Hermes/evidence/live-nemotron-matching-20261018T1742Z/progress.json`; `core/verification/nebius-model-deployment/core-retrieval-live.json`; `core/verification/nebius-model-deployment/gpu-models-live.json`.

Classification sémantique finale :95 pages textuelles Parse,1 planche astronomique partielle(ligne2243),3 feuilles blanches(lignes374,1615,2077) et1 couverture sans texte(ligne452)=100 originaux. Les trois feuilles ont été inspectées visuellement. Les98 réponses Parse complètes acceptées comprennent ces3 sorties de mise en page ; acceptation ne signifie ni prose exploitable ni exactitude OCR. Reçus conservés. `Hermes/evidence/page-content-classification.json` contient100 identités et empreintes.


Les 100 pages originales sont comptabilisées. La recherche sémantique réelle a terminé 96 pages textuelles ou partielles :23 résultats candidats et 73 ambigus. Trois feuilles blanches et une couverture sans texte restent non associées ; la planche partielle figure parmi les 96. Échecs initiaux et reprises ciblées sont conservés. Ces comptes ne mesurent pas l’exactitude des associations.

`Hermes/evidence/100-page-semantic-summary.json` · `Hermes/evidence/100-page-semantic-ledger.csv` · `Hermes/evidence/page-content-classification.json`

[Index documentaire](README.md) · [Instructions de configuration](../../README.md) · [Revue des sources et de l’export](source-review.json)
