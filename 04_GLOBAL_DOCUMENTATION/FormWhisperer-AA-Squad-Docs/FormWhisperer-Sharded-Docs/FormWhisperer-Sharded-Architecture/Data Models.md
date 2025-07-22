---
type: Page
title: Data Models
description: null
icon: null
createdAt: '2025-07-11T08:37:07.305Z'
creationDate: 2025-07-11 03:37
modificationDate: 2025-07-11 03:37
tags: []
coverImage: null
---

# Data Models

### Core Application Entities / Domain Objects

#### Persona

- **Description:** Represents a simulated user profile for form completion.

- **Schema / Interface Definition:**

    ```typescript
    export interface Persona {
      id: string; // Unique identifier for the persona
      userId: string; // ID of the human user this persona belongs to
      name: string; // Display name of the persona (e.g., "My Default Persona", "Tech Enthusiast")
      demographics: {
        ageRange?: string; // e.g., "25-34"
        gender?: string; // e.g., "Male", "Female", "Non-binary"
        incomeRange?: string; // e.g., "50k-75k"
        raceEthnicity?: string[]; // e.g., ["White", "Asian"]
        educationLevel?: string; // e.g., "Bachelors"
        country?: string;
        // ... more demographic details
      };
      preferences: {
        productCategories?: string[]; // e.g., ["Electronics", "Software"]
        shoppingHabits?: string; // e.g., "Online frequently"
        // ... more specific preferences
      };
      opinions: {
        [topic: string]: string; // Key-value pairs for specific opinions, e.g., "abortion": "legal", "AI_ethics": "regulated"
      };
      responseStyle: {
        verbosity?: "concise" | "moderate" | "verbose";
        tone?: "formal" | "neutral" | "casual";
        // ... other stylistic elements
      };
      createdAt: Date;
      updatedAt: Date;
    }
    ```

- **Validation Rules:** `userId` must be a valid UUID. `name` max length 100 characters. Demographic fields should conform to predefined enum values where applicable.

#### SurveyCompletionRecord

- **Description:** Stores metadata and details of a completed survey by an AI agent.

- **Schema / Interface Definition:**

    ```typescript
    export interface SurveyCompletionRecord {
      id: string; // Unique ID for the completion record
      personaId: string; // ID of the persona used
      surveyUrl: string; // URL of the completed survey
      platformName: string; // Name of the survey platform
      completionStatus: "completed" | "partial" | "failed" | "hitl_paused";
      startTime: Date;
      endTime?: Date;
      durationSeconds?: number;
      responses: Array<{ // Optional: store key responses for analysis
        question: string;
        answer: string;
        questionType: "text" | "dropdown" | "radio" | "checkbox" | "open_ended";
        hitlInvolved: boolean; // Was HITL used for this answer?
      }>;
      hitlRequests: Array<{ // Log of HITL interactions for this survey
        requestId: string;
        timestamp: Date;
        question: string;
        context: string;
        humanResponse?: string;
      }>;
      notes: string; // Any notes or errors during completion
    }
    ```

### Database Schemas (MongoDB Collections)

#### `personas` Collection

- **Purpose:** Stores `Persona` documents.

- **Schema Definition:** Corresponds to the `Persona` interface above, with appropriate indexing on `userId` and `id`.

#### `surveyCompletionRecords` Collection

- **Purpose:** Stores `SurveyCompletionRecord` documents.

- **Schema Definition:** Corresponds to the `SurveyCompletionRecord` interface above, with indexing on `personaId`, `completionStatus`, and `startTime`.

