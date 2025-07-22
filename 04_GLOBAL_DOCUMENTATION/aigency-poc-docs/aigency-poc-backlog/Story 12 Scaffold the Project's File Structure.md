---
type: Page
title: 'Story 1.2: Scaffold the Project''s File Structure'
description: null
icon: null
createdAt: '2025-07-10T03:54:43.062Z'
creationDate: 2025-07-09 22:54
modificationDate: 2025-07-09 22:55
tags: []
coverImage: null
---

# Story 1.2: Scaffold the Project's File Structure

# **Story 1.2: Scaffold the Project's File Structure**

**Status:** To Do

**Epic:** The Aigency Collaboratory & Development Core

---

### **Story**

- **As a** solo developer,

- **I want** the Aigency Squad to create the foundational file and folder structure for my new web application after my initial request is understood,

- **so that** I can see tangible progress and have a correct starting point for development.

---

### **Acceptance Criteria (ACs)**

1. Given the Aigency Squad has acknowledged my initial project goal (from Story 1.1), an AI agent must inform me that it will now generate the project's scaffolding.

2. The file and folder structure must be created in the system's backend, adhering to the architecture defined in the System Architecture Document.

3. The structure must be a Turborepo monorepo with distinct `apps/web` and `apps/api` directories.

4. A visual representation of the new project's file and folder structure must be displayed to me within the "Collaboratory" interface.

5. The system must create placeholder configuration files, including a root `package.json`, a `turbo.json`, a `package.json` for the `web` app, and a `pyproject.toml` for the `api` app.

6. After the structure is displayed, I must have an opportunity to review and approve it before the squad proceeds to the next step.

---

### **Tasks / Subtasks**

- **Frontend:**

    - [ ] Design and build a UI component to display a file tree structure within the chat interface.

    - [ ] Implement the logic to receive the file structure data from the backend and render it using the new component.

    - [ ] Create "Approve" and "Request Changes" buttons that appear after the file structure is displayed.

- **Backend:**

    - [x] Create a "Project Scaffolding" service or function that generates the complete file and folder structure as defined in the System Architecture.

    - [x] This service should be triggered after the successful completion of Story 1.1.

    - [x] The service must generate the correct boilerplate configuration files (`package.json`, `turbo.json`, `pyproject.toml`).

    - [x] The service must return a JSON representation of the created file structure to the frontend.

    - [ ] Implement logic to handle the user's approval before proceeding to the next story.

---

### **Dev Technical Guidance**

- The backend service should use the approved architecture: a Turborepo monorepo with a Next.js frontend and a Python (FastAPI) backend.

- The frontend file tree component should be reusable and could be considered a "Molecule" in our Atomic Design system.

- The process should feel seamless to the user, like a continuous part of the conversation. The AI agent's messages should guide the user through the step clearly.

[profile picture](https://lh3.googleusercontent.com/a/ACg8ocIt4GVnDinGqgCInTBr4ufFx6pF7dPWP217mtUtj5Q33uN546U=s64-c)

