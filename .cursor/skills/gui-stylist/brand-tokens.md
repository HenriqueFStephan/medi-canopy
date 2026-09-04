# Brand Tokens Reference

Source of truth: `docs/BRAND.md` · SCSS file: `frontend/src/styles/_variables.scss`

## Color Tokens

### Greens (primary palette)

| Token | Hex | Role |
|-------|-----|------|
| `--color-primary` | `#1B4332` | Deep forest green — headers, primary buttons, nav background |
| `--color-primary-mid` | `#2D6A4F` | Hover states, links, italic accents |
| `--color-primary-light` | `#52B788` | Lighter tint for tags, dividers, icons |
| `--color-secondary` | `#95D5B2` | Mint — badges, success indicators, highlights |

### Accent & Earth

| Token | Hex | Role |
|-------|-----|------|
| `--color-accent` | `#D4A574` | Warm hemp gold — CTAs, icon fills, pull quotes |
| `--color-earth` | `#5C4033` | Earth brown — consulting/services section, special callouts |

### Backgrounds & Surfaces

| Token | Hex | Role |
|-------|-----|------|
| `--color-bg` | `#F8FAF7` | Main page background |
| `--color-bg-dark` | `#0D1F17` | Footer, hero overlays, dark sections |
| `--color-surface` | `#FFFFFF` | Cards, modals, panels |

### Text & Borders

| Token | Hex | Role |
|-------|-----|------|
| `--color-text` | `#1A1A1A` | Primary body text |
| `--color-text-muted` | `#5A6B62` | Secondary / caption text |
| `--color-border` | `#E2E8E4` | Dividers, input borders |

## Contrast Matrix (on white surface)

| Token | Ratio | WCAG Level |
|-------|-------|------------|
| `--color-primary` on white | ~8.4:1 | AAA |
| `--color-text` on white | ~18.1:1 | AAA |
| `--color-text-muted` on white | ~5.1:1 | AA |
| `--color-accent` on white | ~2.8:1 | ❌ Use on dark only or for large text |
| `--color-accent` on `--color-bg-dark` | ~6.1:1 | AA large text |

## Typography Tokens

| Role | Font | CSS |
|------|------|-----|
| Headings | DM Serif Display | `font-family: 'DM Serif Display', Georgia, serif` |
| Body | Source Sans 3 | `font-family: 'Source Sans 3', system-ui, sans-serif` |
| Mono | JetBrains Mono | `font-family: 'JetBrains Mono', monospace` |

Loaded via Google Fonts in `frontend/src/index.html`. Do not add extra font families.

## Spacing Scale

Use a consistent spacing scale to avoid magic numbers:

| Variable | Value | Use |
|----------|-------|-----|
| `--space-xs` | `0.25rem` | Icon gaps, tight inline spacing |
| `--space-sm` | `0.5rem` | Compact padding |
| `--space-md` | `1rem` | Default padding/gap |
| `--space-lg` | `1.5rem` | Section inner padding |
| `--space-xl` | `2rem` | Section vertical rhythm |
| `--space-2xl` | `3rem` | Hero / section separators |

If these aren't yet in `_variables.scss`, add them before using.

## Breakpoints

| Name | Min-width | Target |
|------|-----------|--------|
| `sm` | 480px | Large phones |
| `md` | 768px | Tablets |
| `lg` | 1024px | Small desktops |
| `xl` | 1280px | Standard desktops |
| `2xl` | 1536px | Wide screens |

Always mobile-first (`min-width`).
