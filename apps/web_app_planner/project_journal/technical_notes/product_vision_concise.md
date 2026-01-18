# Product Vision

## Overview

### Digital Workbook

- Structured
- Interactive
- Web App Planning Worflow

### Multi Agent System

- Guided
- Conversational
- Adaptive

#### Generates

- Planning Artifacts
- Working Code
- Working Prototypes

### MVP

#### Core Workbook Functionality

- Users can define and document:
    - Branding
    - Goals & Objectives
    - User Stories
    - Their App's Core Features
    - Wireframes
    - Foundational Atomic Design System elements
     - Key Data Points
- Process is interactive & conversational
- User Authentication
- Persistent Data Storage

#### Expanded Vision

- More comprehensive planning
    - Specialized Agents
    - Advanced code generation
    - Integrated Design System Management
    - Enhanced Collaboration Tools
    - Export to PDF/Markdown
    - Seamless integration with the Broader SDLC

### Scope

#### Core Platform

- Next.js application deployed on Vercel
-  User Authentication via Clerk
- Data Persistence:
  - User workbook saved to Supabase with RLS

### Multi Agent System

#### Orchestrator

- Primary UI
- Conversational Interface
- Task Orchestration

#### Planner

- Requirements Gathering
- Planning Artifacts Generation
- Project Structure Generation

#### UI Designer

- Wireframes
- Prototypes
- Design System Management

### Workbook Sections

#### Branding

- Conversation Inputs
  - Mission Statement
  - Target Audience
  - Brand Voice & Tone
  - Mood Board
- Dynamic List for Core Values

#### Goals & Objectives

- Conversation Inputs
  - Problem Statement
  - Target Audience
  - MVP Functionalities
  - Desired Outcomes

#### User Stories

- Conversation Inputs
  - User Type
  - Action
  - Benefit
- Dynamic List for Add/Edit/Delete

#### Core Features

- Conversation Inputs
  - Feature Identification/Prioritization
- Dynamic List for Add/Edit/Delete

#### Wireframes

- Conversation Inputs
  - Description of screens
    - Name
    - Purpose
    - Key Elements
    - User Interactions
- Agent Generated Wireframes & Prototypes

### Atomic Design System

#### Atoms

- Conversation Inputs
  - Brand Color Palette
  - Neutral Palette Notes
  - Semantic Color Palette
  - Typography
  - Iconography
  - Type Scale
  - Color Scales

#### Molecules, Organisms, Templates, Pages

- Conversation Inputs
  - Conventional Definitiions
    - Component Hierarchy
    - Component Relationships

#### Key Data Points

- Conversation Inputs
  - Identification of Key data entities & relationships
  - Agent Suggested Data Scheme

#### UI & UX

- Clean, modern UI
  - Tailwind CSS 4,
  - Radix UI,
  - and ShadCN
- Animations powered by
  - Framer Motion
  - and anime.js
- Intuitive sidebar navigation with active section highlighting
- Dark/Light mode toggle with preference saved to Supabase
- Toast notifications for user feedback (save, error)
- Loading indicators for asynchronous operations
- Responsive design (mobile-first focus)
- Interactive Conversational UI
  - Visible Agent Transitions
- Visualization of Agent Work
- xyFlow Canvas

## Functional Requirements

### FR1: Core Platform & User Session

- Authentication via Clerk
- Authentication via tokens
- Persistent Data Storage via Supabase with Row Level Security
- Interactive Conversational UI
- Visualization of Agent Work
- xyFlow Canvas
- Maintain conversation context across sessions
- Light/Dark mode toggle
- Theme preference saved to Supabase

### FR2: Multi Agent System

- Orchestrator to manage conversation flow
- Planner to generate planning artifacts
- UI Designer to generate wireframes & prototypes
- Communication via Standard message format
- Visual indication when transitioning between agents
- memory system to maintain conversation context
- Graceful failure handling

### FR3: Convseration & Planning

- User can describe their app in natural language
- Agents ask clarifying questions
- Agents generate structured PRD from conversation
- Users can provide feedback on generated artifacts
- Agents incorporate feedback into revised artifacts

### FR4: Visualization & Interface

- Convsersations & artifacts are visualized on xyFlow canvas
- User can navigate conversational history
- Users can branch conversations to explore alternatives
- Agents provide visual indicators of thinking process
- System display artifacts in appropriate formats

### FR5: Prototype Generation

- Agents generate Next.js prototypes based on planning artifacts
- Prototypes include core artifacts from planning
- Prototypes are interactive and navgiable between screens
- Prototypes connect to backend system for data persistence
- Users can downloand or deploy prototypes

