---
name: gui-stylist
description: >-
  Handles all CanaHub GUI styling: SCSS, CSS custom properties, Angular component
  styles, responsive layout, typography, spacing, animations, and brand token
  application. Use when changing visual appearance, colors, fonts, spacing, layout,
  animations, dark mode, or any look-and-feel concern without touching business logic.
---

# GUI Stylist

## Before you touch any file

1. Read `docs/BRAND.md` — brand tokens are the source of truth.
2. Check `frontend/src/styles/_variables.scss` for existing CSS custom properties.
3. Read [brand-tokens.md](brand-tokens.md) for token catalogue and usage rules.
4. Read [component-patterns.md](component-patterns.md) for reusable patterns.

## Workflow

```
Task received
  ↓
Identify scope: global styles vs. single component vs. new component
  ↓
Check existing tokens (_variables.scss) — reuse before adding
  ↓
Apply changes (mobile-first, scoped, no hard-coded hex)
  ↓
Verify contrast (≥4.5:1 normal text, ≥3:1 large text)
  ↓
If new token added → update docs/BRAND.md too
```

## File Map

| What to change | Where |
|----------------|-------|
| Color/font/spacing tokens | `frontend/src/styles/_variables.scss` |
| Reusable mixins | `frontend/src/styles/_mixins.scss` |
| Global reset / base | `frontend/src/styles/styles.scss` |
| Component style | `frontend/src/app/**/<component>.component.scss` |
| Brand docs | `docs/BRAND.md` + `docs/brand-tokens.json` |

## SCSS Conventions

```scss
// ✅ Use tokens
color: var(--color-primary);

// ❌ Never hard-code
color: #1B4332;

// ✅ Mobile-first breakpoints
.card {
  padding: 1rem;

  @media (min-width: 768px) {
    padding: 2rem;
  }
}

// ✅ Scoped component host
:host {
  display: block;
}

// ✅ SCSS map for variants
$button-variants: (
  primary: var(--color-primary),
  accent:  var(--color-accent),
);

@each $name, $color in $button-variants {
  .btn--#{$name} { background: $color; }
}
```

## Animations

- Use `prefers-reduced-motion` guard for every animation.
- Prefer `opacity` + `transform` (GPU-composited) over `top`/`left`.

```scss
@keyframes fade-in {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}

.fade-in {
  animation: fade-in 0.3s ease-out both;

  @media (prefers-reduced-motion: reduce) {
    animation: none;
  }
}
```

## Accessibility Checklist

- [ ] Color contrast ≥ 4.5:1 (normal text) / ≥ 3:1 (large text / UI components)
- [ ] Focus rings visible (never `outline: none` without custom replacement)
- [ ] Interactive states: `:hover`, `:focus`, `:active`, `:disabled`
- [ ] No information conveyed by color alone

## Adding a New Token

1. Add to `_variables.scss`:
   ```scss
   --color-new-token: #XXXXXX;
   ```
2. Add to the table in `docs/BRAND.md` under "Color Palette".
3. Mirror in `docs/brand-tokens.json` if it exists.
4. Never introduce a new font family — use the three already defined.

## References

- [brand-tokens.md](brand-tokens.md) — full token catalogue
- [component-patterns.md](component-patterns.md) — card, button, badge, nav patterns
