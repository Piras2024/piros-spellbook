---
name: html-report
description: >
  Write an analysis, comparison, or findings document as a self-contained
  dark-theme HTML report from the html-report template: TL;DR callout,
  provenance meta line, tabular-nums tables, pos/neg deltas and a findings
  callout. Use when asked to write, render, or restyle a report or document
  as HTML, when a completed analysis should become a shareable report page,
  or when the user asks for "the usual report style".
---

# html-report

One file: copy `template.html` (next to this file) to `<subject>-report.html` where the data being reported on lives, and fill it in. Kebab-case subject, `-report` suffix. This file and `template.html` describe the same contract: when one changes, change the other in the same edit.

Document order, matching the template slots:

1. `<title>` + `<h1>` — specific title: names the subject and what is compared or measured.
2. `<p class="tldr">` — one paragraph with leading `<strong>TL;DR.</strong>`, in four movements: **change** (what was done, one sentence), **outcome** (whether it worked), **evidence** (who or what moved by how much, with the numbers), **caveat** (the one problem observed, with its cause and impact). Secondary status (pending commits, ops notes) and mechanism details stay out — they live in the sections.
3. Intro `<p>` — scope and comparability of the data.
4. `<p class="meta">` — provenance, clauses joined by `&middot;`: source system with id, generation date, data origin, links to the underlying artifacts, sibling reports.
5. Numbered `<h3> N. Name</h3>` sections — each a table plus a one-line reading, or bold-lead bullets (`<li><strong>Claim.</strong> Evidence with numbers, quotes, links.</li>`).
6. `<div class="callout">` — numbered bold-lead findings, then a `<p><strong>Final considerations.</strong> …</p>` with the open points worth attention.
7. `<footer>` — optional: delete it, or point it at the real source of the content.

Conventions: every claim is backed by a number, a quote, or a link. Numeric table columns carry `class="num"` on their `th`/`td`; wrap positive values in `<span class="pos">`, negative in `<span class="neg">`, bold them when they are the headline. Use `&mdash;` `&rarr;` `&middot;` `&Delta;` `&minus;` `&hellip;`. Inline links to sibling reports as `./sibling-name.html`.

Named subjects the report compares in repeated mentions (pairs, variants, cohorts) get a legend: a numbered subsection near the top whose table links the compared artifacts themselves — the actual tasks compared, not adjacent records like their parent offer — with an `id` anchor per subject; every later mention of a subject name links back to that anchor. An inline meta line is not a legend.

Frame history as it is: a bug that was discovered, compared against the original recorded values — never an invented era like "pre-incident" — and label problems plainly ("Problema osservato"), not as reservations ("riserva").

Keep the template's CSS untouched: the look is the contract (the `[id] { scroll-margin-top: 50vh; }` rule ships in the template so internal anchors land mid-viewport, not flush at the top — keep it). The page must stay self-contained — no external scripts, fonts, or stylesheets.

Done when: all template slots are filled or deleted, numeric columns carry `class="num"`, deltas carry `pos`/`neg`, and the HTML opens standalone from `file://`.
