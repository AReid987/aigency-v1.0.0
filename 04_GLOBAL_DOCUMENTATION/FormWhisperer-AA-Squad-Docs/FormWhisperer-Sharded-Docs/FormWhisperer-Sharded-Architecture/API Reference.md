---
type: Page
title: API Reference
description: null
icon: null
createdAt: '2025-07-11T08:35:43.058Z'
creationDate: 2025-07-11 03:35
modificationDate: 2025-07-11 03:36
tags: []
coverImage: null
---

# API Reference

### External APIs Consumed

#### Large Language Model (LLM) API (e.g., Gemini, OpenAI GPT)

- **Purpose:** Core for natural language understanding and generation in `Response Generator`.

- **Base URL(s):**

    - Production: `{LLM_API_PRODUCTION_URL}`

    - Staging/Dev: `{LLM_API_STAGING_URL}`

- **Authentication:** API Key in Header (`Authorization: Bearer {API_KEY}`)

- **Key Endpoints Used:**

    - `POST /v1/chat/completions` (or similar for text generation)

        - Description: Generates text responses based on prompt and persona.

        - Request Body Schema: `{ "model": "...", "messages": [{ "role": "user", "content": "..." }], "temperature": 0.7 }` (example for OpenAI Chat Completions API)

        - Success Response Schema: `{ "choices": [{ "message": { "content": "..." } }] }`

- **Rate Limits:** To be observed per LLM provider's documentation.

- **Link to Official Docs:** `{URL_TO_LLM_PROVIDER_DOCS}`

#### Telegram Bot API (for HITL)

- **Purpose:** Sending HITL prompts to the user and receiving responses.

- **Base URL(s):** `https://api.telegram.org/bot{BOT_TOKEN}/`

- **Authentication:** Bot Token in URL.

- **Key Endpoints Used:**

    - `POST /sendMessage`

        - Description: Sends a text message to a user or chat.

        - Request Body Schema: `{ "chat_id": "...", "text": "...", "reply_markup": {...} }`

    - `POST /getUpdates`

        - Description: Receives incoming updates (messages from users).

- **Rate Limits:** Adhere to Telegram's limits (e.g., 30 messages/second per bot to the same chat).

- **Link to Official Docs:** `https://core.telegram.org/bots/api`

### Internal APIs Provided

#### Persona Service API

- **Purpose:** Provides API for managing user personas.

- **Base URL(s):** `/api/v1/personas`

- **Authentication/Authorization:** Internal service-to-service authentication (e.g., API key, JWT for internal calls).

- **Endpoints:**

    - `POST /`

        - Description: Creates a new persona.

        - Request Body Schema: `{"name": "string", "demographics": {}, "preferences": {}, "opinions": {}}`

        - Success Response Schema: `{"id": "string", "name": "string", ...}`

    - `GET /{id}`

        - Description: Retrieves a persona by ID.

        - Success Response Schema: `{"id": "string", "name": "string", ...}`

    - `PUT /{id}`

        - Description: Updates an existing persona.

        - Request Body Schema: `{"name": "string", "demographics": {}, ...}`

    - `GET /current` (if user-specific persona via UI)

        - Description: Retrieves the currently active user's persona.

#### HITL Orchestration Service API

- **Purpose:** Internal API for the Automation Orchestrator to request HITL.

- **Base URL(s):** `/api/v1/hitl`

- **Authentication/Authorization:** Internal service-to-service authentication.

- **Endpoints:**

    - `POST /request`

        - Description: Sends a human-in-the-loop request.

        - Request Body Schema: `{"userId": "string", "question": "string", "context": "string", "options": ["string"], "callbackUrl": "string"}`

        - Success Response Schema: `{"hitlRequestId": "string"}`

