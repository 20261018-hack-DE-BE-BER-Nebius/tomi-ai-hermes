---
id: demo-narration-de
topic: demo-narration
lang: de
title: "Tomi-Sprechtext: dreiminütige Abgabe und erweitertes Interview"
type: guide
status: evidence-draft
updated: "2026-10-18"
tags: [tomi, submission, evidence, de]
---

[EN](demo-narration-en.md) · [ES](demo-narration-es.md) · [DE](demo-narration-de.md) · [FR](demo-narration-fr.md)

> Videostand: Beide finalen Dateien sind in diesem Repository enthalten und lokal verifiziert (Einreichung: 180.000 Sekunden; Rundgang: 279.722656 Sekunden). Unabhängige Sicht- und Technikprüfung bestanden; Hören, Verständlichkeit und Aussprache wurden nicht zertifiziert. Eine Portalabgabe wurde nicht durchgeführt. Die automatische MOV-Transkription ist abgeschlossen (46 Abschnitte, 87 Segmente), Hör- und Treueprüfung bleiben unvollständig.

# Tomi

## Dreiminütige Einreichungsfassung

Tomi verbindet historische Encyclopaedia Britannica mit Wikipedia und zeigt, worauf jeder Vergleich beruht.

Wir wählten hundert Seiten reproduzierbar aus und prüften jeden Bildhash. Alle erhielten echte Nemotron-Parse-Aufrufe. Achtundneunzig vollständige Antworten wurden akzeptiert, darunter drei leere Blätter; eine astronomische Tafel bleibt teilweise, ein Umschlag enthält keine nutzbare Prosa. Akzeptierte OCR bedeutet keine perfekte Abschrift.

Alle vier vorgeschriebenen NVIDIA-Modelle laufen. Embed und Rerank nutzen die zugewiesene Nebius-GPU. LanceDB speichert und durchsucht Vektoren. Nemotron Super VL bedient unser Hermes-Belegwerkzeug über das Rust-Gateway.

Drei begrenzte Ergebnisse sind durch Quellen gestützt: Historische Verbindungsteile bestehen aus Holz, während der moderne Text eine Werft definiert. Beide Quellen verbinden den Liter mit einem Kubikdezimeter. Das Bleichbeispiel vergleicht historische Gefäße und Gas mit dem modernen Ziel, Farbe zu entfernen.

Die ersten breiten Fragen scheiterten. Die Suche lieferte Schiffbauunternehmen, Maßpolitik verdrängte Einheitendefinitionen, und verrauschte OCR erlaubte keinen vollständigen Prozessvergleich. Diese echten Fehler bleiben neben den erfolgreichen begrenzten Fragen erhalten.

Hermes wählt nur angebotene Belegabschnitte. Der Server bindet sie an genaue Zitate und Unicode-Positionen. Ungültige Zitate werden abgewiesen. Auch gültige Zitate benötigen eine inhaltliche Quellenprüfung; sie machen eine Aussage nicht automatisch wahr.

Alle 100 Originalseiten sind bilanziert. Echte semantische Suche wurde für 96 Text- oder Teilseiten abgeschlossen:23 Kandidatenergebnisse und 73 mehrdeutige Ergebnisse. Drei leere Blätter und ein textloser Umschlag bleiben ohne Zuordnung; die teilweise astronomische Tafel gehört zu den 96. Ursprüngliche Fehler und gezielte Wiederholungen bleiben erhalten. Diese Zahlen sind keine gemessene Zuordnungsgenauigkeit.

Das kompilierte Archiv enthält hundert Quelldokumente auf 187 PDF-Seiten. Die mehrsprachige Anwendung zeigt Quellen und Werkzeugaktivität; öffentliche Tests bestätigten Streaming, Steuerung, Abbruch und gespeicherte Ereignisse.

Tomi macht nützliche Antworten prüfbar und bewahrt die Gründe für Fehler.

## Erweiterte Interviewfassung

Tomi vergleicht historische Encyclopaedia Britannica mit Wikipedia. Ziel ist, Belege und Unsicherheit prüfbar zu machen, statt eine flüssige Antwort als ausreichenden Nachweis zu behandeln.

Wir wählten hundert Seiten mit einem reproduzierbaren Manifest und prüften ihre Bildhashes. Jedes Bild erhielt einen echten Nemotron-Parse-3.5-Aufruf. Achtundneunzig vollständige Antworten wurden ohne Abschneiden akzeptiert, darunter drei leere Blätter mit ausschließlich Layoutsteuerzeichen. Eine astronomische Tafel benötigte Ausschnitte und bleibt teilweise; ein Umschlag enthält keine nutzbare Prosa. Alle Identitäten und Fehlversuche bleiben erhalten. Das belegt Extraktionsergebnisse, keine zertifizierte OCR-Genauigkeit.

Die vorgeschriebene Pipeline nutzt jetzt alle vier NVIDIA-Modelle. Kandidaten stammen aus dem fixierten Wikimedia-Snapshot, mit vollständigem Text, Revision und geprüften Hashes. Embed repräsentiert Inhalte, LanceDB speichert und durchsucht Vektoren, Rerank bewertet Relevanz. Beide Suchmodelle laufen auf unserer zugewiesenen Nebius-GPU. Super VL betreibt das echte Hermes-Belegwerkzeug über das Rust-Gateway. Anbieterzugangsdaten bleiben in Core.

Drei begrenzte Vergleiche bestanden eine Quellenprüfung durch den Assistenten. Der Schiffbaufall vergleicht historische Holzteile mit der modernen Werftdefinition. Der Messfall verbindet den Liter in beiden Texten mit dem Kubikdezimeter. Die Antwort normalisiert das Kubikzeichen typografisch, während Rohzitate exakt bleiben. Der Bleichfall vergleicht historische Gefäße und Gas mit dem modernen Entfärbungszweck. Es sind begrenzte Beobachtungen, keine pauschalen Aussagen über wissenschaftlichen Fortschritt.

Die früheren breiten Fragen scheiterten. Schiffbausuche bevorzugte Unternehmen, Messkandidaten beschrieben Politik statt Definitionen und die verrauschte Bleich-OCR erlaubte keinen vollständigen Technikvergleich. Diese Fehler und spätere begrenzte Fragen bleiben mit ausdrücklichen Suchthemen und Modellspuren erhalten. Eine unabhängige menschliche Zertifizierung wird nicht behauptet.

Auch Zitierfehler wurden reproduziert. Das reparierte Werkzeug bietet unveränderliche Abschnittskennungen an. Super VL wählt Kennungen; der Server bindet sie an exakte Zitate und Unicode-Positionen und nutzt denselben strikten Prüfer. Unbekannte Kennungen, Überschreibungen und Belege nur eines Korpus scheitern. Mechanische Gültigkeit benötigt weiter eine inhaltliche Prüfung. Die ursprüngliche Frage bleibt von der Suchfrage getrennt, damit der gewünschte Umfang erhalten bleibt.

Alle 100 Originalseiten sind bilanziert. Echte semantische Suche wurde für 96 Text- oder Teilseiten abgeschlossen:23 Kandidatenergebnisse und 73 mehrdeutige Ergebnisse. Drei leere Blätter und ein textloser Umschlag bleiben ohne Zuordnung; die teilweise astronomische Tafel gehört zu den 96. Ursprüngliche Fehler und gezielte Wiederholungen bleiben erhalten. Diese Zahlen sind keine gemessene Zuordnungsgenauigkeit. Relevanzlogits sind keine Wahrheitswahrscheinlichkeiten; eine Genauigkeit gegen gelabelte Referenzdaten liegt nicht vor. Wortschatz und normalisierte Häufigkeiten beschreiben Texte, werden aber durch OCR und unterschiedliche Abdeckung begrenzt.

Das Archiv enthält kompilierte PDFs für hundert Quelldokumente auf 187 Seiten, bearbeitbares LaTeX und einen statischen Viewer. Die Anwendung unterstützt vier Sprachen. Öffentliche Tests bestätigten Streaming, Steuerung, Abbruch, gespeicherte Ereignisse und Abmeldung. Bildgenerierung und Realtime-Sitzungsausgabe wurden geprüft, physisches Mikrofon und Wiedergabe nicht.

Sechs Dienste laufen auf Azure, nur die Webanwendung ist öffentlich. Native Azure-Blob-Speicherung ermöglicht LanceDB-Schreibvorgänge. Offene Grenzen sind die administrative Datenbankrolle und die Zuverlässigkeit breiter Fragen. Es ist ein funktionierender, prüfbarer Ablauf mit Erfolgen und Fehlern, keine Zusage für jede Quelle oder Frage.

## Produktions- und Nachweisgrenzen

Das Teilnehmer-PDF verlangt drei Minuten. Die enthaltenen finalen Videos dauern 180.000 und 279.722656 Sekunden und besitzen passende Hashes sowie vollständige Dekodierbelege. Das englische erweiterte Vorbereitungsskript bleibt unter600Wörtern. Alle vier vorgeschriebenen Modelle sind tatsächlich ausgeführt; der öffentliche Nemotron-Vergleich endete mit sieben Quellen und Prüfhinweis. Die vollständige Stichprobe ist mit ausdrücklicher Mehrdeutigkeit bearbeitet. Die sechs Fälle prüfte der Assistent; unabhängige menschliche Zertifizierung steht aus. Portalabgabe, Preis oder physische Audiotreue werden nicht behauptet.

[submission-guide-de](submission-guide-de.md) · [interview-preparation-de](interview-preparation-de.md)

`Hermes/evidence/reviewed-six-cases.json` · `Hermes/evidence/live-nemotron-matching-20261018T1742Z/progress.json` · `Hermes/archive/assets/compile-receipt.json`

Endgültige semantische Einteilung:95 Parse-Textseiten,1 teilweise astronomische Tafel(Zeile2243),3 leere Blätter(Zeilen374,1615,2077) und1 textloser Umschlag(Zeile452)=100 Originalseiten. Alle drei leeren Bilder wurden visuell geprüft. Die98 akzeptierten vollständigen Parse-Antworten enthalten diese3 Layout-Ausgaben; Annahme bedeutet weder Prosa noch OCR-Genauigkeit. Originalbelege bleiben erhalten. `Hermes/evidence/page-content-classification.json` enthält100 Identitäten und Hashes.


Alle 100 Originalseiten sind bilanziert. Echte semantische Suche wurde für 96 Text- oder Teilseiten abgeschlossen:23 Kandidatenergebnisse und 73 mehrdeutige Ergebnisse. Drei leere Blätter und ein textloser Umschlag bleiben ohne Zuordnung; die teilweise astronomische Tafel gehört zu den 96. Ursprüngliche Fehler und gezielte Wiederholungen bleiben erhalten. Diese Zahlen sind keine gemessene Zuordnungsgenauigkeit.

`Hermes/evidence/100-page-semantic-summary.json` · `Hermes/evidence/100-page-semantic-ledger.csv` · `Hermes/evidence/page-content-classification.json`

[Dokumentationsübersicht](README.md) · [Einrichtungsanleitung](../../README.md) · [Quellen- und Exportprüfung](source-review.json)
