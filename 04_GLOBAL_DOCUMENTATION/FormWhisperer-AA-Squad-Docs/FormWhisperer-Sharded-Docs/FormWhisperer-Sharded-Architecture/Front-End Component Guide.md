---
type: Page
title: Front-End Component Guide
description: null
icon: null
createdAt: '2025-07-11T09:14:25.196Z'
creationDate: 2025-07-11 04:14
modificationDate: 2025-07-11 04:14
tags: []
coverImage: null
---

# Front-End Component Guide

## Component Breakdown & Implementation Details

This section outlines the conventions and templates for defining UI components. The AI agent MUST follow the "Template for Component Specification" below whenever a new component is identified for development.

### Component Naming & Organization

- **Component Naming Convention:** PascalCase for files and component names (e.g., `UserProfileCard.tsx`). All component files MUST follow this convention.

- **Organization:** Globally reusable components in `src/components/ui/` or `src/components/layout/`. Feature-specific components co-located within their feature directory, e.g., `src/features/feature-name/components/`.

### Template for Component Specification

For each significant UI component identified from the UI/UX Specification and design files (Figma), the following details MUST be provided. The level of detail MUST be sufficient for an AI agent or developer to implement it with minimal ambiguity.

#### Component: `{ComponentName}` (e.g., `PersonaInputForm`, `HitlPromptDisplay`)

- **Purpose:** {Briefly describe what this component does and its role in the UI. MUST be clear and concise.}

- **Source File(s):** {e.g., `src/features/persona/components/PersonaInputForm.tsx`. MUST be the exact path.}

- **Visual Reference:** {Link to specific Figma frame/component, or Storybook page. REQUIRED.}

- **Props (Properties):**

    | Prop Name       | Type                                                                       | Required? | Default Value | Description                                                                                      |
    | :-------------- | :------------------------------------------------------------------------- | :-------- | :------------ | :----------------------------------------------------------------------------------------------- |
    | `data`          | `{ any specific interface for data }`                                      | Yes       | N/A           | Data object required for component display or function.                                          |
    | `onSave`        | `(data: T) => void`                                                        | No        | N/A           | Callback function triggered on save action.                                                      |
    | `{anotherProp}` | `{Specific primitive, imported type, or inline interface/type definition}` | {Yes/No}  | {If any}      | {MUST clearly state the prop's purpose and any constraints, e.g., 'Must be a positive integer.'} |

- **Internal State (if any):**

    | State Variable   | Type                      | Initial Value                 | Description                                      |
    | :--------------- | :------------------------ | :---------------------------- | :----------------------------------------------- |
    | `formValues`     | `{ form data interface }` | `{ initial data from props }` | Manages the current state of form inputs.        |
    | `{anotherState}` | `{type}`                  | `{value}`                     | {Description of state variable and its purpose.} |

- **Key UI Elements / Structure:**

    ```html
    <form>
      <label for="name">Name:</label>
      <input id="name" type="text" value="{formValues.name}" />
      <button type="submit">Save</button>
    </form>
    ```

- **Events Handled / Emitted:**

    - **Handles:** {e.g., `onChange` for input fields, `onSubmit` for forms, `onClick` for buttons.}

    - **Emits:** {If the component emits custom events/callbacks not covered by props, describe them with their exact signature. e.g., `onFormChange: (payload: { field: string; value: any }) => void`}

- **Actions Triggered (Side Effects):**

    - **State Management:** {e.g., "Updates local `formValues` state on input change." OR "Dispatches `personaSlice.actions.updatePersonaField(payload)` to global state." Action payload MUST match the defined action creator.}

    - **API Calls:** {Specify which service/function from the "API Interaction Layer" is called. e.g., "Calls `personaService.savePersona(formData)` from `src/services/personaService.ts` on form submit. Success response updates global persona state. Error response dispatches `uiSlice.actions.showErrorToast({ message: 'Failed to save persona' })`."}

- **Styling Notes:**

    - {MUST reference specific Design System component names (e.g., "Uses `<Button variant='primary'>` from UI library") OR specify Tailwind CSS classes / CSS module class names to be applied (e.g., "Container uses `p-4 bg-white rounded-lg shadow-md`. Title uses `text-xl font-semibold`.") OR specify SCSS custom component classes to be applied (e.g., "Container uses `@apply p-4 bg-white rounded-lg shadow-md`. Title uses `@apply text-xl font-semibold`."). Any dynamic styling logic based on props or state MUST be described. If Tailwind CSS is used, list primary utility classes or `@apply` directives for custom component classes. AI Agent should prioritize direct utility class usage for simple cases and propose reusable component classes/React components for complex styling patterns.}

- **Accessibility Notes:**

    - {MUST list specific ARIA attributes and their values (e.g., `aria-label="User profile card"`, `role="article"`), required keyboard navigation behavior (e.g., "Tab navigates through form fields in logical order. Inputs are focusable and editable."), and any focus management requirements (e.g., "On error, focus shifts to the first invalid field.").}

### Foundational Components (Conceptual)

- **Input Fields:** Text, Number, Email (standard HTML with clean borders, consistent sizing).

- **Buttons:** Primary (e.g., "Save," "Submit"), Secondary (e.g., "Cancel," "Skip").

- **Radio Buttons / Checkboxes:** Standard, accessible styling.

- **Dropdowns:** Standard, accessible styling.

- **Toasts/Notifications:** For HITL prompts and completion confirmations within the messaging app.

