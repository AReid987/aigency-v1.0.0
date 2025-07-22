---
type: Page
title: 'Story 4.2: Provide Input via HITL Channel'
description: null
icon: null
createdAt: '2025-07-11T10:18:01.777Z'
creationDate: 2025-07-11 05:18
modificationDate: 2025-07-11 05:18
tags: []
coverImage: null
---

# Story 4.2: Provide Input via HITL Channel

## Status: Draft

## Story

- As a FormWhisperer user

- I want to provide input to the AI agent via the HITL channel

- so that I can guide its responses and resolve ambiguities.

## Acceptance Criteria (ACs)

- The user can receive HITL requests from the agent on the configured channel.

- The user can send a response (e.g., text, selection) back to the agent.

- The agent receives and processes the human input.

- The agent resumes its task, incorporating the human input into its response.

- The system logs the human input and the agent's subsequent action.

- Local command-line test script can simulate human input and verify agent response.

## Tasks / Subtasks

- [ ] **Task 1: Implement Human Response Reception in HITL Orchestration Service (AC: 1, 2, 3)**

    - [ ] Subtask 1.1: Within the `hitl-service` (`src/services/hitl-service/`), set up a mechanism to receive user responses from the Telegram Bot API. This can be done via:

        - **Webhook:** Configure a public webhook endpoint that Telegram sends updates to.

        - **Polling:** Implement a polling mechanism to `getUpdates` from the Telegram API.

    - [ ] Subtask 1.2: Parse incoming messages to extract the human response and associate it with the correct `hitlRequestId`.

    - [ ] Subtask 1.3: Develop an internal API endpoint (e.g., `POST /api/v1/hitl/response`) for `hitl-service` to allow `automation-orchestrator` to query for a specific HITL response, or to push the response.

- [ ] **Task 2: Integrate Human Input into Automation Orchestrator (AC: 3, 4)**

    - [ ] Subtask 2.1: Update the `automation-orchestrator` service (`src/services/automation-orchestrator/`) to pause its execution loop (as initiated in Story 4.1) when an HITL request is sent.

    - [ ] Subtask 2.2: Implement logic for the orchestrator to await or fetch the human response from the `hitl-service` (via the internal API from Task 1.3).

    - [ ] Subtask 2.3: Once the human response is received, the orchestrator should resume the `browser-automator`'s task, providing the human input to the `response-generator` for re-evaluation (as per `docs/sequence-diagrams.md#human-in-the-loop-hitl-workflow`).

- [ ] **Task 3: Incorporate Human Input in Response Generation (AC: 4)**

    - [ ] Subtask 3.1: Enhance the `response-generator` agent (`src/agents/response-generator/`) to accept human input as an additional parameter when re-evaluating an answer.

    - [ ] Subtask 3.2: Modify the prompt engineering strategy to explicitly incorporate the human input, guiding the LLM to generate a final, confident answer based on this new information.

- [ ] **Task 4: Implement Robust Logging for HITL Responses (AC: 5)**

    - [ ] Subtask 4.1: Ensure `hitl-service`, `automation-orchestrator`, and `response-generator` log human responses received, how they were processed, and the agent's subsequent action, adhering to structured logging standards (`docs/operational-guidelines.md#logging`).

    - [ ] Subtask 4.2: Log that the browser automation task has been resumed.

- [ ] **Task 5: Develop Local Test Script for Full HITL Flow (AC: 6)**

    - [ ] Subtask 5.1: Create a Python CLI script (in `scripts/`) that simulates a full HITL cycle: triggering a request (from Story 4.1's test script), simulating a human response, and verifying that the `automation-orchestrator` receives and acts upon it (mocking Telegram API and LLM if necessary).

    - [ ] Subtask 5.2: The script should verify that the system logs accurately reflect the full HITL exchange.

## Dev Technical Guidance

This story completes the critical Human-in-the-Loop feedback loop, requiring seamless integration between services and robust handling of asynchronous communication.

- **Telegram Bot API Integration:** Decide between webhook or polling for receiving updates. Webhooks are generally preferred for real-time applications but require a publicly accessible endpoint. Refer to `docs/api-reference.md#telegram-bot-api` and ensure secure handling of the `TELEGRAM_BOT_TOKEN`.

- **Inter-Service Communication:** The `automation-orchestrator` and `hitl-service` will communicate to exchange HITL requests and responses. Use the internal API defined in `docs/api-reference.md#hitl-orchestration-service-api`.

- **Asynchronous Processing:** The `automation-orchestrator` will need to manage asynchronous waits for human input. Implement robust mechanisms to avoid deadlocks or timeouts while waiting for a response.

- **Prompt Engineering with Human Input:** The `response-generator` needs to effectively integrate human guidance into its LLM prompts. Experiment with how to best phrase the prompt to leverage this input for accurate and persona-consistent answers.

- **Project Structure:** All new code should adhere to the established monorepo structure. Updates to `hitl-service` (`src/services/hitl-service/`), `automation-orchestrator` (`src/services/automation-orchestrator/`), and `response-generator` (`src/agents/response-generator/`) are expected.

- **Logging & Security:** Implement structured JSON logging for all HITL-related actions and ensure no sensitive data is logged, adhering strictly to `docs/operational-guidelines.md#security-best-practices`.

- **Coding Standards & Testing:** Adhere to Node.js/TypeScript and Python coding standards, type safety, and unit test file organization as defined in `docs/operational-guidelines.md#coding-standards` and `docs/operational-guidelines.md#overall-testing-strategy`.

    - Unit tests for `hitl-service`: Verify it can parse incoming Telegram messages and correctly store/retrieve HITL responses (mocking Telegram API).

    - Integration tests: Verify the full HITL communication flow, from the agent requesting help to the human providing input and the agent resuming, mocking external APIs as needed.

## Story Progress Notes

### Agent Model Used: Benjamin "Beacon" Hayes (PO)

### Completion Notes List

### Change Log

