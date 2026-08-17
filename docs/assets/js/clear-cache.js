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
