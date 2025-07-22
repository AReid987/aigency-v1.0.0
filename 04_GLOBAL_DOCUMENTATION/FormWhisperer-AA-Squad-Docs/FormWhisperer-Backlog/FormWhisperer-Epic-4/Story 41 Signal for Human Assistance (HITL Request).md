---
type: Page
title: 'Story 4.1: Signal for Human Assistance (HITL Request)'
description: null
icon: null
createdAt: '2025-07-11T09:43:47.556Z'
creationDate: 2025-07-11 04:43
modificationDate: 2025-07-11 04:44
tags: []
coverImage: null
---

# Story 4.1: Signal for Human Assistance (HITL Request)

## Status: Draft

## Story

- As a FormWhisperer agent

- I want to signal for human assistance when I encounter an ambiguous question or have low confidence in a response

- so that I can get accurate guidance.

## Acceptance Criteria (ACs)

- The agent detects low confidence in an answer (threshold configurable).

- The agent can detect when an unknown or ambiguous question type is presented.

- The agent pauses its current task.

- The agent sends a clear, concise request for human input to the configured HITL channel (e.g., Telegram message).

- The request includes the question, its context (e.g., previous answers), and proposed options if any.

- The system logs the HITL request and its reason.

- Local command-line test script can simulate low confidence and verify HITL request generation.

## Tasks / Subtasks

- [ ] **Task 1: Implement Confidence Detection in Response Generator (AC: 1)**

    - [ ] Subtask 1.1: Within the `response-generator` agent (`src/agents/response-generator/`), integrate a mechanism to assess the confidence level of a generated answer. This could be based on LLM output scores, or rule-based (e.g., if LLM provides multiple conflicting answers).

    - [ ] Subtask 1.2: Define a configurable confidence threshold. If the generated answer falls below this threshold, signal low confidence.

- [ ] **Task 2: Implement Ambiguity/Unknown Type Detection in Form Parser (AC: 2)**

    - [ ] Subtask 2.1: Enhance the `form-parser` agent (`src/agents/form-parser/`) to identify question types or elements it has not been trained on, or that appear ambiguous (e.g., malformed HTML, unexpected UI widgets).

    - [ ] Subtask 2.2: When such an element is detected, the parser should flag it as "unknown" or "ambiguous" and provide relevant context (e.g., element type, surrounding text).

- [ ] **Task 3: Implement HITL Request Triggering in Automation Orchestrator (AC: 3, 4, 5)**

    - [ ] Subtask 3.1: Update the `automation-orchestrator` service (`src/services/automation-orchestrator/`) to handle triggers for HITL.

    - [ ] Subtask 3.2: When `response-generator` signals low confidence OR `form-parser` signals ambiguity, the orchestrator should pause the `browser-automator`'s current task.

    - [ ] Subtask 3.3: The orchestrator should then call the `HITL Orchestration Service`'s internal API (`docs/api-reference.md#hitl-orchestration-service-api`) to send an HITL request.

    - [ ] Subtask 3.4: The request payload should include `userId`, the `question`, its `context` (e.g., relevant HTML snippet or previous conversation turns), and any `proposed options` (if response generator had multiple low-confidence options).

- [ ] **Task 4: Develop HITL Orchestration Service (AC: 4)**

    - [ ] Subtask 4.1: Create a new Node.js/TypeScript service: `src/services/hitl-service/`.

    - [ ] Subtask 4.2: Implement the `POST /api/v1/hitl/request` endpoint as defined in `docs/api-reference.md#hitl-orchestration-service-api`.

    - [ ] Subtask 4.3: Integrate the service with the Telegram Bot API (`docs/api-reference.md#telegram-bot-api`) to send the HITL request message to the user.

    - [ ] Subtask 4.4: Ensure the Telegram message is clear, concise, and includes all necessary information for the user to respond effectively.

- [ ] **Task 5: Implement Logging for HITL Requests (AC: 6)**

    - [ ] Subtask 5.1: Ensure `response-generator`, `form-parser`, `automation-orchestrator`, and `hitl-service` all log HITL requests, their reasons (low confidence, ambiguity), and the full payload sent, adhering to structured logging standards (`docs/operational-guidelines.md#logging`).

    - [ ] Subtask 5.2: Log that the browser automation task has been paused.

- [ ] **Task 6: Develop Local Test Script for HITL Trigger (AC: 7)**

    - [ ] Subtask 6.1: Create a Python CLI script (in `scripts/`) that simulates an ambiguous question or forces a low-confidence scenario.

    - [ ] Subtask 6.2: The script should trigger the `automation-orchestrator` to initiate an HITL request, verifying that the request is correctly sent via the `hitl-service` (mocking Telegram API for testing).

    - [ ] Subtask 6.3: Verify that the system logs indicate the HITL trigger and task pause.

## Dev Technical Guidance

This story introduces the crucial Human-in-the-Loop mechanism, integrating multiple core services and leveraging external APIs.

- **Confidence Scoring:** The method for determining "low confidence" in `response-generator` should be well-defined. This might involve LLM output probabilities, specific keywords, or a separate classifier.

- **Ambiguity Detection:** `form-parser`'s ability to detect truly "unknown" or "ambiguous" elements is important. This may involve heuristics or a pre-defined list of supported element types.

- **Telegram Bot API:** Refer to `docs/api-reference.md#telegram-bot-api` for precise API calls to send messages. Ensure the `TELEGRAM_BOT_TOKEN` is securely managed via environment variables as per `docs/environment-vars.md`.

- **Internal API Call:** The `automation-orchestrator` will make an internal HTTP call to the `hitl-service`. Ensure proper error handling and retries for this internal call.

- **Pausing Automation:** The `browser-automator` needs a robust way to pause its execution when commanded by the `automation-orchestrator` and wait for a signal to resume. This may involve an event-driven mechanism or a polling loop.

- **Project Structure:** New `hitl-service` in `src/services/hitl-service/`. Updates to `response-generator`, `form-parser`, and `automation-orchestrator` should adhere to their existing directories.

- **Logging & Security:** Implement structured JSON logging (`Pino` for Node.js, `structlog` for Python) for all HITL-related actions. Adhere strictly to `docs/operational-guidelines.md#security-best-practices`, especially regarding not logging sensitive data from requests or responses.

- **Coding Standards & Testing:** Adhere to Node.js/TypeScript and Python coding standards, type safety, and unit test file organization.

    - Unit tests for `response-generator` and `form-parser`: Focus on their respective confidence/ambiguity detection logic.

    - Unit tests for `hitl-service`: Verify it correctly forms and attempts to send Telegram messages (mocking the Telegram API).

    - Integration tests: Verify the full flow from `response-generator` or `form-parser` triggering the `automation-orchestrator` to call the `hitl-service`, mocking the external Telegram API.

## Story Progress Notes

### Agent Model Used: Benjamin "Beacon" Hayes (PO)

### Completion Notes List

### Change Log

