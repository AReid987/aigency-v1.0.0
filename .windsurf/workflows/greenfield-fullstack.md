---
name: "Greenfield Full-Stack Application Development"
description: "Agent workflow for building full-stack applications from concept to development. Supports both comprehensive planning for complex projects and rapid prototyping for simple ones."
tags:
  - greenfield
  - web-app
  - saas
  - enterprise-app
  - prototype
  - mvp
  - greenfield-fullstack
---

# Greenfield Full-Stack Application Development

## Workflow Metadata

- **ID:** greenfield-fullstack
- **Type:** greenfield
- **Project Types:** web-app, saas, enterprise-app, prototype, mvp

## Description

Agent workflow for building full-stack applications from concept to development. Supports both comprehensive planning for complex projects and rapid prototyping for simple ones.

## Workflow Steps

### Unnamed Step

- **Agent:** analyst
- **Action:** N/A
- **Notes:**
  Can do brainstorming first, then optional deep research before creating project brief. SAVE OUTPUT: Copy final project-brief.md to your project's docs/ folder.

### Unnamed Step

- **Agent:** pm
- **Action:** N/A
- **Notes:**
  Creates PRD from project brief using prd-tmpl. SAVE OUTPUT: Copy final prd.md to your project's docs/ folder.
- **Requires:** project-brief.md

### Unnamed Step

- **Agent:** ux-expert
- **Action:** N/A
- **Notes:**
  Creates UI/UX specification using front-end-spec-tmpl. SAVE OUTPUT: Copy final front-end-spec.md to your project's docs/ folder.
- **Requires:** prd.md

### Unnamed Step

- **Agent:** ux-expert
- **Action:** N/A
- **Notes:**
  OPTIONAL BUT RECOMMENDED: Generate AI UI prompt for tools like v0, Lovable, etc. Use the generate-ai-frontend-prompt task. User can then generate UI in external tool and download project structure.
- **Requires:** front-end-spec.md

### Unnamed Step

- **Agent:** architect
- **Action:** N/A
- **Notes:**
  Creates comprehensive architecture using fullstack-architecture-tmpl. If user generated UI with v0/Lovable, can incorporate the project structure into architecture. May suggest changes to PRD stories or new stories. SAVE OUTPUT: Copy final fullstack-architecture.md to your project's docs/ folder.
- **Requires:** ['prd.md', 'front-end-spec.md']

### Unnamed Step

- **Agent:** pm
- **Action:** N/A
- **Notes:**
  If architect suggests story changes, update PRD and re-export the complete unredacted prd.md to docs/ folder.
- **Requires:** fullstack-architecture.md

### Unnamed Step

- **Agent:** po
- **Action:** N/A
- **Notes:**
  Validates all documents for consistency and completeness. May require updates to any document.

### Unnamed Step

- **Agent:** various
- **Action:** N/A
- **Notes:**
  If PO finds issues, return to relevant agent to fix and re-export updated documents to docs/ folder.

### Unnamed Step

- **Agent:** N/A
- **Action:** guide_project_structure
- **Notes:**
  If user generated UI with v0/Lovable: For polyrepo setup, place downloaded project in separate frontend repo alongside backend repo. For monorepo, place in apps/web or packages/frontend directory. Review architecture document for specific guidance.

### Unnamed Step

- **Agent:** N/A
- **Action:** guide_development_sequence
- **Notes:**
  Based on PRD stories: If stories are frontend-heavy, start with frontend project/directory first. If backend-heavy or API-first, start with backend. For tightly coupled features, follow story sequence in monorepo setup. Reference sharded PRD epics for development order.

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
    A[Start: Greenfield Project] --> B[analyst: project-brief.md]
    B --> C[pm: prd.md]
    C --> D[ux-expert: front-end-spec.md]
    D --> D2{Generate v0 prompt?}
    D2 -->|Yes| D3[ux-expert: create v0 prompt]
    D2 -->|No| E[architect: fullstack-architecture.md]
    D3 --> D4[User: generate UI in v0/Lovable]
    D4 --> E
    E --> F{Architecture suggests PRD changes?}
    F -->|Yes| G[pm: update prd.md]
    F -->|No| H[po: validate all artifacts]
    G --> H
    H --> I{PO finds issues?}
    I -->|Yes| J[Return to relevant agent for fixes]
    I -->|No| K[po: shard documents]
    J --> H
    
    K --> L[sm: create story]
    L --> M{Review draft story?}
    M -->|Yes| N[analyst/pm: review & approve story]
    M -->|No| O[dev: implement story]
    N --> O
    O --> P{QA review?}
    P -->|Yes| Q[qa: review implementation]
    P -->|No| R{More stories?}
    Q --> S{QA found issues?}
    S -->|Yes| T[dev: address QA feedback]
    S -->|No| R
    T --> Q
    R -->|Yes| L
    R -->|No| U{Epic retrospective?}
    U -->|Yes| V[po: epic retrospective]
    U -->|No| W[Project Complete]
    V --> W

    B -.-> B1[Optional: brainstorming]
    B -.-> B2[Optional: market research]
    D -.-> D1[Optional: user research]
    E -.-> E1[Optional: technical research]

    style W fill:#90EE90
    style K fill:#ADD8E6
    style L fill:#ADD8E6
    style O fill:#ADD8E6
    style D3 fill:#E6E6FA
    style D4 fill:#E6E6FA
    style B fill:#FFE4B5
    style C fill:#FFE4B5
    style D fill:#FFE4B5
    style E fill:#FFE4B5
    style N fill:#F0E68C
    style Q fill:#F0E68C
    style V fill:#F0E68C
```

```
