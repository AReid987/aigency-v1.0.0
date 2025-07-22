---
type: Page
title: Front-End Style Guide
description: null
icon: null
createdAt: '2025-07-11T09:09:35.643Z'
creationDate: 2025-07-11 04:09
modificationDate: 2025-07-11 04:10
tags: []
coverImage: null
---

#### `docs/front-end-style-guide.md`

# Front-End Style Guide

## Overall Frontend Philosophy & Patterns

- **Styling Approach:** Tailwind CSS. Configuration File(s): `tailwind.config.js`, `postcss.config.js`. Key conventions: A utility-first approach will be used for rapid styling. Custom components and any specific shared styles will be defined using Tailwind's `@apply` directives within dedicated CSS files (e.g., `src/styles/components.css`). Theme extensions will be configured in `tailwind.config.js` under `theme.extend`.

### Branding & Style Guide Basics (from UI/UX Specification)

- **Color Palette:** Neutral base (grays, whites) with a single accent color for primary actions.

- **Typography:** A clean, legible sans-serif font (e.g., Inter, Roboto, or system font stack).

- **Iconography:** Simple, clear icons (e.g., for alerts, confirmations).

- **Spacing & Grid:** Consistent use of a base unit (e.g., 8px) for margins, padding, and component spacing to ensure visual harmony.

