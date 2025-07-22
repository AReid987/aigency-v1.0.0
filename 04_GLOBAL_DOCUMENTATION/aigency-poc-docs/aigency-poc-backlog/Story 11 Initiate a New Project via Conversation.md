---
type: Page
title: 'Story 1.1: Initiate a New Project via Conversation'
description: null
icon: null
createdAt: '2025-07-10T03:51:57.489Z'
creationDate: 2025-07-09 22:51
modificationDate: 2025-07-09 22:52
tags: []
coverImage: null
---

# Story 1.1: Initiate a New Project via Conversation

# **Story 1.1: Initiate a New Project via Conversation**

**Status:** Done

**Epic:** The Aigency Collaboratory & Development Core

---

### **Story**

- **As a** solo developer,

- **I want to** start a new project and describe my goal for a simple web application to the Aigency Squad,

- **so that** they can understand my vision and begin the development process.

---

### **Acceptance Criteria (ACs)**

1. Given I am an authenticated user on the main dashboard, I must see a clear and prominent option (e.g., a button or card) to start a new project.

2. When I initiate a new project, I must be prompted to provide a name for it.

3. After naming the project, I must be taken to a dedicated, full-screen conversational interface (The "Collaboratory").

4. The conversational interface must contain an input field where I can type my project description and a "send" button.

5. After I send my initial message (e.g., "I want a personal portfolio site with a bio and a contact form"), the message must appear in the chat history.

6. An AI agent must issue a response in the chat, acknowledging my request and confirming that it understands the initial goal (e.g., "Understood. A personal portfolio site. I'm ready to help you build it. Let's start by creating the project structure.").

---

### **Tasks / Subtasks**

- **Frontend:**

    - [x] Design and implement a "New Project" button on the main dashboard.

    - [x] Create a modal or dedicated page for the user to name their new project.

    - [x] Build the core UI for the "Collaboratory" conversational view, including the chat history display and message input form.

    - [x] Implement the logic to send the user's message to the backend API.

    - [x] Implement the logic to receive and display the AI agent's response in the chat interface.

- **Backend:**

    - [x] Create a `POST /projects` API endpoint to handle the creation of a new project, storing its name and associating it with the user.

    - [x] Create a `POST /projects/{projectId}/messages` API endpoint to handle new messages from the user.

    - [ ] Integrate the initial AI agent logic to provide a simple acknowledgment response to the user's first message.

---

### **Dev Technical Guidance**

- The UI for this flow should adhere to the "sentient" design principles outlined in the Frontend Architecture document.

- All state related to the conversation should be managed appropriately, likely using Zustand as defined in the frontend architecture.

- API calls must be authenticated and authorized, ensuring a user can only interact with their own projects.

[profile picture](https://lh3.googleusercontent.com/a/ACg8ocIt4GVnDinGqgCInTBr4ufFx6pF7dPWP217mtUtj5Q33uN546U=s64-c)

