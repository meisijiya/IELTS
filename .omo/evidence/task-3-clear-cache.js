# Task 3 Evidence: docs/assets/js/clear-cache.js

## File
- Path: `docs/assets/js/clear-cache.js`
- Lines: 20 (≤ 20 required)
- Status: Untracked (created this run; orchestrator will batch-commit)

## Source content
```js
(function () {
  'use strict';
  document.addEventListener('DOMContentLoaded', () => {
    const btn = document.querySelector('button.clear-cache-btn');
    if (!btn) return;
    btn.addEventListener('click', () => {
      const keys = [];
      try {
        for (let i = 0; i < localStorage.length; i++) {
          const k = localStorage.key(i);
          if (k && k.startsWith('ielts-')) keys.push(k);
        }
      } catch (e) { /* ponytail: localStorage may be disabled */ }
      keys.forEach(k => localStorage.removeItem(k));
      btn.textContent = '已清除 ✓';
      btn.classList.add('cleared');
      setTimeout(() => { btn.textContent = '清除缓存'; btn.classList.remove('cleared'); location.reload(); }, 2000);
    });
  });
})();
```

## Acceptance checks
| Check | Command | Expected | Actual | |
|---|---|---|---|---|
| Line count | `wc -l docs/assets/js/clear-cache.js` | ≤ 20 | 20 | PASS |
| Prefix filter | `grep -c "startsWith('ielts-')" docs/assets/js/clear-cache.js` | ≥ 1 | 1 | PASS |
| Reload call | `grep -c "location.reload" docs/assets/js/clear-cache.js` | ≥ 1 | 1 | PASS |

## Must-NOT checks
| Check | Expected | Actual | |
|---|---|---|---|
| `var` usage | 0 | 0 | PASS |
| `localStorage.clear()` usage | 0 | 0 | PASS |
| `alert(` / `confirm(` usage | 0 | 0 | PASS |

## Must-DO checks
| Check | Status | |
|---|---|---|
| IIFE wrapper | present (line 1 + line 20) | PASS |
| `'use strict';` | present (line 2) | PASS |
| `DOMContentLoaded` listener | present (line 3) | PASS |
| No-op when button missing | `if (!btn) return;` (line 5) | PASS |
| Try/catch around localStorage iteration | present (lines 8–13) | PASS |
| Explicit `for (let i = 0; i < localStorage.length; i++)` | present (line 9) | PASS |
| `localStorage.key(i)` (not `Object.keys`) | present (line 10) | PASS |
| Collect-first-then-remove | `const keys = []` then `keys.forEach(removeItem)` | PASS |
| Only `ielts-` prefix | `k.startsWith('ielts-')` (line 11) | PASS |
| Text feedback `'已清除 ✓'` | present (line 15) | PASS |
| `.cleared` class added | `btn.classList.add('cleared')` (line 16) | PASS |
| `setTimeout(..., 2000)` with reload | present (line 17) | PASS |
| `location.reload()` invoked | present (line 17) | PASS |
| Reset text + remove class before reload | present in same setTimeout (line 17) | PASS |

## Spec deltas vs. `.omo/drafts/design-preview.html:607–630`
- Selector: `button.clear-cache-btn` (class selector matching `<button class="clear-cache-btn">`) vs. the preview's `getElementById('clearBtn')`. Preview was a demo; production uses class selector per spec.
- Adds try/catch around localStorage iteration per MUST-DO.
- Preview omits `location.reload()` (commented out to avoid interrupting the demo); production calls it.
- Compressed `setTimeout` body to one line to fit the line budget while keeping the for-loop readable.

## Design notes
- Reversed `for...in` / `Object.keys(localStorage)` traps avoided by using the explicit indexed loop and capturing keys into a fresh array before removal.
- Ponytail comment on the `catch` documents the deliberate simplification: localStorage can throw in private mode / quota-exceeded; the user-facing button will silently no-op rather than surface an error.