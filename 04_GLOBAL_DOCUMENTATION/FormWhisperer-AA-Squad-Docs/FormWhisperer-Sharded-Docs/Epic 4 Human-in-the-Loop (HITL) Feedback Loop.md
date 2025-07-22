---
type: Page
title: 'Epic 4: Human-in-the-Loop (HITL) Feedback Loop'
description: null
icon: null
createdAt: '2025-07-11T08:34:28.837Z'
creationDate: 2025-07-11 03:34
modificationDate: 2025-07-11 03:34
tags: []
coverImage: null
---

# Epic 4: Human-in-the-Loop (HITL) Feedback Loop

- Goal: Establish a reliable mechanism for the AI to request and receive human assistance, enabling continuous learning and graceful handling of uncertainties.

- Story 4.1: As a FormWhisperer agent, I want to signal for human assistance when I encounter an ambiguous question or have low confidence in a response so that I can get accurate guidance.

    - Acceptance Criteria List:

        - The agent detects low confidence in an answer (threshold configurable).

        - The agent can detect when an unknown or ambiguous question type is presented.

        - The agent pauses its current task.

        - The agent sends a clear, concise request for human input to the configured HITL channel (e.g., Telegram message).

        - The request includes the question, its context (e.g., previous answers), and proposed options if any.

        - The system logs the HITL request and its reason.

        - Local command-line test script can simulate low confidence and verify HITL request generation.

- Story 4.2: As a FormWhisperer user, I want to provide input to the AI agent via the HITL channel so that I can guide its responses and resolve ambiguities.

    - Acceptance Criteria List:

        - The user can receive HITL requests from the agent on the configured channel.

        - The user can send a response (e.g., text, selection) back to the agent.

        - The agent receives and processes the human input.

        - The agent resumes its task, incorporating the human input into its response.

        - The system logs the human input and the agent's subsequent action.

        - Local command-line test script can simulate human input and verify agent response.

