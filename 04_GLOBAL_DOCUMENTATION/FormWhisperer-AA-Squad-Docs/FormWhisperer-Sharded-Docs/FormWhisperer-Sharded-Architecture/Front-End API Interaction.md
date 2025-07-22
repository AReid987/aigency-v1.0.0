---
type: Page
title: Front-End API Interaction
description: null
icon: null
createdAt: '2025-07-11T09:21:10.376Z'
creationDate: 2025-07-11 04:21
modificationDate: 2025-07-11 04:21
tags: []
coverImage: null
---

# Front-End API Interaction

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

