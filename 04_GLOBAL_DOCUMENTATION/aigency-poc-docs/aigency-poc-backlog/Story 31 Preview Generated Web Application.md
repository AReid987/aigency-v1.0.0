---
type: Page
title: 'Story 3.1: Preview Generated Web Application'
description: null
icon: null
createdAt: '2025-07-10T04:15:29.508Z'
creationDate: 2025-07-09 23:15
modificationDate: 2025-07-09 23:15
tags: []
coverImage: null
---

# Story 3.1: Preview Generated Web Application

Of course. Here is the next story from the backlog, "Story 3.1," written in its long-form version.

---

# **Story 3.1: Preview Generated Web Application**

**Status:** To Do

**Epic:** Prototyping & Visualization Showcase

---

### **Story**

- **As a** user,

- **I want to** see the web application rendered in a live, interactive preview pane within the platform after the Aigency Squad generates it,

- **so that** I can immediately test the output without needing to deploy it myself.

---

### **Acceptance Criteria (ACs)**

1. A "Showcase" or "Preview" area must exist within the project workspace.

2. After a web application is successfully generated and built (following Story 1.3 or 1.4), a preview of the application must be automatically rendered in this area.

3. The preview must be fully interactive; I can click buttons, fill out forms, and navigate as if it were a deployed website.

4. The preview pane must include controls to refresh the preview or open the application in a new browser tab.

5. The process should feel integrated, with an AI agent announcing that the preview is ready for review.

---

### **Tasks / Subtasks**

- **Frontend:**

    - [ ] Design and build the UI for the "Showcase" area, including the preview pane and control buttons (Refresh, Open in New Tab).

    - [ ] Implement the logic to render an external or sandboxed URL within an `<iframe>` or a similar component.

    - [ ] The UI should update automatically to show the preview once the backend signals that the build is complete and the app is ready.

- **Backend:**

    - [ ] Implement a sandboxed environment where the generated Next.js application can be securely built and run.

    - [ ] The system must dynamically assign a unique, temporary URL for each running preview.

    - [ ] Create a mechanism (e.g., a webhook or WebSocket message) to notify the frontend when the preview is ready and provide the URL.

    - [ ] Ensure the sandboxed environment has the necessary dependencies installed (`pnpm install`) and can run the `pnpm dev` or `pnpm start` command.

---

### **Dev Technical Guidance**

- Security is paramount for the sandboxed environment. The environment must be isolated from the main platform infrastructure to prevent any potential security risks from the generated code.

- Using a service like an isolated Docker container for each preview is a recommended approach.

- The communication between the main platform and the sandboxed environment needs to be robust and secure.

- The user experience should be seamless. The user shouldn't need to know the technical details of the sandboxing; they should just see their app appear in the preview pane.

[profile picture](https://lh3.googleusercontent.com/a/ACg8ocIt4GVnDinGqgCInTBr4ufFx6pF7dPWP217mtUtj5Q33uN546U=s64-c)

