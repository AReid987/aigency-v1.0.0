# Nextra Docs Theme Implementation Plan for xprt-webui

**Objective:** Implement Nextra Docs theme in `apps/xprt-webui` with top navigation bar, glassmorphism navigation bar, collapsible pages sidebar, table of contents, and landing/login/signup pages.

**Plan:**

1.  **Install Nextra Docs Theme**
    *   Verify if `nextra` and `nextra-theme-docs` are installed. If not, install them using `pnpm add nextra nextra-theme-docs`.

2.  **Update \`layout.tsx\`**
    *   **2.1. Implement Basic Docs Layout:** Wrap \`children\` with \`<Layout>\` from \`nextra-theme-docs\`.
    *   **2.2. Configure Top Navigation Bar:** Add navigation links to the \`navigation\` prop of \`<Layout>\`. We'll need to decide on the links.
    *   **2.3. Implement Glassmorphism Navigation Bar:** Style the navigation bar with glassmorphism CSS.
    *   **2.4. Implement Collapsible Sidebar:** Ensure sidebar is configured (should be default with Nextra Docs theme).
    *   **2.5. Implement Table of Contents:** Ensure TOC is enabled (should be default).
    *   **2.6. Move Search Bar to Navigation Bar:** Place the search bar within the navigation bar.

3.  **Create Landing Page (\`page.tsx\`)**
    *   Create \`app/page.tsx\` with login/signup links.

4.  **Create Login/Signup Pages**
    *   Create \`app/login/page.tsx\` and \`app/signup/page.tsx\` with basic forms.

5.  **Implement Authentication (Placeholder)**
    *   Add placeholder authentication logic. Full implementation will depend on the chosen auth mechanism.

6.  **Style Customizations (Glassmorphism Navigation Bar)**
    *   Add CSS for glassmorphism to \`globals.css\` or CSS modules for the navigation bar. Make header sticky.

7.  **Testing and Refinement**
    *   Test all features and refine styles.

**Next Steps:**

After writing this plan to \`nextra-implementation-plan.md\`, we will switch to \`code\` mode to execute this plan step-by-step.