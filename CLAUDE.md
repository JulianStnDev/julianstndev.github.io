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
ai-pm-portfolio und eine meta.json mit Status ausschließlich: planned | active | done.

## README-Schema (in jedem Use-Case-Repo)
Problem → PM-Entscheidung (abgewogene Optionen) → Architekturskizze →
Evaluationsergebnisse → Kosten/Latenz → Learnings → was ich anders machen würde.
Das PM-Artefakt (Entscheidung, Begründung) ist der eigentliche Deliverable —
der Code ist der Beleg, nicht der Star.

## Sprache in öffentlich sichtbaren Texten
READMEs und Hub-Page lesen sich wie Fallstudien abgeschlossener Projekte, nicht
wie Kursmaterial. Begriffe wie "Lernpfad", "Woche X", "Übung" oder "Curriculum"
gehören nicht in öffentlich sichtbaren Text.

## Neue Use-Case-Repos anlegen
Über "Use this template" auf dem Repo ai-uc-template, nicht von Hand kopieren.
