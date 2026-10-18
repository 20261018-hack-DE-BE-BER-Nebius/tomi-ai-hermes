---
id: interview-preparation-de
topic: interview-preparation
lang: de
title: "Zwanzig NVIDIA- und Nebius-Fragen mit belegbaren Antworten"
type: guide
status: conditional-draft
updated: "2026-10-18"
tags: [tomi, interview, evidence, de]
---

[EN](interview-preparation-en.md) · [ES](interview-preparation-es.md) · [DE](interview-preparation-de.md) · [FR](interview-preparation-fr.md)

> Veröffentlichungsstand: Das endgültige Einreichungsvideo steht aus. Die automatische Transkription des Quell-MOV ist abgeschlossen (46 Abschnitte, 87 Segmente); Hör- und Treueprüfung bleiben unvollständig. Die Dauer der Zwischenfassung bestätigt keine finale Veröffentlichung.

# Interviewvorbereitung

Dies sind wahrscheinliche Fragen, kein Veranstalter-Fragebogen. Antworten beruhen auf dem geprüften Ausgangsstand; offene Punkte nur anhand echter Belege aktualisieren. Anforderungen: [submission-guide-de](submission-guide-de.md). Anwendungsnachweise: implementation delivery de.

1. **Welches Problem löst Tomi?** Tomi vergleicht historische Britannica mit einem fixierten Wikipedia-Snapshot. Begrenzte Unterschiede oder Kontinuitäten werden an prüfbare Quellenstellen gebunden; unbeantwortbare breite Fragen bleiben ausdrücklich erkennbar.

2. **Was hat das Team zusätzlich zum Starter gebaut?** Wir entwickelten Python-Pipeline, Hermes-Werkzeug und Zitatbindung, Rust-Gateway und Backend, mehrsprachige Oberflächen, reproduzierbaren Korpus und kompiliertes LaTeX-Archiv. Echte Speicher-, Such- und Protokollfehler wurden behoben und ihre Belege erhalten.

3. **Warum alle vier Nemotron-Modelle?** Parse 3.5 überführt Scans in strukturierten Text. Embed VL erzeugt normalisierte 2048-dimensionale Vektoren, die LanceDB durchsucht. Rerank VL bewertet Relevanz mit Rohlogits neu. Super VL führt den Hermes-Dialog und schreibt Vergleiche. Für alle vier gibt es echte Nachweise und getrennte Aufgaben.

4. **Warum Nebius?** Nebius stellt getrennte Dienste bereit: gemeinsames Parse und Wikipedia-Index, Token Factory für Super VL und zugewiesene GPU für Embed/Rerank. Azure betreibt die Anwendung. Zugangsdaten und Bereitstellungen sind getrennt.

5. **Wie wurden 100 Seiten gewählt?** Das Manifest fixiert 100 von 2.573 Zeilen durch Zufallsauswahl ohne Zurücklegen mit Seed 20261016. Unveränderliche Datenrevision und jeder Bildhash sind enthalten. Schwierige, leere und illustrierte Seiten bleiben Teil der Stichprobe.

6. **Haben alle 100 funktioniert?** Alle 100 erhielten Parse-Aufrufe. Endbilanz:95 vollständige Textseiten,1 teilweise Tafel,3 visuell bestätigte leere Blätter und 1 textloser Umschlag. Die 98 akzeptierten vollständigen Antworten enthalten 3 reine Layout-Ausgaben; Annahme war nie perfekte OCR.

7. **Wie wird Extraktionsqualität gemessen?** Geprüft werden Hashes, Herkunft, Abschneiden und ausgewählte Scanvergleiche. Drei leere normalisierte Ausgaben wurden anhand ihrer Bilder als leer bestätigt. Eine vollständig menschlich annotierte Zeichenfehlerrate oder Lesereihenfolgengenauigkeit wurde nicht gemessen.

8. **Warum reicht der Titel nicht?** Vollständige Artikel kommen aus dem fixierten Snapshot und werden per Hash geprüft. Layoutsteuerzeichen werden nur für Modelleingaben entfernt, danach folgen Embed, LanceDB und Rerank. Ein verifizierter Artikel mit exakt passendem Titel aus demselben Snapshot ergänzt schwachen BM 25-Rücklauf. Rohzitate bleiben unverändert.

9. **Wie hoch ist die Matching-Genauigkeit?** Eine belastbare Genauigkeit gegen gelabelte Referenzdaten fehlt. Kandidatenwerte, Abstände, Mehrdeutigkeit, Abdeckung und geprüfte Beispiele werden getrennt ausgewiesen. Der 100-Seiten-Lauf und Wiederholungen bewahren Fehler; erfolgreiche API-Aufrufe werden nicht als Genauigkeit ausgegeben.

10. **Welche Rolle hat LanceDB?** LanceDB speichert eigene Dokumente und Vektoren; der gemeinsame BM 25-Index ist getrennt. Native Azure Blob-Schreibvorgänge wurden geprüft, weil Azure Files keine sicheren Lance-Commits unterstützt. Der frühe 183-Dokumente-/Null-Vektoren-Test ist historisch; spätere Zählungen haben eigene Belege.

11. **Welche Vergleiche berechnet ihr?** Wir berechnen Jaccard-Überlappung, Jensen–Shannon-Divergenz und Worthäufigkeiten. Sie beschreiben Textverteilungen, keine historische Wahrheit. OCR, häufige Wörter, Länge und Themenumfang können dominieren. BERTopic war optional; ein Lauf wird nicht behauptet.

12. **Warum ist Hermes hier ein Agent?** Hermes führt eine echte modellgesteuerte Werkzeugschleife aus: Super VL ruft die einzige lesende Belegfunktion auf, erhält begrenzte Abschnitte und gibt IDs in strukturierten Aussagen zurück. Die Spur bleibt erhalten. Es gibt keine Shell-, Dateisystem- oder Browserwerkzeuge; anschließend prüft deterministischer Code die Quellen.

13. **Wie verhindert ihr erfundene Zitate?** Nur angebotene Abschnitts-IDs dürfen gewählt werden. Der Server bindet sie an unveränderliche Zitate und Unicode-Positionen und führt den strikten Prüfer aus. Unbekannte IDs, Überschreibungen und Ein-Korpus-Zitate scheitern. Inhaltliche Unterstützung wird separat geprüft.

14. **Welche Fehlerfälle gibt es?** Die drei ausgewählten Fehler betreffen breite Fragen zu Schiffbau, Maßeinheiten und Bleiche: schwacher Rücklauf, Politik statt Definitionen und korrupte OCR verhinderten brauchbare vollständige Vergleiche. Fehlende Seite, unmögliche GPS-Frage und Instruktionsangriff bleiben ebenfalls dokumentiert. Spätere begrenzte Erfolge löschen nichts.

15. **Wie behandelt ihr Prompt-Injektion?** OCR und gefundener Text bleiben nicht vertrauenswürdige Daten. Der Agent erhält keine Anbieterschlüssel und besitzt nur ein begrenztes Lesewerkzeug. Echte Instruktionsangriffe führten zu Enthaltung; Regressionstests weisen fremde Belege ab. Das beweist einzelne Schutzmaßnahmen, keine allgemeine Immunität.

16. **Was funktioniert öffentlich tatsächlich?** Die gespeicherte öffentliche Basisprüfung bestätigte Astra-Streaming, sieben Quellen, Steuerung, Abbruch, gespeicherte Ereignisse und Abmeldung. Der Vier-Modell-Hermes-Ablauf hat getrennte echte Lauf- und Fallbelege. Seine öffentliche Abnahme ist eine eigene Versionsprüfung und folgt nicht automatisch aus Astra.

17. **Welche multimodalen Funktionen sind geprüft?** Öffentliche Endpunkte lieferten ein echtes PNG und erteilten eine Realtime-Sitzung. Eine Sitzung belegt weder Mikrofonaufnahme noch Wiedergabe oder fertigen Sprachdialog. Physische audiovisuelle Interaktion und Diarisierung werden ohne eigene aktuelle Abnahme nicht behauptet.

18. **Wie sind Betrieb und Sicherheit aufgebaut?** Sechs Dienste laufen auf Azure, nur Web ist öffentlich; die vorgeschriebene Suchinferenz läuft auf Nebius. Anbieterschlüssel bleiben in Core. Geprüfte Geheimnisscans sind sauber. Administrative PostgreSQL-Laufzeitrolle und flüchtiger Covenant-Verlauf bleiben Grenzen; keine Produktions- oder LTS-Freigabe.

19. **Was würdet ihr verbessern?** Prioritäten sind unabhängige Relevanzlabels, OCR- und Eintragssegmentierung, Kalibrierung, robuste breite Fragen und eine eingeschränkte Datenbankrolle. Die leeren Blätter zeigen, weshalb Transporterfolg und nutzbarer Inhalt getrennt geprüft werden müssen.

20. **Ist das Projekt fertig und eingereicht?** Drei begrenzte Fälle wurden vom Assistenten auf Quellenstützung geprüft; drei echte Fehler sind erhalten. Die Stichprobe besitzt eigene Bilanz und Wiederholungsbelege; unabhängige menschliche Zertifizierung fehlt. Code und Video sind keine Eingangsbestätigung. Die Frist war 18. Oktober 2026 um 18:30 MESZ; Verlängerung und Annahme sind ungeprüft.

Belege: `submission-guide/evidence/source-review.json`; Hermes `evidence/100-page-extraction.json`, `page-visual-review.json`, `six-case-evaluation.json`, `azure-blob-runtime-probe.json`; Backend `verification/public-acceptance.json`, `public-multimodal.json`; IaC `verification/security-deployment-review.json`. Repository-Pfade: `submission-guide/repository-map.json`. Aktueller Beleg, Implementierung und Planung bleiben getrennt.

`Hermes/evidence/reviewed-six-cases.json`; `Hermes/evidence/live-nemotron-matching-20261018T1742Z/progress.json`; `core/verification/nebius-model-deployment/core-retrieval-live.json`; `core/verification/nebius-model-deployment/gpu-models-live.json`.

Endgültige semantische Einteilung:95 Parse-Textseiten,1 teilweise astronomische Tafel(Zeile2243),3 leere Blätter(Zeilen374,1615,2077) und1 textloser Umschlag(Zeile452)=100 Originalseiten. Alle drei leeren Bilder wurden visuell geprüft. Die98 akzeptierten vollständigen Parse-Antworten enthalten diese3 Layout-Ausgaben; Annahme bedeutet weder Prosa noch OCR-Genauigkeit. Originalbelege bleiben erhalten. `Hermes/evidence/page-content-classification.json` enthält100 Identitäten und Hashes.


Alle 100 Originalseiten sind bilanziert. Echte semantische Suche wurde für 96 Text- oder Teilseiten abgeschlossen:23 Kandidatenergebnisse und 73 mehrdeutige Ergebnisse. Drei leere Blätter und ein textloser Umschlag bleiben ohne Zuordnung; die teilweise astronomische Tafel gehört zu den 96. Ursprüngliche Fehler und gezielte Wiederholungen bleiben erhalten. Diese Zahlen sind keine gemessene Zuordnungsgenauigkeit.

`Hermes/evidence/100-page-semantic-summary.json` · `Hermes/evidence/100-page-semantic-ledger.csv` · `Hermes/evidence/page-content-classification.json`

[Dokumentationsübersicht](README.md) · [Einrichtungsanleitung](../../README.md) · [Quellen- und Exportprüfung](source-review.json)
