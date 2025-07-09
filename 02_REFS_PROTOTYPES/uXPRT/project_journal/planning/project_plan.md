# Project Plan: uXPRT

## 🎯 Objective Summary

uXPRT is a simplified version of XPRT, the Knowledge OS, focused on providing a conversational agent team to guide users through the UX Pipeline. It aims to speed up product development and content creation by automatically generating various artifacts.

## ✨ Key Features Summary

The core features involve a conversational agent team assisting users in:

- Defining target demographic and creating user personas.
- Generating product documentation (PRD, FRD, DRD, ERD).
- Creating diagrams, wireframes, and sitemaps.
- Developing GTM strategy, Lean Canvas, Basic Atomic Design System, Brand voice & Tone, Core values, Brand Identity, and Brand Book.
- Providing web search capabilities for research.

## ⚙️ Technical Considerations

Based on user feedback, the following technologies and frameworks are being considered:

- **Agent Frameworks:** BrowserUse, BlastAI, Open Manus, Proxy Light, Skyvern, Open Operator, Hyperbrowser, Agno, AG2, Magentic One, Suna AI
- **MCP Web Search:** Tavily, Exa, Webresearch, Serper, puppeteer, playwright, stagehand, browserbase
- **Documentation Schema:** zod, pydantic
- **ORM:** Prisma, Drizzle

Decisions on which specific technologies to use will be made during the relevant implementation tasks.

## 🚧 Initial Task Board

### To Do

- [ ] TaskID: TASK-DISC-20250503-235159 | Desc: Define target demographic and create user personas. (MODE: discovery-agent, Prio: H, Refs: project_journal/planning/requirements.md)
- [ ] TaskID: TASK-PLAN-20250503-235159 | Desc: Generate initial product documentation drafts (PRD, FRD, DRD, ERD). (MODE: software-planning, Prio: H, Refs: project_journal/planning/requirements.md)
- [ ] TaskID: TASK-DESIGN-20250503-235159 | Desc: Create initial diagram, wireframe, and sitemap concepts. (MODE: ui-designer, Prio: M, Refs: project_journal/planning/requirements.md)
- [ ] TaskID: TASK-BIZ-20250503-235159 | Desc: Develop initial GTM strategy, Lean Canvas, and Brand elements. (MODE: research-context-builder, Prio: M, Refs: project_journal/planning/requirements.md)
- [ ] TaskID: TASK-AI-20250503-235159 | Desc: Plan implementation of conversational agent guidance logic. (MODE: api-developer, Prio: H, Refs: project_journal/planning/requirements.md)
- [ ] TaskID: TASK-API-20250503-235159 | Desc: Implement core web search integration, considering options like Tavily, Exa, Webresearch, Serper, puppeteer, playwright, stagehand, browserbase. (MODE: api-developer, Prio: H, Refs: project_journal/planning/requirements.md)
- [ ] TaskID: TASK-DB-20250503-235159 | Desc: Design and implement initial database schema for data handling, considering ORMs like Prisma or Drizzle and documentation schemas like zod or pydantic. (MODE: database-specialist, Prio: H, Refs: project_journal/planning/requirements.md)
- [ ] TaskID: TASK-ARCH-20250503-235159 | Desc: Address initial non-functional requirements (Performance, Security, Scalability, Data Privacy). (MODE: technical-architect, Prio: H, Refs: project_journal/planning/requirements.md)

### In Progress

### Completed

- [x] TaskID: TASK-DISC-20250503-234134 | Desc: Define Requirements (MODE: discovery-agent, Task Log: project_journal/tasks/TASK-DISC-20250503-234134.md)
