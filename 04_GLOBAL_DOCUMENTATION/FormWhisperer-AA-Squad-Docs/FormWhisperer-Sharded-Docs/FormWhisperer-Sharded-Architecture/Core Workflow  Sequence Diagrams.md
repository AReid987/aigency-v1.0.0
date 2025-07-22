---
type: Page
title: Core Workflow / Sequence Diagrams
description: null
icon: null
createdAt: '2025-07-11T08:51:02.210Z'
creationDate: 2025-07-11 03:51
modificationDate: 2025-07-11 03:51
tags: []
coverImage: null
---

# Core Workflow / Sequence Diagrams

### Survey Completion Workflow (Happy Path)

```text
sequenceDiagram
    actor User
    participant WebUI
    participant AOS as Automation Orchestrator Service
    participant PS as Persona Service
    participant BA as Browser Automator
    participant FP as Form Parser
    participant RG as Response Generator
    participant LLM as LLM API
    participant ESP as External Survey Platform
    User->>WebUI: Initiate Survey Completion (e.g., provide URL, select Persona)
    WebUI->>AOS: Request Start Survey (url, personaId)
    AOS->>PS: Get Persona Data (personaId)
    PS-->>AOS: Return Persona Data
    AOS->>BA: Launch Browser & Navigate (url)
    BA->>ESP: Load Survey Page
    ESP-->>BA: Rendered Survey Page
    loop For each form question
        BA->>FP: Get Current Page DOM
        FP-->>BA: Return Parsed Form Elements (question, type, options)
        BA->>AOS: Send Form Elements
        AOS->>RG: Request Answer (question, type, options, personaData)
        RG->>LLM: Query for Answer (question, personaData, context)
        LLM-->>RG: Return Raw Answer
        RG-->>AOS: Return Processed Answer
        AOS->>BA: Fill Form Field (answer)
        BA->>ESP: Interact with Form (type, click, select)
        ESP-->>BA: Next Question / Submit
    end
    BA->>AOS: Survey Completed
    AOS->>PS: Store SurveyCompletionRecord
    PS-->>AOS: Confirmation
    AOS->>WebUI: Notify Survey Complete
    WebUI->>User: Display Completion Status
```

