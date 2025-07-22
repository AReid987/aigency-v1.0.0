---
type: Page
title: HITL
description: null
icon: null
createdAt: '2025-07-11T08:52:22.700Z'
creationDate: 2025-07-11 03:52
modificationDate: 2025-07-11 03:52
tags: []
coverImage: null
---

```markdown
sequenceDiagram
    actor User
    participant AOS as Automation Orchestrator Service
    participant HS as HITL Service
    participant MP as Messaging Platform (e.g., Telegram)
    participant RG as Response Generator
    participant BA as Browser Automator
    BA->>AOS: Detected Ambiguity / Low Confidence (question, context)
    AOS->>RG: Request Answer (question, context, personaData)
    RG->>RG: Evaluate Confidence
    alt Low Confidence
        RG->>AOS: Signal HITL Required (question, context, options)
        AOS->>HS: Send HITL Request (userId, question, context, options)
        HS->>MP: Send Message to User
        MP-->>User: Notification
        User->>MP: Provide Response
        MP-->>HS: Forward User Response
        HS-->>AOS: Return User Response
        AOS->>RG: Retry Answer with Human Input (question, context, options, humanInput)
        RG->>LLM: Re-query with Human Input (optional)
        LLM-->>RG: Return Refined Answer
        RG-->>AOS: Return Confident Answer
    else High Confidence
        RG-->>AOS: Return Confident Answer
    end
    AOS->>BA: Fill Form Field (answer)
    BA->>ESP: Interact with Form
```

