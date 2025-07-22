---
type: Page
title: 'Story 2.2: Update Story Status via Drag and Drop'
description: null
icon: null
createdAt: '2025-07-10T04:14:27.776Z'
creationDate: 2025-07-09 23:14
modificationDate: 2025-07-09 23:14
tags: []
coverImage: null
---

# Story 2.2: Update Story Status via Drag and Drop

# **Story 2.2: Update Story Status via Drag and Drop**

**Status:** To Do

**Epic:** Agile Project Management

---

### **Story**

- **As a** user,

- **I want to** drag and drop story cards on the Kanban board into different columns,

- **so that** I can easily update their status and reflect the current state of the project.

---

### **Acceptance Criteria (ACs)**

1. Story cards on the Kanban board must be interactive and draggable using a mouse or touch input.

2. When a story card is dropped into a new status column (e.g., from "To Do" to "In Progress"), a request must be sent to the backend to update its status.

3. The board's state must be persistent. After a page refresh, the card must remain in its new column.

4. The UI must provide clear visual feedback during the drag-and-drop operation, such as the card lifting up and the target column being highlighted.

5. The movement of cards should be smooth and fluid, adhering to the "sentient UI" principles.

---

### **Tasks / Subtasks**

- **Frontend:**

    - [ ] Integrate a modern drag-and-drop library (e.g., `dnd-kit`) with the Kanban board component.

    - [ ] Implement the UI logic to provide visual feedback during drag operations (e.g., changing styles on the dragged item and target column).

    - [ ] On a successful drop, trigger an API call to the backend to update the story's status.

    - [ ] Optimistically update the UI to show the card in the new column immediately, before waiting for the API response, to make the interface feel faster.

- **Backend:**

    - [ ] Create a new `PATCH` or `PUT` API endpoint (e.g., `PATCH /api/stories/{storyId}/status`).

    - [ ] The endpoint should accept a new status for the story in the request body.

    - [ ] The endpoint must validate the request and update the story's status in the PostgreSQL database.

---

### **Dev Technical Guidance**

- The frontend should handle the state management of the board optimistically to ensure a smooth user experience. This means updating the local state immediately and then syncing with the backend.

- The backend API must be efficient to handle potentially frequent status updates.

- Animations from Framer Motion should be used to make the drag-and-drop interaction feel fluid and natural. For example, the card could subtly change its angle when lifted, and other cards could animate to make space for it in the new column.

[profile picture](https://lh3.googleusercontent.com/a/ACg8ocIt4GVnDinGqgCInTBr4ufFx6pF7dPWP217mtUtj5Q33uN546U=s64-c)

