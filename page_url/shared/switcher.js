/**
 * CanaHub Palette & Variation Switcher
 * Reads ?palette=N&var=M from the URL, applies the right tokens,
 * and keeps the UI controls in sync.
 *
 * To link between variations:
 *   switchVariation(3)   → navigates to var3/index.html keeping current palette
 *   switchPalette(2)     → swaps palette colours in place (no page reload)
 */

const PALETTES = [
  {
    id: 1, name: "Forest Canopy", mood: "Earthy · Botanical",
    dots: ["#1b4332","#95d5b2","#d4a574","#f8faf7","#0d1f17"]
  },
  {
    id: 2, name: "Midnight Bloom", mood: "Premium · Bold",
    dots: ["#0d1b2a","#a8c8ff","#e8a87c","#f4f7fc","#060d18"]
  },
  {
    id: 3, name: "Golden Hour", mood: "Warm · Artisan",
    dots: ["#7c3d12","#fcd34d","#34d399","#fffbf5","#3c1a06"]
  },
  {
    id: 4, name: "Slate & Sage", mood: "Modern · Minimal",
    dots: ["#1e293b","#86efac","#f472b6","#f8fafc","#0f172a"]
  },
  {
    id: 5, name: "Terracotta Hemp", mood: "Craft · Organic",
    dots: ["#5c3d2e","#e8c9a0","#4a7c59","#fdf6ee","#2a1a12"]
  },
  {
    id: 6, name: "Emerald Leaf", mood: "Fresh · Vibrant",
    dots: ["#065f46","#6ee7b7","#fbbf24","#f0fdf4","#022c22"]
  },
  {
    id: 7, name: "Lavender Fields", mood: "Calm · Therapeutic",
    dots: ["#4c1d95","#c4b5fd","#14b8a6","#faf5ff","#2e1065"]
  },
  {
    id: 8, name: "Citrus Grove", mood: "Bright · Zesty",
    dots: ["#3f6212","#fde047","#f97316","#fefce8","#1a2e05"]
  }
];

const PALETTE_TOKENS = {
  1: {
    "--color-primary-dark":"#1b4332","--color-primary-mid":"#2d6a4f","--color-primary-light":"#52b788",
    "--color-secondary":"#95d5b2","--color-accent":"#d4a574","--color-bg":"#f8faf7",
    "--color-bg-dark":"#0d1f17","--color-surface":"#ffffff","--color-text":"#1a1a1a",
    "--color-text-muted":"#5a6b62","--color-border":"#e2e8e4"
  },
  2: {
    "--color-primary-dark":"#0d1b2a","--color-primary-mid":"#1b3a6b","--color-primary-light":"#3a7bd5",
    "--color-secondary":"#a8c8ff","--color-accent":"#e8a87c","--color-bg":"#f4f7fc",
    "--color-bg-dark":"#060d18","--color-surface":"#ffffff","--color-text":"#0d1b2a",
    "--color-text-muted":"#5a6880","--color-border":"#d8e3f0"
  },
  3: {
    "--color-primary-dark":"#7c3d12","--color-primary-mid":"#b45309","--color-primary-light":"#d97706",
    "--color-secondary":"#fcd34d","--color-accent":"#34d399","--color-bg":"#fffbf5",
    "--color-bg-dark":"#3c1a06","--color-surface":"#ffffff","--color-text":"#1c0f00",
    "--color-text-muted":"#78614a","--color-border":"#f0e0cc"
  },
  4: {
    "--color-primary-dark":"#1e293b","--color-primary-mid":"#334155","--color-primary-light":"#64748b",
    "--color-secondary":"#86efac","--color-accent":"#f472b6","--color-bg":"#f8fafc",
    "--color-bg-dark":"#0f172a","--color-surface":"#ffffff","--color-text":"#0f172a",
    "--color-text-muted":"#64748b","--color-border":"#e2e8f0"
  },
  5: {
    "--color-primary-dark":"#5c3d2e","--color-primary-mid":"#8b5e52","--color-primary-light":"#c4896f",
    "--color-secondary":"#e8c9a0","--color-accent":"#4a7c59","--color-bg":"#fdf6ee",
    "--color-bg-dark":"#2a1a12","--color-surface":"#fff9f2","--color-text":"#2a1a12",
    "--color-text-muted":"#8b7260","--color-border":"#eaddd0"
  },
  6: {
    "--color-primary-dark":"#065f46","--color-primary-mid":"#059669","--color-primary-light":"#34d399",
    "--color-secondary":"#6ee7b7","--color-accent":"#fbbf24","--color-bg":"#f0fdf4",
    "--color-bg-dark":"#022c22","--color-surface":"#ffffff","--color-text":"#052e16",
    "--color-text-muted":"#4b7a6a","--color-border":"#bbf7d0"
  },
  7: {
    "--color-primary-dark":"#4c1d95","--color-primary-mid":"#6d28d9","--color-primary-light":"#8b5cf6",
    "--color-secondary":"#c4b5fd","--color-accent":"#14b8a6","--color-bg":"#faf5ff",
    "--color-bg-dark":"#2e1065","--color-surface":"#ffffff","--color-text":"#1e1b4b",
    "--color-text-muted":"#6b6580","--color-border":"#e9d5ff"
  },
  8: {
    "--color-primary-dark":"#3f6212","--color-primary-mid":"#65a30d","--color-primary-light":"#a3e635",
    "--color-secondary":"#fde047","--color-accent":"#f97316","--color-bg":"#fefce8",
    "--color-bg-dark":"#1a2e05","--color-surface":"#ffffff","--color-text":"#1a2e05",
    "--color-text-muted":"#656d4a","--color-border":"#ecfccb"
  }
};

/** Apply a palette by id (1–8) to the :root element */
function applyPalette(id) {
  const tokens = PALETTE_TOKENS[id];
  if (!tokens) return;
  const root = document.documentElement;
  Object.entries(tokens).forEach(([k,v]) => root.style.setProperty(k, v));
  // keep URL in sync
  const url = new URL(location.href);
  url.searchParams.set('palette', id);
  history.replaceState({}, '', url.toString());
  syncSwitcherUI(id);
}

/** Navigate to a variation page, preserving current palette */
function switchVariation(varNum) {
  const url = new URL(location.href);
  const palette = url.searchParams.get('palette') || 1;
  const depth = url.pathname.split('/').filter(Boolean).length;
  // figure out relative path to page_url/varN/index.html
  const base = location.origin + location.pathname.split('/page_url')[0];
  location.href = `${base}/page_url/var${varNum}/index.html?palette=${palette}`;
}

/** Sync the floating switcher's select + dots to the active palette id */
function syncSwitcherUI(activeId) {
  document.querySelectorAll('.palette-dot').forEach(dot => {
    dot.classList.toggle('active', Number(dot.dataset.palette) === Number(activeId));
  });
  const sel = document.getElementById('palette-select');
  if (sel) sel.value = activeId;
  const nameEl = document.getElementById('palette-name');
  const moodEl = document.getElementById('palette-mood');
  const p = PALETTES.find(x => x.id === Number(activeId));
  if (p) {
    if (nameEl) nameEl.textContent = p.name;
    if (moodEl) moodEl.textContent = p.mood;
  }
}

/** Build the floating switcher HTML and inject it into the page */
function buildSwitcher(currentVar) {
  const el = document.createElement('div');
  el.className = 'palette-switcher';
  el.innerHTML = `
    <label>🎨 Palette</label>
    <div class="palette-dots">
      ${PALETTES.map(p => `<span
        class="palette-dot"
        data-palette="${p.id}"
        title="${p.name} — ${p.mood}"
        style="background:${p.dots[0]};box-shadow:inset 2px -2px 0 ${p.dots[1]}"
        onclick="applyPalette(${p.id})"
      ></span>`).join('')}
    </div>
    <select id="palette-select" onchange="applyPalette(Number(this.value))">
      ${PALETTES.map(p => `<option value="${p.id}">${p.id}. ${p.name}</option>`).join('')}
    </select>
    <div style="font-size:.75rem;color:var(--color-text-muted);line-height:1.3">
      <strong id="palette-name"></strong><br>
      <span id="palette-mood"></span>
    </div>
    <hr style="border:none;border-top:1px solid var(--color-border);margin:.25rem 0">
    <label>📐 Layout</label>
    <div style="display:flex;gap:.35rem;flex-wrap:wrap">
      ${[1,2,3,4,5].map(n => `<button
        onclick="switchVariation(${n})"
        style="
          flex:1;min-width:28px;padding:.3rem .4rem;font-size:.75rem;font-weight:700;
          border-radius:6px;border:1px solid var(--color-border);
          background:${n===currentVar?'var(--color-primary-dark)':'var(--color-bg)'};
          color:${n===currentVar?'#fff':'var(--color-text)'};cursor:pointer
        "
      >V${n}</button>`).join('')}
    </div>
  `;
  document.body.appendChild(el);
}

/** Init – runs on DOMContentLoaded */
document.addEventListener('DOMContentLoaded', () => {
  const url = new URL(location.href);
  const paletteId = Number(url.searchParams.get('palette')) || 1;

  // detect current variation from pathname (…/var3/index.html → 3)
  const varMatch = location.pathname.match(/var(\d)/);
  const currentVar = varMatch ? Number(varMatch[1]) : 1;

  applyPalette(paletteId);
  buildSwitcher(currentVar);

  // add variation badge
  const badge = document.createElement('div');
  badge.className = 'variation-badge';
  badge.textContent = `Layout V${currentVar}`;
  document.body.appendChild(badge);
});
