---
type: Page
title: Front-End Routing Strategy
description: null
icon: null
createdAt: '2025-07-11T09:23:02.932Z'
creationDate: 2025-07-11 04:23
modificationDate: 2025-07-11 04:23
tags: []
coverImage: null
---

# Front-End Routing Strategy

## Routing Strategy

Next.js App Router will handle routing for the FormWhisperer web UI.

### Route Definitions

| Path Pattern      | Component/Page (`src/app/...`) | Protection                                     | Notes                                                 |
| :---------------- | :----------------------------- | :--------------------------------------------- | :---------------------------------------------------- |
| `/`               | `app/page.tsx`                 | `Public`                                       | Landing or default redirect.                          |
| `/persona-setup`  | `app/(persona-setup)/page.tsx` | `Public` (initial) / `Authenticated` (updates) | Initial persona questionnaire.                        |
| `/hitl-dashboard` | `app/(hitl)/page.tsx`          | `Authenticated`                                | Optional MVP page to view HITL status/history.        |
| `/login`          | `app/login/page.tsx`           | `Public`                                       | User login (if authentication is implemented for UI). |
| `{anotherRoute}`  | `{ComponentPath}`              | `{Public/Authenticated/Role:[ROLE_NAME]}`      | {Notes, parameter names and types}                    |

### Route Guards / Protection

- **Authentication Guard:** If user authentication is implemented for the web UI, routes will be protected using Next.js middleware (`middleware.ts`) or client-side checks in layouts. Logic MUST use authentication state from a global store (e.g., a simple `sessionStore` if separate from `personaStore`). Unauthenticated users attempting to access protected routes MUST be redirected to `/login`.

- **Authorization Guard (if applicable):** Role-based authorization will be implemented as needed, similar to authentication, to restrict access to certain UI sections based on user roles (e.g., only administrators can view certain dashboards).

