# Hub-Repo: AI Product Manager Portfolio

## Zweck
Dieses Repo ist die GitHub-Pages-Hub-Seite für ein Portfolio angewandter
AI-Projekte mit Product-Management-Perspektive.

## Wie die Page entsteht
.github/workflows/build-page.yml sammelt automatisch (Cron + manueller Trigger)
alle Repos des Users mit Topic ai-pm-portfolio, liest deren meta.json und
generiert daraus index.html. index.html nicht von Hand pflegen — sie wird
bei jedem Lauf überschrieben.

## Namenskonvention für Use-Case-Repos
ai-uc-NN-kurzname (z.B. ai-uc-01-ticket-classification). Jedes trägt das Topic
ai-pm-portfolio (unter Topics, nicht im Website-Feld) und eine meta.json mit
Status ausschließlich: planned | active | done.

## meta.json (Englisch, speist die Karten)
- title, summary (ein Satz „what it shows“), status, tags
- metrics: 1–2 Kennzahlen wörtlich aus dem README
- optional demo {url, note}, z.B. note "access code on request"
- optional screenshot: Pfad im Repo, wird über raw.githubusercontent.com eingebunden
Reihenfolge der Karten: Status, dann Repo-Name (UC-Nummer).

## README-Schema (in jedem Use-Case-Repo)
Problem → PM-Entscheidung (abgewogene Optionen) → Architekturskizze →
Evaluationsergebnisse → Kosten/Latenz → Learnings → was ich anders machen würde.
Das PM-Artefakt (Entscheidung, Begründung) ist der eigentliche Deliverable —
der Code ist der Beleg, nicht der Star.

## Sprache in öffentlich sichtbaren Texten
Hub-Page komplett auf Englisch. In jedem Use-Case-Repo: README.md auf Englisch,
README_DE.md auf Deutsch, inhaltlich identisch, oben jeweils Sprachlink
(🇩🇪 Deutsche Version / 🇬🇧 English version).
READMEs und Hub-Page lesen sich wie Fallstudien abgeschlossener Projekte, nicht
wie Kursmaterial. Begriffe wie "Lernpfad", "Woche X", "Übung" oder "Curriculum"
gehören nicht in öffentlich sichtbaren Text.

## Neue Use-Case-Repos anlegen
Über "Use this template" auf dem Repo ai-uc-template, nicht von Hand kopieren.

Pflichtpunkte beim Anlegen (gilt ab UC8):
- GitHub-Topic ai-pm-portfolio gesetzt (gh repo edit <repo> --add-topic ai-pm-portfolio).
  Ohne Topic überspringt build-page.yml das Repo, und es erscheint keine Karte
  (so ist UC6 zunächst gefehlt).
