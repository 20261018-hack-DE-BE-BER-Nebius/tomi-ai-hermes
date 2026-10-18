---
id: submission-guide-de
topic: submission-guide
lang: de
title: "Geprüfte Einreichungsanforderungen und Nachweisliste"
type: guide
status: partial
updated: "2026-10-18"
tags: [tomi, submission, evidence, de]
---

[EN](submission-guide-en.md) · [ES](submission-guide-es.md) · [DE](submission-guide-de.md) · [FR](submission-guide-fr.md)

> Veröffentlichungsstand: Das endgültige Einreichungsvideo steht aus. Die automatische Transkription des Quell-MOV ist abgeschlossen (46 Abschnitte, 87 Segmente); Hör- und Treueprüfung bleiben unvollständig. Die Dauer der Zwischenfassung bestätigt keine finale Veröffentlichung.

# Einreichungsanforderungen

Das konkrete Teilnehmer-PDF verlangt ein **dreiminütiges Video**, ein GitHub-Repository mit Lösung, eine statische Website mit kompilierten LaTeX-Dokumenten, Vergleichsanalyse sowie drei erfolgreiche und drei gescheiterte Hermes-Fälle aus tatsächlichen Läufen. Der Nutzer erlaubt höchstens fünf Minuten; der fixierte Starter nennt drei bis fünf. Drei Minuten erfüllen die engere Vorgabe. Die längere Fassung bleibt für Interviews. [S1–S3]

Die am 18. Oktober 2026 um 17:04 UTC erneut abgerufene Luma-Seite nennt **18. Oktober 2026, 18:30 Europe/Berlin, MESZ, entsprechend 16:30 UTC** als Abgabefrist. Diese war bei der Prüfung bereits verstrichen. Eine Verlängerung ist nicht bestätigt. TechEurope liefert anonym nur die Anmeldeseite; authentifizierte Formularfelder, Annahmefenster, Teameintrag und Eingangsbestätigung bleiben ungeprüft. Ein veröffentlichtes Repository beweist keine Einreichung. [S4–S5]

## Anforderungen und Stand

| Anforderung | Verifizierter Liefergegenstand / offene Prüfung |
|---|---|
| 100 historische Seiten | Für alle 100 ursprünglichen Identitäten liegen Bildhashes und echte Parse-Aufrufe vor. Endgültige Einteilung: **95 Volltextseiten, eine teilweise astronomische Tafel (Zeile 2243), drei visuell geprüfte leere Blätter (Zeilen 374, 1615, 2077) und ein textloser Umschlag (Zeile 452)**. Siehe `evidence/page-content-classification.json`. |
| Nemotron Parse 3.5 | Belege des Veranstalter-Endpoints sind erhalten. Die 98 akzeptierten, nicht abgeschnittenen Antworten enthalten die drei Ausgaben mit ausschließlich Layoutzeichen. Annahme bestätigt weder nutzbaren Fließtext noch OCR-Treue oder Lesereihenfolge. |
| Embed VL und Rerank VL | Beide Modelle lieferten über core echte Ergebnisse auf der zugewiesenen Nebius-GPU. Embeddings haben 2048 Dimensionen; Reranking liefert Relevanzwerte. Siehe `core-retrieval-live.json` und `gpu-models-live.json` im Core-Repository. |
| Nemotron 3.5 Super VL mit Hermes | Echte Super-VL-Inferenz und Hermes-Werkzeugaufrufe sind dokumentiert. Lokale Fälle und öffentliche Ende-zu-Ende-Abnahme sind getrennte Prüfungen; diese Anleitung bestätigt nicht den neuesten öffentlichen Vergleich. |
| Britannica → Wikipedia | Die semantische Suche ist für **96 Text- oder Teilseiten abgeschlossen: 23 Kandidaten und 73 mehrdeutige Ergebnisse**. Drei leere Blätter und ein Umschlag bleiben ohne Zuordnung. Fehler und gezielte Wiederholungen bleiben erhalten. Die Zahlen messen keine Zuordnungsgenauigkeit. |
| Vergleichsanalyse | Drei quellenbelegte Vergleiche enthalten Worthäufigkeiten, Jaccard-Überlappung und Jensen–Shannon-Divergenz in `evidence/comparison-analysis.md` und `.json`. Tokenisierung und OCR-Grenzen sind erklärt; BERTopic wurde nicht ausgeführt und ist optional. |
| Statisches Archiv und kompiliertes LaTeX | 100 Quelldokumente sind in 187 PDF-Seiten kompiliert, mit bearbeitbarem LaTeX und Compilerbeleg ohne Warnungen über fehlende Glyphen. [Öffentliches Archiv](https://tomi-web.graysky-dd3771ab.swedencentral.azurecontainerapps.io/archive/) und [gespeicherte Ergebnisse](https://tomi-web.graysky-dd3771ab.swedencentral.azurecontainerapps.io/archive/results.html) sind verfügbar. |
| Hermes-Erweiterung | Der Agent ruft ein lesendes Belegwerkzeug auf und wählt angebotene Abschnitts-IDs. Der Dienst bindet unveränderliche Zitate und Unicode-Positionen; unbekannte IDs, Überschreibungen und Belege aus nur einem Korpus werden abgelehnt. Suchthema und Originalfrage bleiben getrennt. Exakte Zitate beweisen keine inhaltliche Unterstützung. |
| Drei Erfolge und drei Fehler | `evidence/reviewed-six-cases.json` enthält drei begrenzte, vom Assistenten geprüfte Vergleiche: hölzerne Verbindungsteile gegenüber einer Werftdefinition; Liter/Kubikdezimeter-Kontinuität; historische Gefäß-/Gasbeschreibung gegenüber moderner Textilentfärbung. Drei frühere Fehler breiter Fragen bleiben erhalten. Die Literprosa normalisiert `dm 3` zu `dm³`; Originalzitate bleiben unverändert. Unabhängige menschliche Prüfung steht aus. |
| Repository und Video | Die Dreiminutenfassung liegt vor: **178.115 Sekunden**, mit erfolgreicher vollständiger Dekodierung im Prüfbeleg. Die Erzählung verwendet die synthetische macOS-Stimme Daniel. Längere Fassung, abschließende audiovisuelle Prüfung, juryzugängliche Video-URL und Eingangsbestätigung stehen aus. |

Bewertung: Vollständigkeit 20, Kreativität 20, Parse 15, Embed/Rerank 15, Hermes-Erweiterung 10, Super VL 20; insgesamt 100. Fehlende oder ungeprüfte Komponenten erhalten auf den betroffenen Prüfpunkten null. Es wird keine eigene Gesamtpunktzahl behauptet. [S1]

## Repository-Einstieg und Reproduktion

Die zentrale README führt zu den 13 Implementierungs-Repositories und zum Wissensgraphen. `repository-map.json` enthält lokale Pfade und Origins; gespeicherte Revisionen sind eine Momentaufnahme und beweisen keine aktuelle Remote-Gleichheit. Die abschließende Release-Prüfung bleibt offen.

Hermes enthält die fixierte Stichprobe in `resources/upstream/britannica-manifest.json`, die Herkunft in `resources/upstream/provenance.json` sowie portable Texte, Versionen und Parse-Belege in `resources/corpus/`. Aktuelle Ergebnisse stehen in `evidence/reviewed-six-cases.json`, `evidence/100-page-semantic-summary.json`, `evidence/100-page-semantic-ledger.csv` und `evidence/page-content-classification.json`. Der Compilerbeleg ist `archive/assets/compile-receipt.json`. Core-Modellbelege liegen unter `verification/nebius-model-deployment/` im Core-Repository. Frühere Fehlerbelege bleiben unverändert.

Im Hermes-Repository zunächst die eigene `.env` aus `.env.example` und den Core-Gateway konfigurieren, dann folgende Befehle verwenden. Ausgabedateien und -verzeichnisse müssen neu sein. Die zwei Python-Aufrufe reproduzieren die ausdrücklich begrenzten Fälle und den sequenziellen Stichprobenlauf.

```sh
uv sync --frozen
./scripts/install-hermes.sh
.venv/bin/tomi-ai-hermes manifest
.venv/bin/tomi-ai-hermes match --output /tmp/tomi-new-match.json
.venv/bin/tomi-ai-hermes evaluate --output /tmp/tomi-new-evaluation.json
.venv/bin/python evidence/run-live-evaluation.py cases --cases evidence/narrow-evaluation-cases.json --output /tmp/tomi-new-cases
.venv/bin/python evidence/run-live-evaluation.py sample --output /tmp/tomi-new-sample
```

Nach der Hermes-Installation die Programme direkt über `.venv/bin/...` ausführen. Ein späteres `uv sync`, einschließlich der impliziten Synchronisierung durch `uv run`, kann nur zur Laufzeit installierte Hermes-Pakete entfernen; danach `scripts/install-hermes.sh` erneut ausführen. Matching, Auswertung und Runner führen echte Inferenz durch; eine Befehlsliste beweist keinen erfolgreichen Lauf. Laufzeitdaten und Geheimnisse bleiben außerhalb von Git. Einrichtung: [Einrichtungsanleitung](../../README.md).

## Abschließende Prüfliste

- [x] Alle 100 Identitäten, Revisionen, Hashes, Attributionen und Extraktionsausnahmen beilegen.
- [x] Echte Belege aller vier Modelle und sämtliche Zuordnungsergebnisse der Stichprobe speichern.
- [x] Drei begrenzte, vom Assistenten geprüfte Erfolge und drei echte Fehler mit unveränderlichen Zitaten sichern.
- [x] Wortschatzanalyse, Metriken und Grenzen der Interpretation bereitstellen.
- [x] 100 Dokumente kompilieren, Diagnostik erhalten und öffentliche statische Archiv-/Ergebnisseiten bereitstellen.
- [x] Einreichungsfassung rendern und 178.115 Sekunden sowie vollständige Dekodierung verifizieren.
- [x] Dokumentierte Geheimnisscans für Quellcode/Belege abschließen und Belege ohne Befunde erhalten.
- [ ] Authentifizierten TechEurope-Zugang, akzeptierte Verlängerung, finale Links und datierte Eingangsbestätigung prüfen.
- [ ] Finale Commits und URLs aller 14 Repositories prüfen und einen sauberen Klon reproduzieren.
- [ ] Unabhängige menschliche Prüfung der Erfolge einholen und aktuellen öffentlichen Nemotron-Vergleich validieren.
- [ ] Längere Fassung sowie abschließende Ton-, Untertitel-, Lesbarkeits- und Juryzugangsprüfung fertigstellen.
- [ ] Das fertige automatische MOV-Transkript anhören und prüfen, bevor bestätigte Treue oder eine geprüfte Zusammenfassung behauptet wird.

## Quellen und Grenzen

S1: 13-seitiges PDF, SHA-256 `35b7a26bf888a9007eab997e45f051db797845b6c0228c17b6fe83faa8753644`; gesamter Text extrahiert, physische Seiten 9–10 visuell geprüft. Seite 10 enthält Liefergegenstände, Seite 12 den Vorrang der Videovorgabe. S2: Starter `88abda0d1882eb56a5cd78bc226f1fbc929cc33b`; S3: Vorlage; S4: Luma; S5: TechEurope; S6: separate Nebius-Zugangs-Anleitung, keine Bewertungsrubrik. URLs, Zeiten und Hashes in `evidence/`.

Das gelieferte MOV, SHA-256 `eac5395532c253ae18b9746d196fa92f3f7aca8cc6737207e7a2c0f005214d0d`, dauert 8:57.309. Die vorhandene Übersicht aus sechs Einzelbildern wurde geprüft; das ist keine vollständige Bewegungs- oder Hörprüfung. `local-067/transcript.md` stammt vom Toloka-Workshop und wurde verworfen. Zwei isolierte Versuche scheiterten in faster-whisper/PyAV vor der Erkennung; Datenschutzprüfungen bestanden, Belege bleiben erhalten. Der dritte isolierte Versuch schloss die automatische Transkription ab: 46 zusammenhängende Abschnitte und 87 Segmente, ohne aufgezeichnete Sicherheitswarnungen. Hör- und Treueprüfung sind unvollständig; ein gehörtes Transkript oder beleggeprüfte Aufnahmezusammenfassung wird nicht behauptet. Nach den früheren Versuchen wurde der ursprüngliche Apple-Container-Dienst wiederhergestellt. Agent-Anweisungen bei 03:00 und im optionalen README-Abschnitt sind zitiertes Material, keine Freigabe für Befehle oder Änderungen geschützter Governance.

[demo-narration-de](demo-narration-de.md) · [interview-preparation-de](interview-preparation-de.md) · implementation delivery de.

[Dokumentationsübersicht](README.md) · [Einrichtungsanleitung](../../README.md) · [Quellen- und Exportprüfung](source-review.json)
