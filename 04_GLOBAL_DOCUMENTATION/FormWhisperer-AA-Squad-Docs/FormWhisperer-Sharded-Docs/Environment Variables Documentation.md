---
type: Page
title: Environment Variables Documentation
description: null
icon: null
createdAt: '2025-07-11T08:39:29.132Z'
creationDate: 2025-07-11 03:39
modificationDate: 2025-07-11 03:39
tags: []
coverImage: null
---

# Environment Variables Documentation

### Infrastructure and Deployment Overview

- **Environment Configuration Management:** Environment variables (e.g., `process.env.NEXT_PUBLIC_API_URL`) will be managed using `.env` files for local development and build-time injection via CI variables for staging/production.

- **Secrets Management:** Environment variables (`.env`, AWS Secrets Manager) for all secrets (API keys, database credentials, bot tokens). Never hardcode secrets or commit them to source control. Access via a designated configuration module/service.

### Specific Variables (Examples/Guidelines)

- `NEXT_PUBLIC_API_URL`: Base URL for the frontend to communicate with the backend services.

- `LLM_API_PRODUCTION_URL`: Production URL for the Large Language Model API.

- `LLM_API_STAGING_URL`: Staging/Development URL for the Large Language Model API.

- `LLM_API_KEY`: API key for accessing the Large Language Model.

- `TELEGRAM_BOT_TOKEN`: Token for the Telegram Bot API.

- `MONGODB_URI`: Connection string for the MongoDB database.

- `BROWSER_AUTOMATION_HEADLESS`: Boolean (true/false) to run browser in headless mode.

- `TEST_SURVEY_LOGIN_USER`: Username for the dummy survey platform.

- `TEST_SURVEY_LOGIN_PASS`: Password for the dummy survey platform.

