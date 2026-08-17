---
id: T-005
goal: Task 1 essay 01 (Static table — universities ranked top 200) renders with 三件套 + embedded chart.
files:
  - docs/writing/task1/01-table-universities-ranked.html
  - docs/assets/images/task1-charts/01-table-universities-ranked.png
deps: [T-002, T-004]
ac:
  - REQ-essay-content-scenario-task1-essay-coverage
  - REQ-essay-content-scenario-chart-data-not-fabricated
evidence: essay page committed; grep confirms `data-task="task1"`, `data-difficulty="easy"`, `data-type="static-graph"`; `wc -w` on the essay body shows 170–190; chart image extracted to docs/assets/images/task1-charts/.
size: S
status: ready-for-agent
created: 2026-08-15
feature: ielts-writing-site-stage1a
---

## What to build

A single Task 1 essay HTML page covering the Static table question about universities ranked top 200 in three subjects across five countries (date 2026.2.7, see `.omo/plans/stage1a.md` P4 row #01).

Page structure:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Task 1 — Universities ranked top 200 | IELTS Writing 6-band samples</title>
  <link rel="stylesheet" href="../../assets/css/style.css">
</head>
<body>
  <article data-task="task1" data-difficulty="easy" data-type="static-graph">
    <nav class="crumbs">… breadcrumb …</nav>
    <section class="prompt">… question text from docx …</section>
    <figure>
      <img src="../../assets/images/task1-charts/01-table-universities-ranked.png" alt="Table showing universities ranked top 200 in three subjects across five countries">
    </figure>
    <section class="essay">… English essay (170–190 words, 6-band-clean) …</section>
    <section class="rubric">… Chinese 1–2 paragraph TA/CC/LR/GRA note …</section>
    <section class="keywords">… 5–10 keyword / synonym list …</section>
  </article>
</body>
</html>
```

Chart data must come from `Task 1 冲刺(1).docx`: extract the embedded image with `python-docx` (`doc.part.rels`), save it as PNG to `docs/assets/images/task1-charts/01-table-universities-ranked.png`, and read the image with the multimodal reader to obtain the actual numbers. **Numbers in the essay body must match the chart image; BLOCKED if any key number is unreadable.**

## Acceptance criteria

- [ ] File exists at `docs/writing/task1/01-table-universities-ranked.html`.
- [ ] Root `<article>` carries `data-task="task1"`, `data-difficulty="easy"`, `data-type="static-graph"`.
- [ ] `<img>` element points to `../../assets/images/task1-charts/01-table-universities-ranked.png` and the image file exists.
- [ ] English essay body word count (excluding tags) is 170–190.
- [ ] Chinese TA/CC/LR/GRA note present (1–2 paragraphs).
- [ ] Keyword list present (5–10 items, `<code>` wrapped).
- [ ] Every numeric figure in the essay body is visible in the source chart image (trace in evidence log).

## Verification

- [ ] `grep -E 'data-task="task1"|data-difficulty="easy"|data-type="static-graph"' docs/writing/task1/01-table-universities-ranked.html` returns 3 hits.
- [ ] `python3 -c "import re; t=open('docs/writing/task1/01-table-universities-ranked.html').read(); body=re.search(r'<section class="essay">(.*?)</section>', t, re.S).group(1); print(len(body.split()))"` prints a value in 170..190.
- [ ] `test -f docs/assets/images/task1-charts/01-table-universities-ranked.png` exits 0.
- [ ] `grep -E '[0-9]+%|[0-9]+ (countries|universities|subjects)' docs/writing/task1/01-table-universities-ranked.html` shows numbers cross-checked against chart image (build agent records the comparison in commit message or evidence note).

## Files in scope

- `docs/writing/task1/01-table-universities-ranked.html` (create).
- `docs/assets/images/task1-charts/01-table-universities-ranked.png` (create via docx extraction).

## Files out of scope

- `Task 1 冲刺(1).docx` (read-only).
- Other Task 1 essay pages (T-006..T-009).

## BLOCKED condition

If any key number in the chart image is unreadable, mark this ticket `blocked`, do **not** write a fabricated essay. Record which number(s) are missing in the ticket evidence log and surface to user via the dispatcher.