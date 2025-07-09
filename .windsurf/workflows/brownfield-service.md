---
name: "Brownfield Service/API Enhancement"
description: "Agent workflow for enhancing existing backend services and APIs with new features, modernization, or performance improvements. Handles existing system analysis and safe integration."
tags:
  - brownfield
  - service-modernization
  - api-enhancement
  - microservice-extraction
  - performance-optimization
  - integration-enhancement
  - brownfield-service
---

# Brownfield Service/API Enhancement

## Workflow Metadata

- **ID:** brownfield-service
- **Type:** brownfield
- **Project Types:** service-modernization, api-enhancement, microservice-extraction, performance-optimization, integration-enhancement

## Description

Agent workflow for enhancing existing backend services and APIs with new features, modernization, or performance improvements. Handles existing system analysis and safe integration.

## Workflow Steps

### service_analysis

- **Agent:** architect
- **Action:** analyze existing project and use task document-project
- **Notes:**
  Review existing service documentation, codebase, performance metrics, and identify integration dependencies.

### Unnamed Step

- **Agent:** pm
- **Action:** N/A
- **Notes:**
  Creates comprehensive PRD focused on service enhancement with existing system analysis. SAVE OUTPUT: Copy final prd.md to your project's docs/ folder.
- **Requires:** existing_service_analysis

### Unnamed Step

- **Agent:** architect
- **Action:** N/A
- **Notes:**
  Creates architecture with service integration strategy and API evolution planning. SAVE OUTPUT: Copy final architecture.md to your project's docs/ folder.
- **Requires:** prd.md

### Unnamed Step

- **Agent:** po
- **Action:** N/A
- **Notes:**
  Validates all documents for service integration safety and API compatibility. May require updates to any document.

### Unnamed Step

- **Agent:** various
- **Action:** N/A
- **Notes:**
  If PO finds issues, return to relevant agent to fix and re-export updated documents to docs/ folder.

### Unnamed Step

- **Agent:** po
- **Action:** shard_documents
- **Notes:**
  Shard documents for IDE development:
  - Option A: Use PO agent to shard: @po then ask to shard docs/prd.md
  - Option B: Manual: Drag shard-doc task + docs/prd.md into chat
  - Creates docs/prd/ and docs/architecture/ folders with sharded content
- **Requires:** all_artifacts_in_project

### Unnamed Step

- **Agent:** sm
- **Action:** create_story
- **Notes:**
  Story creation cycle:
  - SM Agent (New Chat): @sm → *create
  - Creates next story from sharded docs
  - Story starts in "Draft" status
- **Requires:** sharded_docs

### Unnamed Step

- **Agent:** analyst/pm
- **Action:** review_draft_story
- **Notes:**
  OPTIONAL: Review and approve draft story
  - NOTE: story-review task coming soon
  - Review story completeness and alignment
  - Update story status: Draft → Approved
- **Requires:** story.md

### Unnamed Step

- **Agent:** dev
- **Action:** implement_story
- **Notes:**
  Dev Agent (New Chat): @dev
  - Implements approved story
  - Updates File List with all changes
  - Marks story as "Review" when complete
- **Requires:** story.md

### Unnamed Step

- **Agent:** qa
- **Action:** review_implementation
- **Notes:**
  OPTIONAL: QA Agent (New Chat): @qa → review-story
  - Senior dev review with refactoring ability
  - Fixes small issues directly
  - Leaves checklist for remaining items
  - Updates story status (Review → Done or stays Review)
- **Requires:** implementation_files

### Unnamed Step

- **Agent:** dev
- **Action:** address_qa_feedback
- **Notes:**
  If QA left unchecked items:
  - Dev Agent (New Chat): Address remaining items
  - Return to QA for final approval

### Unnamed Step

- **Agent:** N/A
- **Action:** continue_for_all_stories
- **Notes:**
  Repeat story cycle (SM → Dev → QA) for all epic stories
  Continue until all stories in PRD are complete

### Unnamed Step

- **Agent:** po
- **Action:** epic_retrospective
- **Notes:**
  OPTIONAL: After epic completion
  - NOTE: epic-retrospective task coming soon
  - Validate epic was completed correctly
  - Document learnings and improvements

### Unnamed Step

- **Agent:** N/A
- **Action:** project_complete
- **Notes:**
  All stories implemented and reviewed!
  Project development phase complete.
  
  Reference: data#bmad-kb:IDE Development Workflow

## Flow Diagram

```mermaid
```mermaid
graph TD
    A[Start: Service Enhancement] --> B[analyst: analyze existing service]
    B --> C[pm: prd.md]
    C --> D[architect: architecture.md]
    D --> E[po: validate with po-master-checklist]
    E --> F{PO finds issues?}
    F -->|Yes| G[Return to relevant agent for fixes]
    F -->|No| H[po: shard documents]
    G --> E
    
    H --> I[sm: create story]
    I --> J{Review draft story?}
    J -->|Yes| K[analyst/pm: review & approve story]
    J -->|No| L[dev: implement story]
    K --> L
    L --> M{QA review?}
    M -->|Yes| N[qa: review implementation]
    M -->|No| O{More stories?}
    N --> P{QA found issues?}
    P -->|Yes| Q[dev: address QA feedback]
    P -->|No| O
    Q --> N
    O -->|Yes| I
    O -->|No| R{Epic retrospective?}
    R -->|Yes| S[po: epic retrospective]
    R -->|No| T[Project Complete]
    S --> T

    style T fill:#90EE90
    style H fill:#ADD8E6
    style I fill:#ADD8E6
    style L fill:#ADD8E6
    style C fill:#FFE4B5
    style D fill:#FFE4B5
    style K fill:#F0E68C
    style N fill:#F0E68C
    style S fill:#F0E68C
```

```
