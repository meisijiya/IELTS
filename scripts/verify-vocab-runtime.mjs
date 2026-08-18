#!/usr/bin/env node
/* Final verification wave — RUNTIME checks for docs/vocab (F4, F7, F8).
 * Loads vocab.js in jsdom, drives the real UI, asserts behavior.
 * Exits 0 only if all 3 verifiers PASS.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const VOCAB_DIR = path.join(ROOT, 'docs', 'vocab');
const LOG_FILE = path.join(ROOT, '.omo', 'evidence', 'final-wave-runtime.log');
const ISSUES_FILE = path.join(ROOT, '.omo', 'notepads', 'five-modules-expansion', 'issues.md');

const SOURCE_IDS = ['speaking-p1', 'listening', 'cambridge', 'kaodian538', 'writing'];

let JSDOM, VirtualConsole;
try {
  ({ JSDOM, VirtualConsole } = await import('jsdom'));
} catch (e) {
  console.error('[FATAL] jsdom not installed. Run: npm install --no-save jsdom');
  process.exit(2);
}

const warnings = [];
const errors = [];
const vc = new VirtualConsole();
vc.on('warn', (...a) => warnings.push(a.map(String).join(' ')));
vc.on('error', (...a) => errors.push(a.map(String).join(' ')));
vc.on('jsdomError', (e) => errors.push('jsdomError: ' + (e.message || String(e))));

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function waitFor(fn, timeout = 5000, interval = 20) {
  const start = Date.now();
  while (!fn()) {
    if (Date.now() - start > timeout) throw new Error('waitFor timeout');
    await sleep(interval);
  }
}

function buildDom() {
  const html = fs
    .readFileSync(path.join(VOCAB_DIR, 'index.html'), 'utf8')
    .replace(/<script[^>]*vocab\.js[^>]*><\/script>/, '');
  const dom = new JSDOM(html, {
    runScripts: 'dangerously',
    url: 'http://localhost/docs/vocab/index.html',
    virtualConsole: vc,
  });
  const { window } = dom;
  // vocab.js calls fetch('./data/<id>.json') — serve from local filesystem.
  window.fetch = async (url) => {
    const name = String(url).split('/').pop();
    const file = path.join(VOCAB_DIR, 'data', name);
    const body = await fs.promises.readFile(file, 'utf8');
    return { ok: true, status: 200, json: async () => JSON.parse(body) };
  };
  return dom;
}

async function boot() {
  const dom = buildDom();
  const { window } = dom;
  // Let DOMContentLoaded fire BEFORE eval so vocab.js's listener never double-inits.
  let loaded = false;
  window.document.addEventListener('DOMContentLoaded', () => { loaded = true; });
  await waitFor(() => loaded, 2000);
  const vocabSource = fs.readFileSync(path.join(VOCAB_DIR, 'assets', 'js', 'vocab.js'), 'utf8');
  window.eval(vocabSource);
  const VocabApp = window.VocabApp;
  if (!VocabApp) throw new Error('window.VocabApp not exposed');
  await VocabApp.init();
  await waitFor(() => Object.keys(VocabApp.STATE.vocabData).length === SOURCE_IDS.length, 5000);
  return { dom, window, VocabApp };
}

async function typeSpell(window, value, wait = 200) {
  const input = window.document.getElementById('spell-input');
  input.value = value;
  input.dispatchEvent(new window.Event('input', { bubbles: true }));
  await sleep(wait);
}

// ---- F4: spell happy/failure/empty/case-insensitive across 5 docs ----
async function checkF4(window, VocabApp) {
  const sub = [];
  for (const docId of SOURCE_IDS) {
    VocabApp.setDoc(docId);
    VocabApp.setMode('spell');
    const item = VocabApp.STATE.items.find((i) => i.english && i.english.trim());
    if (!item) { sub.push(false, false, false, false); continue; }
    const input = window.document.getElementById('spell-input');
    const feedback = window.document.getElementById('spell-feedback');

    await typeSpell(window, item.english); // happy
    sub.push(
      input.classList.contains('correct') &&
      (feedback.innerHTML.includes('拼写正确') || feedback.innerHTML.includes('✓'))
    );

    await typeSpell(window, item.english + 'X'); // failure
    sub.push(
      input.classList.contains('wrong') &&
      (feedback.innerHTML.includes('char-wrong') || feedback.innerHTML.includes('<code>'))
    );

    await typeSpell(window, ''); // empty
    sub.push(!input.classList.contains('correct') && !input.classList.contains('wrong'));

    await typeSpell(window, item.english.toUpperCase()); // case-insensitive
    sub.push(input.classList.contains('correct'));
  }
  return sub; // 20
}

// ---- F7: localStorage write/read/reset + 500KB guard ----
async function checkF7(window, VocabApp) {
  const sub = [];
  window.localStorage.clear();
  VocabApp.ProgressStore.load();
  VocabApp.renderStats();
  const statsTotal = window.document.getElementById('stats-total');

  // 1. first-visit state
  sub.push(statsTotal.textContent === '尚未开始' || statsTotal.textContent === '0');

  // 2. correct + wrong on different items → persisted JSON + non-zero stats
  VocabApp.setDoc('speaking-p1');
  VocabApp.setMode('spell');
  const items = VocabApp.STATE.items;
  await typeSpell(window, items[0].english);       // correct
  VocabApp.nextItem();
  await typeSpell(window, items[1].english + 'X'); // wrong
  await sleep(600); // save() debounce is 500ms
  const stored = window.localStorage.getItem('ielts-vocab:progress');
  let parsedOk = false;
  try { parsedOk = stored != null && Object.keys(JSON.parse(stored)).length > 0; } catch {}
  sub.push(
    parsedOk &&
    statsTotal.textContent !== '尚未开始' && statsTotal.textContent !== '0'
  );

  // 3. reset via modal → cleared
  window.document.getElementById('stats-reset').click();
  await sleep(50);
  const modal = window.document.querySelector('.vocab-reset-confirm');
  const modalShown = modal && modal.getAttribute('data-show') === 'true';
  const okBtn = modal && modal.querySelector('[data-reset="ok"]');
  if (okBtn) okBtn.click();
  await sleep(600);
  const afterReset = window.localStorage.getItem('ielts-vocab:progress');
  // reset() persists '{}' (empty object), not null — both mean "cleared".
  sub.push(modalShown && (afterReset === null || afterReset === '{}'));

  // 4. 500KB guard: 5000 fake entries must not crash; warning must fire
  const cache = VocabApp.ProgressStore._cache;
  for (let i = 0; i < 5000; i++) {
    cache['doc' + (i % 5) + '::cat::item' + i] = {
      correct: 0, wrong: 1,
      firstSeen: '2026-08-18T00:00:00.000Z',
      lastSeen: '2026-08-18T00:00:00.000Z',
    };
  }
  const warnBefore = warnings.length;
  VocabApp.ProgressStore.save();
  await sleep(600);
  const big = window.localStorage.getItem('ielts-vocab:progress');
  const warned = warnings.slice(warnBefore).some((w) => w.includes('500KB'));
  sub.push(big != null && big.length > 0 && warned);

  return sub; // 4
}

// ---- F8: 「未掌握」tab content ----
async function checkF8(window, VocabApp) {
  const sub = [];
  window.localStorage.clear();
  VocabApp.ProgressStore.load();
  VocabApp.renderStats();

  // setup: wrong on 3 distinct items of speaking-p1; item0 wrong twice (wrong=2)
  VocabApp.setDoc('speaking-p1');
  VocabApp.STATE.currentIndex = 0; // setDoc early-returns on same doc; force index 0
  VocabApp.setMode('spell');
  const spItems = VocabApp.STATE.items;
  await typeSpell(window, spItems[0].english + 'X'); // wrong item0
  VocabApp.nextItem();
  await typeSpell(window, spItems[1].english + 'X'); // wrong item1
  VocabApp.nextItem();
  await typeSpell(window, spItems[2].english + 'X'); // wrong item2
  VocabApp.prevItem(); VocabApp.prevItem();          // back to item0
  await typeSpell(window, spItems[0].english + 'X'); // wrong item0 again → wrong=2
  await sleep(600);

  const unmasteredTab = window.document.querySelector('#mode-tabs [data-mode="unmastered"]');
  const list = window.document.getElementById('unmastered-list');

  // 1. 3 cards
  unmasteredTab.click();
  let cards = [...list.querySelectorAll('.vocab-card')];
  sub.push(cards.length === 3);

  // 2. sorted by wrongCount desc (matches wrongItems() order; first = wrong=2 item)
  const expected = VocabApp.ProgressStore.wrongItems();
  const actualIds = cards.map((c) => c.getAttribute('data-id'));
  sub.push(
    actualIds.length === expected.length &&
    actualIds.every((id, i) => id === expected[i].item) &&
    actualIds[0] === spItems[0].id
  );

  // 3. source-doc chips
  const chips = cards.map((c) => {
    const chip = c.querySelector('.vocab-source-chip');
    return chip ? chip.getAttribute('data-source') : null;
  });
  sub.push(chips.length === expected.length && chips.every((s, i) => s === expected[i].sourceDoc));

  // 4. doc with NO wrong attempts → empty state
  VocabApp.setDoc('cambridge');
  unmasteredTab.click();
  cards = [...list.querySelectorAll('.vocab-card')];
  sub.push(cards.length === 0 || list.textContent.includes('暂无未掌握词'));

  // 5. back to speaking-p1 → 3 items again
  VocabApp.setDoc('speaking-p1');
  unmasteredTab.click();
  cards = [...list.querySelectorAll('.vocab-card')];
  sub.push(cards.length === 3);

  return sub; // 5
}

// ---- main ----
const { window, VocabApp } = await boot();

const f4 = await checkF4(window, VocabApp);
const f7 = await checkF7(window, VocabApp);
const f8 = await checkF8(window, VocabApp);

const results = [
  {
    id: 'F4', label: '拼写 happy/failure 路径',
    pass: f4.every(Boolean),
    detail: `${SOURCE_IDS.length} docs × 4 sub-checks = ${f4.filter(Boolean).length}/${f4.length}`,
  },
  {
    id: 'F7', label: 'localStorage 写入/读取/重置',
    pass: f7.every(Boolean),
    detail: `${f7.filter(Boolean).length}/${f7.length} sub-checks`,
  },
  {
    id: 'F8', label: '「未掌握」tab 内容正确',
    pass: f8.every(Boolean),
    detail: `${f8.filter(Boolean).length}/${f8.length} sub-checks`,
  },
];

const lines = results.map((r) =>
  `[${r.id}] ${r.label} ... ${r.pass ? 'PASS' : 'FAIL'} (${r.detail})`
);
const allPass = results.every((r) => r.pass);

// F8 sub-check 4 finding → issues.md (verifier only, no vocab.js edits)
if (!f8[3]) {
  const entry = `
## vocab runtime verification F8 (${new Date().toISOString()})

- F8 sub-check 4 FAILED: 「未掌握」tab is GLOBAL, not doc-scoped.
  \`renderUnmastered()\` queries \`ProgressStore.wrongItems()\` (all docs) and never
  filters by \`STATE.activeDoc\`. Switching to a doc with no wrong attempts still
  shows the 3 wrong items from other docs. Task spec expected a doc-scoped empty
  state ("暂无未掌握词 ✓").
- Not fixed (verifier only). Decide: add an activeDoc filter to renderUnmastered,
  or accept the global list and update the spec.
`;
  fs.appendFileSync(ISSUES_FILE, entry);
}

const logHeader = `### ${new Date().toISOString()} ###`;
const logBody = [logHeader, ...lines, `RESULT: ${allPass ? 'ALL PASS' : 'FAILED'}`, ''].join('\n');
fs.appendFileSync(LOG_FILE, logBody);

console.log(lines.join('\n'));
if (errors.length) console.log('\n[jsdom errors captured (non-fatal unless a check failed)]\n' + errors.join('\n'));
if (warnings.length) console.log('\n[jsdom warnings captured]\n' + warnings.join('\n'));
console.log(`\nRESULT: ${allPass ? 'ALL PASS' : 'FAILED'} → log: ${LOG_FILE}`);

process.exit(allPass ? 0 : 1);