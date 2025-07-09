# Data Requirements Document (DRD) Draft - uXPRT

## 1. Introduction

This document outlines the data requirements for uXPRT, including the data entities, attributes, relationships, and data flow within the system. It is informed by the database schema defined in `src/db/schema.sql` and the Supabase migration `supabase/migrations/20250505222424_create_basic_tables.sql`.

## 2. Data Entities and Attributes

- **users:**

  - `user_id` (UUID, Primary Key, Default: `gen_random_uuid()`) - Unique identifier for the user.
  - `email` (VARCHAR(255), Unique, Not Null) - User's email address.
  - `username` (VARCHAR(255), Unique) - User's username.
  - `created_at` (TIMESTAMP WITH TIME ZONE, Default: `CURRENT_TIMESTAMP`) - Timestamp of user creation.
  - `updated_at` (TIMESTAMP WITH TIME ZONE, Default: `CURRENT_TIMESTAMP`) - Timestamp of last update.
  - `persona_type` (VARCHAR(50)) - Type of user persona.

- **conversations:**

  - `conversation_id` (UUID, Primary Key, Default: `gen_random_uuid()`) - Unique identifier for the conversation.
  - `user_id` (UUID, Not Null, Foreign Key to `users(user_id)`) - User associated with the conversation.
  - `start_time` (TIMESTAMP WITH TIME ZONE, Default: `CURRENT_TIMESTAMP`) - Timestamp when the conversation started.
  - `end_time` (TIMESTAMP WITH TIME ZONE) - Timestamp when the conversation ended.
  - `title` (VARCHAR(255)) - Title of the conversation.
  - `context` (JSONB, Not Null) - JSON object storing conversation context.

- **artifacts:**

  - `artifact_id` (UUID, Primary Key, Default: `gen_random_uuid()`) - Unique identifier for the artifact.
  - `user_id` (UUID, Not Null, Foreign Key to `users(user_id)`) - User who generated the artifact.
  - `conversation_id` (UUID, Foreign Key to `conversations(conversation_id)`) - Conversation associated with the artifact.
  - `artifact_type` (VARCHAR(50), Not Null) - Type of artifact (e.g., PRD, FRD, DRD, ERD).
  - `generated_data` (TEXT, Not Null) - The content of the generated artifact.
  - `created_at` (TIMESTAMP WITH TIME ZONE, Default: `CURRENT_TIMESTAMP`) - Timestamp of artifact creation.
  - `updated_at` (TIMESTAMP WITH TIME ZONE, Default: `CURRENT_TIMESTAMP`) - Timestamp of last update.
  - `version` (INTEGER, Default: 1) - Version number of the artifact.
  - `filename` (VARCHAR(255)) - Filename of the artifact.

- **search_queries:**
  - `query_id` (UUID, Primary Key, Default: `gen_random_uuid()`) - Unique identifier for the search query.
  - `user_id` (UUID, Not Null, Foreign Key to `users(user_id)`) - User who performed the search.
  - `query_text` (TEXT, Not Null) - The text of the search query.
  - `search_time` (TIMESTAMP WITH TIME ZONE, Default: `CURRENT_TIMESTAMP`) - Timestamp of the search.
  - `results` (JSONB) - Optional: Stored search results.

## 3. Data Flow

(Placeholder for Data Flow diagram or description - This will describe how data moves between the user interface, conversational agents, artifact generation modules, and the database.)

## 4. Data Storage

- Data will be stored in a Supabase database (PostgreSQL).
- Artifact files will be stored in Supabase Storage.

## 5. Data Security and Privacy

- User passwords will be stored as hashed values.
- Access to user data and generated artifacts will be restricted based on user authentication and authorization.
- Data transmission will be encrypted using TLS/SSL.
- Compliance with relevant data privacy regulations (e.g., GDPR, CCPA) will be ensured.

## 6. Data Validation and Integrity

- Input data will be validated at the application layer to ensure accuracy and prevent errors.
- Database constraints (e.g., foreign keys, unique constraints) will be used to maintain data integrity.

## 7. Data Retention

- Data retention policies will be defined and implemented based on user requirements and privacy regulations. (Details to be added later).
