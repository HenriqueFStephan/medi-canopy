# Brand Identity — CanaHub

Inspired by professional cannabis consulting ([4trees](https://4treesbuilding.ca/projects), [PlantManager](https://plantmanager.com.br/)) and the author's voice on [@papiroebers](https://www.instagram.com/papiroebers).

## Name & Tagline

- **Product name:** CanaHub (working title — align with author before launch)
- **Tagline (PT):** *Informação confiável sobre cannabis — do campo à política.*
- **Tagline (EN):** *Trusted cannabis intelligence — from cultivation to policy.*

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--color-primary` | `#1B4332` | Deep forest green — headers, primary buttons |
| `--color-primary-light` | `#2D6A4F` | Hover states, accents |
| `--color-secondary` | `#95D5B2` | Highlights, badges, success |
| `--color-accent` | `#D4A574` | Warm hemp gold — CTAs, icons |
| `--color-earth` | `#5C4033` | Earth brown — consulting / services section |
| `--color-bg` | `#F8FAF7` | Page background |
| `--color-bg-dark` | `#0D1F17` | Footer, hero overlays |
| `--color-surface` | `#FFFFFF` | Cards, panels |
| `--color-text` | `#1A1A1A` | Body text |
| `--color-text-muted` | `#5A6B62` | Secondary text |
| `--color-border` | `#E2E8E4` | Dividers |

### Accessibility

- Primary on white: contrast ratio ≥ 7:1 (AAA for large text).
- Accent gold on dark bg only for large text or icons.

## Typography

| Role | Font | Fallback |
|------|------|----------|
| Headings | **DM Serif Display** | Georgia, serif |
| Body | **Source Sans 3** | system-ui, sans-serif |
| Mono (code/citations) | **JetBrains Mono** | monospace |

Loaded via Google Fonts in `index.html`.

## Visual Language

- **Photography:** Real cultivation, facilities, research — avoid stereotypical "leaf" clipart.
- **Layout:** Generous whitespace, card-based grids (reference: 4trees projects grid).
- **Icons:** Line icons, organic curves; cannabis leaf used sparingly in logo mark only.
- **Motion:** Subtle fade-in on scroll; no distracting animations.

## Logo Concept (placeholder)

Text mark: **Cana**Hub with "Cana" in primary green and "Hub" in accent gold. Optional minimal leaf silhouette integrated into the "a".

File: `frontend/src/assets/brand/logo.svg` (to be designed).

## Voice & Tone

- **Authoritative** but approachable — expert who has run full production cycles.
- **Brazil-first** — ANVISA, legislation, local market; international news contextualized.
- **Evidence-based** — cite sources; distinguish news vs. opinion vs. research.

## Social

- Instagram: [@papiroebers](https://www.instagram.com/papiroebers) — prominent in header footer and blog attribution.

## SCSS Variables

Implemented in `frontend/src/styles/_variables.scss` and mirrored in `docs/brand-tokens.json` for design tools.
