---
type: Page
title: FormWhisperer Frontend Architecture Document
description: null
icon: null
createdAt: '2025-07-11T08:21:40.770Z'
creationDate: 2025-07-11 03:21
modificationDate: 2025-07-11 03:22
tags: []
coverImage: null
---

# FormWhisperer Frontend Architecture Document

## Table of Contents

- [Introduction](https://www.google.com/search?q=%23introduction)

- [Overall Frontend Philosophy & Patterns](https://www.google.com/search?q=%23overall-frontend-philosophy--patterns)

- [Detailed Frontend Directory Structure](https://www.google.com/search?q=%23detailed-frontend-directory-structure)

- [Component Breakdown & Implementation Details](https://www.google.com/search?q=%23component-breakdown--implementation-details)

    - [Component Naming & Organization](https://www.google.com/search?q=%23component-naming--organization)

    - [Template for Component Specification](https://www.google.com/search?q=%23template-for-component-specification)

- [State Management In-Depth](https://www.google.com/search?q=%23state-management-in-depth)

    - [Store Structure / Slices](https://www.google.com/search?q=%23store-structure--slices)

    - [Key Selectors](https://www.google.com/search?q=%23key-selectors)

    - [Key Actions / Reducers / Thunks](https://www.google.com/search?q=%23key-actions--reducers--thunks)

- [API Interaction Layer](https://www.google.com/search?q=%23api-interaction-layer)

    - [Client/Service Structure](https://www.google.com/search?q=%23clientservice-structure)

    - [Error Handling & Retries (Frontend)](https://www.google.com/search?q=%23error-handling--retries-frontend)

- [Routing Strategy](https://www.google.com/search?q=%23routing-strategy)

    - [Route Definitions](https://www.google.com/search?q=%23route-definitions)

    - [Route Guards / Protection](https://www.google.com/search?q=%23route-guards--protection)

- [Build, Bundling, and Deployment](https://www.google.com/search?q=%23build-bundling-and-deployment)

    - [Build Process & Scripts](https://www.google.com/search?q=%23build-process--scripts)

    - [Key Bundling Optimizations](https://www.google.com/search?q=%23key-bundling-optimizations)

    - [Deployment to CDN/Hosting](https://www.google.com/search?q=%23deployment-to-cdnhosting)

- [Frontend Testing Strategy](https://www.google.com/search?q=%23frontend-testing-strategy)

    - [Component Testing](https://www.google.com/search?q=%23component-testing)

    - [UI Integration/Flow Testing](https://www.google.com/search?q=%23ui-integrationflow-testing)

    - [End-to-End UI Testing Tools & Scope](https://www.google.com/search?q=%23end-to-end-ui-testing-tools--scope)

- [Accessibility (AX) Implementation Details](https://www.google.com/search?q=%23accessibility-ax-implementation-details)

- [Performance Considerations](https://www.google.com/search?q=%23performance-considerations)

- [Internationalization (i18n) and Localization (l10n) Strategy](https://www.google.com/search?q=%23internationalization-i18n-and-localization-l10n-strategy)

- [Feature Flag Management](https://www.google.com/search?q=%23feature-flag-management)

- [Frontend Security Considerations](https://www.google.com/search?q=%23frontend-security-considerations)

- [Browser Support and Progressive Enhancement](https://www.google.com/search?q=%23browser-support-and-progressive-enhancement)

- [Change Log](https://www.google.com/search?q=%23change-log)

## Introduction

This document details the technical architecture specifically for the frontend of FormWhisperer. It complements the main [FormWhisperer Architecture Document](https://www.google.com/search?q=docs/architecture.md) and the [FormWhisperer UI/UX Specification](https://www.google.com/search?q=docs/front-end-spec.md). This document details the frontend architecture and **builds upon the foundational decisions** (e.g., overall tech stack, CI/CD, primary testing tools) defined in the main FormWhisperer Architecture Document. **Frontend-specific elaborations or deviations from general patterns must be explicitly noted here.** The goal is to provide a clear blueprint for frontend development, ensuring consistency, maintainability, and alignment with the overall system design and user experience goals.

- **Link to Main Architecture Document (REQUIRED):** `docs/architecture.md`

- **Link to UI/UX Specification (REQUIRED if exists):** `docs/front-end-spec.md`

- **Link to Primary Design Files (Figma, Sketch, etc.) (REQUIRED if exists):** (To be added: Figma, Sketch, Adobe XD URL)

- **Link to Deployed Storybook / Component Showcase (if applicable):** (To be established during development)

## Overall Frontend Philosophy & Patterns

The frontend of FormWhisperer will adhere to a modern, component-driven architecture, focusing on reusability, maintainability, and optimal user experience for persona setup and HITL interactions.

- **Framework & Core Libraries:** React 18.x with Next.js 14.x. These are derived from the 'Definitive Tech Stack Selections' in the main Architecture Document. We will leverage Next.js's features for routing, server-side rendering (if applicable to specific pages), and API routes for a lightweight backend for frontend (BFF) layer if needed.

- **Component Architecture:** Atomic Design principles will be applied, distinguishing between Atoms (basic HTML elements/Tailwind utilities), Molecules (combinations of atoms, e.g., a form input with label), Organisms (complex UI sections), Templates (page-level layouts), and Pages (instances of templates with real content). Components will primarily be Presentational (focused on UI) with Container components handling data fetching and logic.

- **State Management Strategy:** Zustand will be used for global state management. This solution is chosen for its simplicity, speed, and scalability for React applications. This will be detailed further in the "State Management In-Depth" section.

- **Data Flow:** Unidirectional data flow will be enforced, primarily using React's props for passing data down the component tree and callbacks for passing events up. Server state will be managed via dedicated API interaction patterns.

- **Styling Approach:** Tailwind CSS. Configuration File(s): `tailwind.config.js`, `postcss.config.js`. Key conventions: A utility-first approach will be used for rapid styling. Custom components and any specific shared styles will be defined using Tailwind's `@apply` directives within dedicated CSS files (e.g., `src/styles/components.css`). Theme extensions will be configured in `tailwind.config.js` under `theme.extend`.

- **Key Design Patterns Used:** Provider pattern (for Context API if used for localized state), Hooks (for reusable logic), and Service patterns for API calls. These patterns will be consistently applied throughout the codebase.

## Detailed Frontend Directory Structure

The frontend application's folder structure is designed for modularity, alignment with Next.js conventions, and clear separation of concerns.

Plaintext

```markdown
src/
├── app/                        # Next.js App Router: Pages/Layouts/Routes. MUST contain route segments, layouts, and page components.
│   ├── (persona-setup)/        # Feature group for persona setup routes
│   │   ├── layout.tsx          # Layout specific to persona setup feature
│   │   └── page.tsx            # Entry page component for persona setup
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

### Notes on Frontend Structure:

Components are primarily co-located with their feature in `src/features/` if not globally reusable to improve modularity and cohesion. Globally reusable UI elements are located in `src/components/ui/`. The AI Agent MUST adhere to this defined structure strictly. New files MUST be placed in the appropriate directory based on these descriptions.

## Component Breakdown & Implementation Details

This section outlines the conventions and templates for defining UI components. The AI agent MUST follow the "Template for Component Specification" below whenever a new component is identified for development.

### Component Naming & Organization

- **Component Naming Convention:** PascalCase for files and component names (e.g., `UserProfileCard.tsx`). All component files MUST follow this convention.

- **Organization:** Globally reusable components in `src/components/ui/` or `src/components/layout/`. Feature-specific components co-located within their feature directory, e.g., `src/features/feature-name/components/`.

### Template for Component Specification

For each significant UI component identified from the UI/UX Specification and design files (Figma), the following details MUST be provided. The level of detail MUST be sufficient for an AI agent or developer to implement it with minimal ambiguity.

#### Component: `{ComponentName}` (e.g., `PersonaInputForm`, `HitlPromptDisplay`)

- **Purpose:** {Briefly describe what this component does and its role in the UI. MUST be clear and concise.}

- **Source File(s):** {e.g., `src/features/persona/components/PersonaInputForm.tsx`. MUST be the exact path.}

- **Visual Reference:** {Link to specific Figma frame/component, or Storybook page. REQUIRED.}

- **Props (Properties):** | Prop Name | Type | Required? | Default Value | Description | | :-------------- | :---------------------------------------- | :-------- | :------------ | :--------------------------------------------------------------------------------------------------------- | | `data` | `{ any specific interface for data }` | Yes | N/A | Data object required for component display or function. | | `onSave` | `(data: T) => void` | No | N/A | Callback function triggered on save action. | | `{anotherProp}` | `{Specific primitive, imported type, or inline interface/type definition}` | {Yes/No} | {If any} | {MUST clearly state the prop's purpose and any constraints, e.g., 'Must be a positive integer.'} |

- **Internal State (if any):** | State Variable | Type | Initial Value | Description | | :-------------- | :-------- | :------------ | :----------------------------------------------------------------------------- | | `formValues` | `{ form data interface }` | `{ initial data from props }` | Manages the current state of form inputs. | | `{anotherState}` | `{type}` | `{value}` | {Description of state variable and its purpose.} |

- **Key UI Elements / Structure:** { Provide a pseudo-HTML or JSX-like structure representing the component's DOM. Include key conditional rendering logic if applicable. **This structure dictates the primary output for the AI agent.** }

    HTML

    ```text
    <form>
      <label for="name">Name:</label>
      <input id="name" type="text" value="{formValues.name}" />
      <button type="submit">Save</button>
    </form>
    ```

- **Events Handled / Emitted:**

    - **Handles:** {e.g., `onChange` for input fields, `onSubmit` for forms, `onClick` for buttons.}

    - **Emits:** {If the component emits custom events/callbacks not covered by props, describe them with their exact signature. e.g., `onFormChange: (payload: { field: string; value: any }) => void`}

- **Actions Triggered (Side Effects):**

    - **State Management:** {e.g., "Updates local `formValues` state on input change." OR "Dispatches `personaSlice.actions.updatePersonaField(payload)` to global state." Action payload MUST match the defined action creator.}

    - **API Calls:** {Specify which service/function from the "API Interaction Layer" is called. e.g., "Calls `personaService.savePersona(formData)` from `src/services/personaService.ts` on form submit. Success response updates global persona state. Error response dispatches `uiSlice.actions.showErrorToast({ message: 'Failed to save persona' })`."}

- **Styling Notes:**

    - {MUST reference specific Design System component names (e.g., "Uses `<Button variant='primary'>` from UI library") OR specify Tailwind CSS classes / CSS module class names to be applied (e.g., "Container uses `p-4 bg-white rounded-lg shadow-md`. Title uses `text-xl font-semibold`.") OR specify SCSS custom component classes to be applied (e.g., "Container uses `@apply p-4 bg-white rounded-lg shadow-md`. Title uses `@apply text-xl font-semibold`."). Any dynamic styling logic based on props or state MUST be described. If Tailwind CSS is used, list primary utility classes or `@apply` directives for custom component classes. AI Agent should prioritize direct utility class usage for simple cases and propose reusable component classes/React components for complex styling patterns.}

- **Accessibility Notes:**

    - {MUST list specific ARIA attributes and their values (e.g., `aria-label="User profile card"`, `role="article"`), required keyboard navigation behavior (e.g., "Tab navigates through form fields in logical order. Inputs are focusable and editable."), and any focus management requirements (e.g., "On error, focus shifts to the first invalid field.").}

## State Management In-Depth

Zustand is the chosen state management solution for the FormWhisperer frontend. It provides a simple, hooks-based approach for managing global state.

- **Chosen Solution:** Zustand.

- **Decision Guide for State Location:**

    - **Global State (Zustand):** Data shared across many unrelated components (e.g., `persona` data, `HITL` notification status). MUST be used for session data, user preferences, and application-wide notifications.

    - **React Context API:** State primarily passed down a specific component subtree (e.g., a form context for nested inputs). MUST be used for localized state not suitable for prop drilling but not needed globally.

    - **Local Component State (**`useState`**,** `useReducer`**):** UI-specific state, not needed outside the component or its direct children (e.g., form input values before submission, dropdown open/close status). MUST be the default choice unless criteria for Context or Global State are met.

### Store Structure / Slices

Global state will be organized into feature-based "slices" within the Zustand store, located in `src/features/[featureName]/store.ts` or `src/store/slices/`.

- **Core Slice Example:** `personaStore.ts` **(in** `src/features/persona/store.ts`**):**

    - **Purpose:** Manages the active user's persona data and related status.

    - **State Shape (Interface/Type):**

        TypeScript

        ```text
        import { Persona } from '@/shared/types'; // Assuming shared types are imported
        interface PersonaState {
          currentPersona: Persona | null;
          isLoading: boolean;
          error: string | null;
        }
        ```

    - **Key Actions (within** `create` **function):** `setPersona(persona: Persona)`, `clearPersona()`, `setLoading(status: boolean)`, `setError(message: string)`.

    - **Async Actions:** `fetchPersonaById(id: string)`, `savePersona(persona: Partial<Persona>)`.

- **Feature Slice Template:** `{featureName}Store.ts` **(in** `src/features/{featureName}/store.ts`**):**

    - **Purpose:** To be filled out when a new feature requires its own state slice.

    - **State Shape (Interface/Type):** {To be defined by the feature.}

    - **Key Actions:** {To be defined by the feature.}

    - **Async Actions:** {To be defined by the feature.}

    - **Export:** All actions and selectors MUST be exported.

### Key Selectors

Selectors will be simple functions that retrieve data from the Zustand store. For derived state or combining multiple store pieces, memoization with libraries like `reselect` should be considered if performance bottlenecks emerge, but Zustand's simplicity often avoids this need initially.

- `usePersonaStore.use.currentPersona` (from `personaStore`): Returns the `currentPersona` object.

- `usePersonaStore.use.isLoading` (from `personaStore`): Returns the `isLoading` boolean.

### Key Actions / Reducers / Thunks

Actions in Zustand are simply functions that modify the store's state. Asynchronous operations are handled directly within these actions.

- **Core Action/Thunk Example:** `savePersona(personaData: Partial<Persona>)` **(in** `personaStore.ts`**):**

    - **Purpose:** Handles saving persona data to the backend API.

    - **Parameters:** `personaData: Partial<Persona>`

    - **Flow:**

        1. Sets `isLoading` to `true`.

        2. Calls `personaService.updatePersona(personaData)` (from `src/services/personaService.ts`).

        3. On success: Calls `setPersona(updatedPersona)`, sets `isLoading` to `false`, clears `error`.

        4. On error: Sets `error` with error message, sets `isLoading` to `false`.

## API Interaction Layer

The frontend will communicate with the backend APIs (primarily the Persona Service and potentially the HITL Orchestration Service's internal API) using a dedicated API client.

### Client/Service Structure

- **HTTP Client Setup:** Axios instance in `src/services/apiClient.ts`. MUST include: Base URL (from environment variable `NEXT_PUBLIC_API_URL`), default headers (e.g., `Content-Type: 'application/json'`), and interceptors for automatic auth token injection (if user authentication is implemented in the UI) and standardized error handling.

- **Service Definitions (Example):**

    - `personaService.ts` **(in** `src/services/personaService.ts`**):**

        - **Purpose:** Handles all API interactions related to user personas.

        - **Functions:** Each service function MUST have explicit parameter types, a return type (e.g., `Promise<Persona>`), JSDoc/TSDoc explaining purpose, params, return value, and any specific error handling. It MUST call the configured HTTP client (`apiClient`) with correct endpoint, method, and payload.

            - `getPersona(id: string): Promise<Persona>`

            - `savePersona(data: Partial<Persona>): Promise<Persona>`

### Error Handling & Retries (Frontend)

- **Global Error Handling:** API errors caught globally via Axios response interceptor in `apiClient.ts`. They will trigger a global notification (e.g., a toast message) or update a global error state.

- **Specific Error Handling:** Components MAY handle specific API errors locally for more contextual feedback (e.g., displaying an inline message on a form field). This MUST be documented in the component's specification if it deviates from global handling.

- **Retry Logic:** Client-side retry logic (e.g., using `axios-retry` with `apiClient`) will be implemented for idempotent requests (GET, PUT) in cases of network errors or specific 5xx server errors, with a maximum of 3 retries and exponential backoff.

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

Export to Sheets

### Route Guards / Protection

- **Authentication Guard:** If user authentication is implemented for the web UI, routes will be protected using Next.js middleware (`middleware.ts`) or client-side checks in layouts. Logic MUST use authentication state from a global store (e.g., a simple `sessionStore` if separate from `personaStore`). Unauthenticated users attempting to access protected routes MUST be redirected to `/login`.

- **Authorization Guard (if applicable):** Role-based authorization will be implemented as needed, similar to authentication, to restrict access to certain UI sections based on user roles (e.g., only administrators can view certain dashboards).

## Build, Bundling, and Deployment

Frontend build and deployment will integrate with the monorepo's CI/CD pipeline.

### Build Process & Scripts

- **Key Build Scripts (from** `package.json`**):** `"build": "next build"`, `"dev": "next dev"`, `"start": "next start"`.

- **Environment Configuration Management:** Environment variables (e.g., `process.env.NEXT_PUBLIC_API_URL`) will be managed using `.env` files for local development and build-time injection via CI variables for staging/production. AI Agent MUST NOT generate code that hardcodes environment-specific values.

### Key Bundling Optimizations

- **Code Splitting:** Next.js handles route-based code splitting automatically. Dynamic imports (`React.lazy(() => import('./MyComponent'))`) MUST be used for component-level code splitting for non-critical large components.

- **Tree Shaking:** Ensured by modern build tools (Webpack, used by Next.js) when using ES Modules.

- **Lazy Loading (Components, Images, etc.):** Components using `React.lazy` with `Suspense`. Images will use `next/image` component for automatic lazy loading and optimization.

- **Minification & Compression:** Handled by Next.js build tools (e.g., Terser). Gzip/Brotli compression will be handled by the hosting platform/CDN.

### Deployment to CDN/Hosting

- **Target Platform:** AWS S3/CloudFront (static site hosting) or Vercel (for Next.js deployments).

- **Deployment Trigger:** Git push to `main` branch via GitHub Actions, integrated with the monorepo's CI/CD pipeline.

- **Asset Caching Strategy:** Immutable assets (JS/CSS bundles with content hashes) will have `Cache-Control: public, max-age=31536000, immutable`. HTML files will have `Cache-Control: no-cache` to ensure fresh entry points. Configured via CDN rules or Next.js headers.

## Frontend Testing Strategy

This section elaborates on the "Testing Strategy" from the main architecture document, focusing on frontend-specific aspects.

- **Link to Main Overall Testing Strategy:** `docs/architecture.md#overall-testing-strategy`

### Component Testing

- **Scope:** Testing individual UI components in isolation (e.g., PersonaInputForm, HitlPromptDisplay).

- **Tools:** React Testing Library with Jest.

- **Focus:** Rendering with various props, user interactions (clicks, input changes), event emission, basic internal state changes. Snapshot testing will be used sparingly.

- **Location:** `*.test.tsx` or `*.spec.tsx` co-located alongside components, or in a `__tests__` subdirectory.

### Feature/Flow Testing (UI Integration)

- **Scope:** Testing how multiple components interact to fulfill a small user flow or feature within a page (e.g., persona setup form submission).

- **Tools:** React Testing Library with Jest.

- **Focus:** Data flow between components, conditional rendering based on interactions, integration with mocked services/state.

### End-to-End UI Testing Tools & Scope

- **Tools:** Playwright.

- **Scope (Frontend Focus):**

    - User completing the Persona Setup Questionnaire successfully.

    - Verification of HITL prompt display and user response submission (if web-based HITL is implemented).

    - Key UI interactions within any management dashboard (if implemented).

- **Test Data Management for UI:** API mocking layer (e.g., MSW) or backend seeding scripts will provide consistent test data.

## Accessibility (AX) Implementation Details

Based on the AX requirements in the UI/UX Specification, these details define how they will be technically implemented.

- **Semantic HTML:** AI Agent MUST prioritize semantic elements (e.g., `<form>`, `<button>`, `<label>`, `<input>`) over generic `<div>`/`<span>` with ARIA roles where a native element with the correct semantics exists.

- **ARIA Implementation:** For custom elements, ARIA attributes (e.g., `aria-label`, `aria-describedby`, `role`) will be used to convey semantic meaning and state where native HTML is insufficient. Refer to ARIA Authoring Practices Guide (APG).

- **Keyboard Navigation:** All interactive elements (form fields, buttons) must be keyboard navigable and operable (Tab, Shift+Tab, Enter, Space). Focus order MUST be logical.

- **Focus Management:** In dynamic content scenarios (e.g., loading spinners, success messages), focus will be managed to direct screen reader users to relevant updates.

- **Testing Tools for AX:** Axe DevTools browser extension, Lighthouse accessibility audit. Automated Axe scans (`jest-axe` for component tests, Playwright Axe integration for E2E tests) will be integrated into the CI pipeline and fail the build on new violations of WCAG AA.

## Performance Considerations

Frontend-specific performance optimization strategies will be employed to ensure a fast and responsive user experience.

- **Image Optimization:** `next/image` component for automatic optimization (formats, responsive images, lazy loading). SVGs for icons.

- **Code Splitting & Lazy Loading:** Next.js handles route-based code splitting. Dynamic imports (`import()`) for component-level lazy loading.

- **Minimizing Re-renders:** `React.memo` for components that render frequently with same props. Zustand selectors inherently optimize re-renders.

- **Debouncing/Throttling:** Use utilities for event handlers like input fields that trigger frequent updates.

- **Client-Side Caching Strategies:** Leveraging HTTP caching headers for static assets as defined in Deployment section.

## Internationalization (i18n) and Localization (l10n) Strategy

Internationalization is not a primary requirement for FormWhisperer at this time, as the initial target user is singular. However, the architecture will be designed to allow for future integration of an i18n library (e.g., `react-i18next`) and translation files, without requiring major refactoring.

## Feature Flag Management

Feature flags are not a primary architectural concern for FormWhisperer's MVP, given the single-user focus. If A/B testing or gradual rollouts become necessary in future phases, a lightweight solution using environment variables or a configuration service will be integrated.

## Frontend Security Considerations

Mandatory frontend-specific security practices will complement the main Architecture Document.

- **Cross-Site Scripting (XSS) Prevention:** React's JSX auto-escaping will be relied upon. `v-html` or direct DOM manipulation will be avoided.

- **Secure Token Storage & Handling:** If the UI implements user authentication, tokens (e.g., JWTs) will be stored in-memory via state management (Zustand) and cleared on tab close. `HttpOnly` cookies will be used if the backend sets them and frontend doesn't need to read. `localStorage` is **STRONGLY DISCOURAGED** for token storage.

- **Third-Party Script Security:** All third-party scripts must be vetted and loaded asynchronously (`async/defer`).

- **Client-Side Data Validation:** For UX improvement only. All critical data validation MUST occur server-side as defined in the main Architecture Document.

- **API Key Exposure:** API keys for client-side services (if any) MUST be restricted (e.g., HTTP referrer, IP address) via the service provider's console. Sensitive keys require a backend proxy.

- **Secure Communication (HTTPS):** All communication with backend APIs MUST use HTTPS.

- **Dependency Vulnerabilities:** `npm audit` (or equivalent) will run in CI. High/critical vulnerabilities MUST be addressed.

## Browser Support and Progressive Enhancement

- **Target Browsers:** Latest 2 stable versions of Chrome, Firefox, Safari, Edge. Internet Explorer is NOT supported.

- **Polyfill Strategy:** `core-js@3` imported at application entry point, configured via Babel `preset-env` with target browser list.

- **JavaScript Requirement & Progressive Enhancement:** Core application functionality REQUIRES JavaScript enabled. The application will not aim for full functionality without JavaScript.

- **CSS Compatibility & Fallbacks:** Autoprefixer (via PostCSS) will be used. CSS features not supported by >90% of target browsers will require graceful degradation or `@supports` queries.

## Change Log

| Change        | Date       | Version | Description                                                    | Author              |
| :------------ | :--------- | :------ | :------------------------------------------------------------- | :------------------ |
| Initial Draft | 2025-07-11 | 1.0     | Comprehensive Frontend Architecture Document for FormWhisperer | Phoenix "Prism" Kim |

Export to Sheets

