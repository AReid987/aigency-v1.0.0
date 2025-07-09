# Textual TUI for Proxy-Lite - Implementation Plan

## 1. Information Gathering and Context

*   Analyzed the `packages/proxy-lite/src/proxy_lite/app.py` file to understand the Streamlit UI's functionality.
*   Identified the storage locations for logs, gifs, trajectories, and screenshots:
    *   `/packages/proxy-lite/gifs/`
    *   `/packages/proxy-lite/local_trajectories/`
    *   `/packages/proxy-lite/screenshots/`
*   Confirmed the availability of PocketBase and the general approach for integration.

## 2. Design the Textual TUI

*   **Layout:**
    *   Header: "Proxy-Lite TUI".
    *   Main content area:
        *   Logger container.
        *   Browser container with tabs.
*   **Widgets:**
    *   `textual.widgets.Header` for the header.
    *   `textual.widgets.Footer` for any potential footer information.
    *   `textual.widgets.RichLog` widget for the logger container.
    *   `textual.widgets.TabbedContent` widget for the browser container.
    *   Within the tabs:
        *   Logs: `textual.widgets.RichLog` (from PocketBase).
        *   Gifs: `textual.widgets.Image` (from `/packages/proxy-lite/gifs/`).
        *   Trajectories: Custom widget (from PocketBase).
        *   Screenshots: `textual.widgets.Image` (from `/packages/proxy-lite/screenshots/`).
*   **Color Palette:**
    *   Use the provided brand color palette for both light and dark modes:
        *   Dark mode:
            *   Primary: `#0F172B`
            *   Secondary: `#8B8D98`
            *   Neutral Dark: `#111111`
            *   Neutral Light: `#B2B3BD`
        *   Light mode:
            *   Primary: `#3D63DD`
            *   Secondary: `#00A6F4`
            *   Neutral Dark: `#45556C`
            *   Neutral Light: `#F5F5F4`
*   **Mermaid Diagram:**

```mermaid
graph LR
    A[Proxy-Lite TUI] --> B(Header)
    A --> C(Main Content)
    B --> D{Title}
    C --> E(Logger Container)
    C --> F(Browser Container)
    E --> G[RichLog: Logger Widget (from PocketBase)]
    F --> H{TabbedContent}
    H --> I[Logs Tab]
    H --> J[Gifs Tab]
    H --> K[Trajectories Tab]
    H --> L[Screenshots Tab]
    I --> M[RichLog: Log List (from PocketBase)]
    J --> N[Image: Gif Viewer (from /packages/proxy-lite/gifs/)]
    K --> O[Trajectory Viewer (from PocketBase)]
    L --> P[Image: Screenshot Viewer (from /packages/proxy-lite/screenshots/)]
    style A fill:#f9f,stroke:#333,stroke-width:2px
```

## 3. Implement the TUI

*   **Code:** Write the Python code using the Textual library.
*   **Logger:** Implement the logger with execution stages and statuses (e.g., `Thinking: ERROR`).
*   **PocketBase Integration:**
    *   Initialize PocketBase as a dependency.
    *   Create collections in PocketBase for logs and trajectories.
    *   Modify the `Runner` or related classes to write logs and trajectories to PocketBase.
    *   Implement the browsing features for logs and trajectories by fetching data from PocketBase.
*   **Browsing Features:** Implement browsing for gifs and screenshots (reading from the file system).
*   **Configuration:** Handle configuration settings.

## 4. Test and Refine

*   Test the TUI thoroughly.
*   Refine the code and UI based on testing and feedback.

## 5. Present the Solution

*   Provide the complete Python code.
*   Explain the code's functionality and how to run the TUI, including PocketBase setup.
*   Provide a demonstration command (if possible).
