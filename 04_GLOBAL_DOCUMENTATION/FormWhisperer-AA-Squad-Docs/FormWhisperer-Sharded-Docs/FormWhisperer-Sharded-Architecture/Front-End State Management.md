---
type: Page
title: Front-End State Management
description: null
icon: null
createdAt: '2025-07-11T09:19:26.739Z'
creationDate: 2025-07-11 04:19
modificationDate: 2025-07-11 04:20
tags: []
coverImage: null
---

# Front-End State Management

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

        ```typescript
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

    - **Export:** All actions and selectors MUST be exported.}

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

