# Aigency Frontend Architecture

## 1. Core Philosophy & Foundational Approach

### Component Architecture:

#### Atomic Design

We will structure our components using Atomic Design principles (Atoms -> Molecules -> Organisms). We'll start with base, unstyled Atoms from Radix UI for accessibility, compose them into functional Molecules, and then into larger Organisms. This ensures a highly reusable and consistent component library.

### Styling Approach:

#### Tailwind CSS with a Twist

We will use Tailwind CSS for all utility-first styling. To create the "living, glassy" feel, we will define a set of custom theme classes in our tailwind.config.js for glassmorphism effects, fluid animations, and gradient glows that we can easily apply to components.

### Animation:

#### Framer Motion

All animations, from simple button presses to complex page transitions and the "liquid" feel, will be handled by Framer Motion. We'll create a library of reusable animation variants to ensure a consistent and high-quality user experience.

### State Management:

#### Zustand

For complex, application-wide state (like managing the user's session or the status of AI agents), we will use Zustand. It is a small, fast, and scalable state-management solution that is simpler than Redux but very powerful.

## 1. Detailed Frontend Directory Structure

This structure is designed to be highly organized, making it easy to locate files, manage features, and reuse components.

src/
├── app/                        # Next.js App Router: MUST contain route segments, layouts, and page components.
│   ├── (features)/             # Feature-based routing groups (e.g., dashboard, projects).
│   ├── api/                    # API Routes for frontend-specific backend handlers.
│   ├── globals.css             # MUST contain base styles, CSS variables, and Tailwind directives.
│   └── layout.tsx              # Root layout for the entire application.
├── components/                 # Shared/Reusable UI Components.
│   ├── ui/                     # Atomic UI elements (Button, Input, Card). MUST contain only generic, reusable UI elements.
│   ├── layout/                 # Layout components (Header, Footer, Sidebar).
│   └── (feature-specific)/     # Components used only by a single feature.
├── features/                   # Feature-specific logic, hooks, and services.
├── hooks/                      # Global/sharable custom React Hooks.
├── lib/                        # Utility functions, helpers, constants.
├── store/                      # Global state management setup (Zustand).
├── styles/                     # Additional global styles or theme configuration.
└── types/                      # Shared TypeScript type definitions.
1. Component Breakdown & Implementation Details
This section defines the pattern for how all components will be specified.

### Component: Button (Atom)

#### Purpose:

- The primary interactive element for user actions, designed to feel responsive and "liquid."

#### Source File:

- src/components/ui/Button.tsx

#### Props:

|Prop Name	| Type	| Required?	| Default Value	| Description |
|---	|---	|---	|---	|---	|
| variant	| `'primary' \ |	'secondary' \ |	'ghost' \	| 'glass'` |
| size	| `'sm' \ |	'md' \	| 'lg'` |
| onClick |	() => void	| No | 	N/A	 | Callback function for click events. |


#### Styling Notes:

- We will use Tailwind CSS with the cva (class-variance-authority) library to manage the different variants and sizes. All buttons will feature a "liquid" press animation using Framer Motion. The 'glass' variant will use our custom glassmorphism theme styles.

#### Accessibility Notes:

- We will build this on top of the Radix UI button primitive to ensure it is fully accessible, focusable, and keyboard-navigable out-of-the-box.

### Component:

#### Card (Molecule)

#### Purpose:

- A container for grouping related content that embodies the "glassy" aesthetic of our UI.

#### Source File:

- src/components/ui/Card.tsx

#### Styling Notes:

- This component will be a prime example of our style. It will use Tailwind CSS utility classes like backdrop-blur-lg, border, border-white/20, and bg-white/10 to create a semi-transparent, frosted-glass effect.
