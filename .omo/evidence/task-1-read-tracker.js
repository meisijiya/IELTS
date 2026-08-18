# Task 1 — read-tracker.js

## File
`docs/assets/js/read-tracker.js` (43 lines, vanilla JS, IIFE + 'use strict')

## What it does
On `DOMContentLoaded` (1) if the current page has a single `<article data-task>` or `<article data-topic-id>`, marks the page slug as read in `localStorage` under `ielts-read:<module>:<slug>`; (2) for every `<article>` on the page, injects a `<span class="dot">` as the first child (if missing) and toggles `dot-read` / `dot-unread` from the stored value. A single document-level `click` listener toggles the dot and the localStorage key when any article is clicked. All `localStorage` access is wrapped in `try/catch` for private-mode / quota safety; event delegation on `document` keeps the listener count to one; slug for list cards is derived via `new URL(href, location.href).pathname.split('/').pop().replace(/\.html$/, '')` and falls back to the page basename for the detail-page case (no `h3 a`).
