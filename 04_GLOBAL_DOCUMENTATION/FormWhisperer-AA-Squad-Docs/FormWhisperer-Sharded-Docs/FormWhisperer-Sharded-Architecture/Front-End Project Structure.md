---
type: Page
title: Front-End Project Structure
description: null
icon: null
createdAt: '2025-07-11T09:08:14.733Z'
creationDate: 2025-07-11 04:08
modificationDate: 2025-07-11 04:08
tags: []
coverImage: null
---

# Front-End Project Structure

## Detailed Frontend Directory Structure

The frontend application's folder structure is designed for modularity, alignment with Next.js conventions, and clear separation of concerns.

```text
src/
├── app/                        # Next.js App Router: Pages/Layouts/Routes. MUST contain route segments, layouts, and page components.
│   ├── (persona-setup)/        # Feature group for persona setup routes
│   │   ├── layout.tsx          # Layout specific to persona setup feature
│   │   └── page.tsx            # Entry page component for a persona setup
│   ├── (hitl)/                 # Feature group for HITL interface (if web-based)
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── api/                    # Next.js API Routes (if using Next.js backend for frontend features). MUST contain backend handlers for client-side calls.
│   ├── globals.css             # Global styles. MUST contain base styles, CSS variable definitions, Tailwind base/components/utilities.
│   └── layout.tsx              # Root layout for the entire application.
├── components/                 # Shared/Reusable UI Components.
│   ├── ui/                     # Base UI elements (Button, Input, Card). MUST contain only generic, reusable, presentational UI elements, often mapped from a design system. MUST NOT contain business logic.
│   │   ├── Button.tsx
│   │   └── Input.tsx
│   ├── layout/                 # Layout components (Header, Footer, Sidebar). MUST contain components structuring page layouts, not specific page content.
│   │   └── MainLayout.tsx
│   └── (feature-specific)/     # Components specific to a feature but potentially reusable within it (alternative to co-locating inside features/).
│       └── persona-form/
│           └── PersonaQuestionnaire.tsx
├── features/                   # Feature-specific logic, hooks, non-global state, services, and components solely used by that feature.
│   └── persona/
│       ├── components/         # Components used exclusively by the persona feature.
│       ├── hooks/              # Custom React Hooks specific to the 'persona' feature.
│       ├── services/           # Feature-specific API interactions for 'persona'.
│       └── store.ts            # Feature-specific state slice (Zustand store).
├── hooks/                      # Global/sharable custom React Hooks. MUST be generic and usable by multiple features/components.
│   └── useAuth.ts
├── lib/ / utils/               # Utility functions, helpers, constants. MUST contain pure functions and constants.
│   └── validators.ts
├── services/                   # Global API service clients or SDK configurations. MUST define base API client instances and core data fetching/mutation services.
│   └── apiClient.ts
├── store/                      # Global state management setup (Zustand store).
│   └── index.ts                # Main store configuration and export.
├── styles/                     # Global styles, theme configurations.
│   └── components.css          # Custom component styles using @apply
└── types/                      # Global TypeScript type definitions/interfaces. MUST contain types shared across multiple features/modules.
    └── index.ts
```

