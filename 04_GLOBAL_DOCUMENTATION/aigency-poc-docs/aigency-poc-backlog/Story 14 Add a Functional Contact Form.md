---
type: Page
title: 'Story 1.4: Add a Functional Contact Form'
description: null
icon: null
createdAt: '2025-07-10T04:04:22.544Z'
creationDate: 2025-07-09 23:04
modificationDate: 2025-07-09 23:04
tags: []
coverImage: null
---

# Story 1.4: Add a Functional Contact Form

# **Story 1.4: Add a Functional Contact Form**

**Status:** To Do

**Epic:** The Aigency Collaboratory & Development Core

---

### **Story**

- **As a** solo developer,

- **I want to** ask the Aigency Squad to add a functional contact form to my personal portfolio site, now that I have a running application,

- **so that** visitors can send me messages.

---

### **Acceptance Criteria (ACs)**

1. Given I have a running application, I can make a request in the Collaboratory like, "add a contact form with fields for name, email, and message."

2. An AI agent must acknowledge the request and then generate the new frontend code for a `ContactForm` component.

3. The generated form must include input fields for "Name" and "Email," a textarea for "Message," and a "Submit" button.

4. The AI agent must also create a new backend API endpoint (e.g., `POST /api/contact`) in the FastAPI application to receive the form data.

5. The frontend form must be wired up to the new backend endpoint, sending the data on submission.

6. The agent must display the code changes for both the frontend component and the backend endpoint in the chat interface for my review.

7. After running the application with the new code, the contact form must be visible and functional on the home page.

---

### **Tasks / Subtasks**

- **Frontend:**

    - [ ] Create a new React component file `ContactForm.tsx` in `apps/web/components/ui/`.

    - [ ] Add form inputs for name, email, and message using Radix UI primitives for accessibility.

    - [ ] Style the form and inputs using Tailwind CSS.

    - [ ] Implement the logic to capture form data and send it to the backend on submit.

    - [ ] Update the main page (`page.tsx`) to import and render the `ContactForm` component.

- **Backend:**

    - [ ] In `apps/api/main.py`, add a new `POST` endpoint at `/api/contact`.

    - [ ] The endpoint should define a Pydantic model to validate the incoming request body (name, email, message).

    - [ ] For the POC, the endpoint can simply log the received message to the console and return a success response.

---

### **Dev Technical Guidance**

- The contact form should be a self-contained component that can be easily placed on any page.

- The frontend should handle basic client-side validation (e.g., checking for empty fields) before submission to provide a better user experience.

- The API endpoint should follow RESTful principles and include appropriate status codes for success and error responses.

- The entire interaction should be conversational, with the agent explaining the changes it's making as it generates the code.

[profile picture](https://lh3.googleusercontent.com/a/ACg8ocIt4GVnDinGqgCInTBr4ufFx6pF7dPWP217mtUtj5Q33uN546U=s64-c)

