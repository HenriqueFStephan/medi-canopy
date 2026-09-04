# Component Styling Patterns

Reusable SCSS patterns for CanaHub Angular components.

---

## Buttons

```scss
// Base
.btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-xs);
  padding: 0.625rem 1.25rem;
  border: none;
  border-radius: 6px;
  font-family: 'Source Sans 3', system-ui, sans-serif;
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.1s ease;

  &:active { transform: scale(0.98); }
  &:disabled { opacity: 0.5; cursor: not-allowed; }
  &:focus-visible { outline: 3px solid var(--color-secondary); outline-offset: 2px; }
}

// Variants
.btn--primary {
  background: var(--color-primary);
  color: #fff;
  &:hover { background: var(--color-primary-mid); }
}

.btn--accent {
  background: var(--color-accent);
  color: var(--color-bg-dark);
  &:hover { filter: brightness(0.92); }
}

.btn--ghost {
  background: transparent;
  color: var(--color-primary);
  border: 1.5px solid var(--color-primary);
  &:hover { background: color-mix(in srgb, var(--color-primary) 8%, transparent); }
}
```

---

## Cards

```scss
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 10px;
  padding: var(--space-lg);
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  transition: box-shadow 0.2s ease;

  &:hover { box-shadow: 0 4px 14px rgba(0,0,0,0.1); }

  &__header {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: 1.25rem;
    color: var(--color-primary);
    margin-bottom: var(--space-sm);
  }

  &__body {
    font-size: 0.9375rem;
    color: var(--color-text);
    line-height: 1.6;
  }

  &__footer {
    margin-top: var(--space-md);
    padding-top: var(--space-sm);
    border-top: 1px solid var(--color-border);
    font-size: 0.8125rem;
    color: var(--color-text-muted);
  }
}
```

---

## Badges

```scss
.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25em;
  padding: 0.2em 0.65em;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.02em;
  text-transform: uppercase;

  &--green  { background: var(--color-secondary); color: var(--color-primary); }
  &--gold   { background: var(--color-accent);    color: var(--color-bg-dark); }
  &--earth  { background: var(--color-earth);     color: #fff; }
  &--muted  { background: var(--color-border);    color: var(--color-text-muted); }
}
```

---

## Navigation

```scss
.nav {
  background: var(--color-primary);
  color: #fff;
  padding: 0 var(--space-lg);
  height: 60px;
  display: flex;
  align-items: center;
  gap: var(--space-xl);

  &__logo {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: 1.375rem;
    color: #fff;
    text-decoration: none;

    span { color: var(--color-accent); }
  }

  &__link {
    color: rgba(255,255,255,0.85);
    text-decoration: none;
    font-size: 0.9375rem;
    transition: color 0.15s;

    &:hover, &.active { color: var(--color-secondary); }
    &:focus-visible { outline: 2px solid var(--color-secondary); border-radius: 3px; }
  }
}
```

---

## Hero Section

```scss
.hero {
  background: var(--color-bg-dark);
  color: #fff;
  padding: var(--space-2xl) var(--space-lg);
  text-align: center;

  &__title {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: clamp(1.75rem, 5vw, 3.25rem);
    line-height: 1.15;
    margin-bottom: var(--space-md);
  }

  &__tagline {
    font-size: clamp(1rem, 2.5vw, 1.25rem);
    color: var(--color-secondary);
    max-width: 640px;
    margin: 0 auto var(--space-xl);
  }
}
```

---

## Dark Section (footer / callouts)

```scss
.section--dark {
  background: var(--color-bg-dark);
  color: #fff;

  a { color: var(--color-secondary); }
  p { color: rgba(255,255,255,0.8); }
  h2, h3 { font-family: 'DM Serif Display', Georgia, serif; }
}
```

---

## Utility Classes (global)

```scss
// Add to styles.scss
.text-primary  { color: var(--color-primary); }
.text-accent   { color: var(--color-accent); }
.text-muted    { color: var(--color-text-muted); }
.text-serif    { font-family: 'DM Serif Display', Georgia, serif; }

.surface       { background: var(--color-surface); }
.surface--dark { background: var(--color-bg-dark); color: #fff; }

.visually-hidden {
  position: absolute;
  width: 1px; height: 1px;
  padding: 0; margin: -1px;
  overflow: hidden;
  clip: rect(0,0,0,0);
  white-space: nowrap;
  border: 0;
}
```
