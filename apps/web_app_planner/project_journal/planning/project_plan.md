# WebApp Planning Workbook: Next.js & Supabase Refactor Plan

## Project Goal

Refactor the existing WebApp Planning Workbook (currently HTML, Tailwind CSS, Vanilla JS, Firebase) to use Next.js for the frontend, Supabase for authentication and data persistence, and deploy to Vercel.

## Key Technologies

- **Frontend Framework:** Next.js
- **Styling:** Tailwind CSS (integrated with Next.js)
- **Backend as a Service (BaaS):** Supabase (Postgres Database, Authentication)
- **Deployment:** Vercel

## High-Level Phases

### Phase 1: Project Setup & Initial Documentation

- Initialize a new Next.js project.
- Configure Tailwind CSS within the Next.js project.
- Set up Supabase project and obtain API keys.
- Create initial project documentation (README.md, project_plan.md, etc.).
- Define Supabase schema based on existing Firestore data structure.

### Phase 2: Core Application Structure & UI Migration

- Migrate existing HTML structure to Next.js components and pages.
- Rebuild sidebar navigation and content sections using React components.
- Implement Dark/Light mode toggle functionality with Next.js and Tailwind CSS.
- Integrate Google Fonts (Inter) and SVG icons.

### Phase 3: Supabase Integration (Authentication & Data Persistence)

- Implement Supabase authentication for user sign-in (anonymous and email/password if applicable).
- Migrate data persistence logic from Firebase Firestore to Supabase.
  - Adapt `loadWorkbookData` to fetch from Supabase.
  - Adapt save/add/delete functions to interact with Supabase tables.
- Implement real-time data updates using Supabase subscriptions.

### Phase 4: Dynamic List Management

- Re-implement dynamic list creation, addition, and deletion functionalities for Branding Values, User Stories, Features, Wireframes, and Data Points using React state management and Supabase.
- Ensure unique ID generation for list items.

### Phase 5: UI/UX Enhancements & Polish

- Refine UI/UX for a seamless and responsive experience across devices.
- Implement visual feedback (toast notifications) and loading indicators.
- Ensure all form fields and interactive elements are fully functional.

### Phase 6: Deployment & Environment Configuration

- Configure Next.js environment variables for Supabase keys.
- Deploy the application to Vercel.
- Set up Vercel environment variables.
- Verify deployment and functionality.

## Supabase Data Model (Initial Draft - based on Firestore structure)

### Table: `user_workbooks`

- `id`: UUID (Primary Key, Supabase Auth `user.id`)
- `theme`: TEXT (e.g., 'dark', 'light')
- `branding_mission`: TEXT
- `branding_audience`: TEXT
- `branding_personality`: TEXT
- `branding_moodboard`: TEXT
- `goals_problem`: TEXT
- `goals_audience`: TEXT
- `goals_mvp`: TEXT
- `goals_outcomes`: TEXT
- `atomic_color_primary`: TEXT (hex code)
- `atomic_color_secondary`: TEXT (hex code)
- `atomic_color_accent`: TEXT (hex code)
- `atomic_neutral_palette_notes`: TEXT
- `atomic_color_success`: TEXT (hex code)
- `atomic_color_error`: TEXT (hex code)
- `atomic_color_warning`: TEXT (hex code)
- `atomic_color_info`: TEXT (hex code)
- `atomic_font_heading`: TEXT (font family name)
- `atomic_font_body`: TEXT (font family name)
- `atomic_iconography_notes`: TEXT
- `atomic_type_scale_notes`: TEXT
- `atomic_color_scale_notes`: TEXT
- `atomic_molecules_notes`: TEXT
- `atomic_organisms_notes`: TEXT
- `atomic_templates_notes`: TEXT
- `atomic_pages_notes`: TEXT

### Table: `branding_values`

- `id`: UUID (Primary Key)
- `user_workbook_id`: UUID (Foreign Key to `user_workbooks.id`)
- `text`: TEXT

### Table: `user_stories`

- `id`: UUID (Primary Key)
- `user_workbook_id`: UUID (Foreign Key to `user_workbooks.id`)
- `user_type`: TEXT
- `action`: TEXT
- `benefit`: TEXT

### Table: `features`

- `id`: UUID (Primary Key)
- `user_workbook_id`: UUID (Foreign Key to `user_workbooks.id`)
- `name`: TEXT

### Table: `wireframes`

- `id`: UUID (Primary Key)
- `user_workbook_id`: UUID (Foreign Key to `user_workbooks.id`)
- `screen_name`: TEXT
- `key_elements`: TEXT
- `interactions`: TEXT

### Table: `data_points`

- `id`: UUID (Primary Key)
- `user_workbook_id`: UUID (Foreign Key to `user_workbooks.id`)
- `name`: TEXT
- `type`: TEXT
- `description`: TEXT

- [x] Phase 1: Project Setup & Initial Documentation for the WebApp Planning Workbook refactor has been completed.
