/\*

- Filename: /Users/antonioreid/01_DOING/XPRT/project_journal/context/roo_commander_guidelines.md
- Path: /Users/antonioreid/01_DOING/XPRT
- Created Date: Monday, April 7th 2025, 7:34:47 pm
- Author: Antonio J. Reid
-
- Copyright (c) 2025 10xAigency
  \*/

/\*

- Filename: /Users/antonioreid/01_DOING/XPRT/project_journal/context/roo_commander_guidelines.md
- Path: /Users/antonioreid/01_DOING/XPRT
- Created Date: 2025-04-07
- Purpose: Roo Commander internal coordination guidelines integrating modular project knowledge base
  \*/

# Roo Commander Coordination Guidelines

## Core Knowledge Base Structure

All project context, progress, and plans are centralized in these files:

- **User Profile:**
  `project_journal/context/user_profile.md`

- **Active Context (focus, goals, blockers, risks):**
  `project_journal/context/active_context.md`

- **Product Context (vision, personas, use cases, differentiators):**
  `project_journal/context/product_context.md`

- **System Patterns (architecture, best practices, future ideas):**
  `project_journal/context/system_patterns.md`

- **Progress Log (milestones, lessons, blockers):**
  `project_journal/progress/progress_log.md`

- **Backlog (deferred tasks):**
  `project_journal/planning/backlog.md`

- **Decisions:**
  `project_journal/decisions/YYYYMMDD-topic.md`

---

## Coordination Principles

- **Before planning or delegating:**
  Review **Active Context**, **Product Context**, **Backlog**, and **Progress Log**.

- **When resolving project status:**
  Summarize from **Active Context** and **Progress Log**.

- **When updating architecture or practices:**
  Append or modify **System Patterns**.

- **When recording milestones or lessons:**
  Update **Progress Log**.

## Handoff & Milestone Integration

- **Continuously assess** project context relevance during coordination.
- **Create a handoff document** (in `/handoffs/`, numbered sequentially) when:
  - Finishing a discrete project segment
  - Context window becomes diluted (~30% irrelevant)
  - Debugging exceeds 5 exchanges without resolution
  - After 10+ conversation rounds
- **Create a milestone folder** (e.g., `/handoffs/2-feature-X/`) when:
  - Major feature/component completes
  - 3-5 handoffs accumulate
  - Critical problem solved
- **Handoff files** capture session-specific learnings, problems, discoveries, deviations, and references.
- **Milestone summaries** consolidate multiple handoffs into concise, future-proof documentation.
- **Do NOT pre-create empty folders/files**; generate them dynamically as triggers occur.
- **Prompt user for confirmation or provide draft** when a handoff or milestone is warranted.
- **Follow templates defined in** `/handoff/0-Instuction/` for content structure.

- **When new tasks are deferred:**
  Add to **Backlog**.

- **When decisions are finalized:**
  Record in a dated file under **Decisions**.

---

## Goal

Maintain a **modular, up-to-date, single source of truth** for project coordination, minimizing fragmentation and improving traceability.
