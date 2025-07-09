# Interactive Knowledge Graph Visualization

This project demonstrates an interactive 3D knowledge graph visualization built with React, Three.js (via React Three Fiber), and a Python (FastAPI) backend for NLP-powered graph generation.

## Project Structure

```
/highlight_demos
├── public/
│   ├── index.html         # Main HTML page
│   ├── manifest.json      # Web app manifest
│   └── (favicon.ico, logo192.png, etc.) # Static assets
├── src/
│   ├── highlight_demos/   # Main application source code
│   │   ├── components/
│   │   │   └── KnowledgeGraph.jsx # React component for 3D graph visualization
│   │   ├── App.js             # Main React application component
│   │   ├── App.css            # Styles for the App component
│   │   ├── index.js           # Entry point for React app
│   │   ├── index.css          # Global styles
│   │   ├── reportWebVitals.js # Performance reporting (Create React App standard)
│   │   ├── api.py             # FastAPI API for NLP processing
│   │   └── nlp_system.py      # Python class for NLP tasks and graph generation
│   └── (other CRA default files if any, like setupTests.js)
├── .env.example         # Example environment variables
├── pyproject.toml       # Python dependencies (managed by PDM)
├── package.json         # Node.js dependencies
└── README.md            # This file
```

## Prerequisites

*   **Node.js and npm (or Yarn):** For running the React frontend.
*   **Python 3.8+ and PDM:** For running the FastAPI backend. (PDM will be used for package management).
*   **Ollama:** For serving the local LLM. You will need to have Ollama installed and running. See <mcurl name="Ollama official website" url="https://ollama.com"></mcurl> for installation instructions.
*   **NLP Model (via Ollama):** The application is configured to use a model served by Ollama (default: `gemma3:latest`). You need to ensure this model (or your chosen alternative) is pulled into your Ollama instance (e.g., `ollama pull gemma3:latest`).

## Setup

### 1. Clone the Repository (if applicable)

```bash
# git clone <repository_url>
# cd highlight_demos
```

### 2. Backend Setup (Python FastAPI with PDM)

   a.  **Install PDM (if you haven't already):**
       Follow the official PDM installation guide: <mcurl name="PDM Installation" url="https://pdm-project.org/latest/installation/"></mcurl>

   b.  **Install Python dependencies using PDM:**
       Navigate to the project root directory (`/Users/antonioreid/CODE/03_REFS_AND_ARTIFACTS/highlight_demos`) where `pyproject.toml` is located.
       ```bash
       pdm install
       ```
       This command will read the `pyproject.toml` file, resolve dependencies (including `ollama`), and install them into a PDM-managed environment.

   c.  **Setup Ollama and Pull Model:**
       1.  **Install Ollama:** If you haven't already, download and install Ollama from <mcurl name="Ollama official website" url="https://ollama.com"></mcurl>.
       2.  **Run Ollama:** Ensure the Ollama application/service is running.
       3.  **Pull the LLM:** The backend API defaults to using `gemma3:latest`. Pull this model (or your preferred alternative) using the Ollama CLI:
           ```bash
           ollama pull gemma3:latest
           ```
           You can change the model used by the API by setting the `OLLAMA_MODEL_NAME` environment variable or by modifying its default value in `src/highlight_demos/api.py`.
           ```python
           # In src/highlight_demos/api.py:
           OLLAMA_MODEL_NAME = os.environ.get("OLLAMA_MODEL_NAME", "gemma3:latest")
           ```
       The `nlp_system.py` file has been simplified, and direct Hugging Face model loading, quantization, and PEFT/LoRA logic have been removed from it, as these aspects are now handled by the Ollama server and the `ollama` Python client in `api.py`.

### 3. Frontend Setup (React App)

   a.  **Navigate to the frontend source directory if your `package.json` is there. If `package.json` is in the root, run these from the root.**
       Assuming `package.json` will be in the root `highlight_demos` directory:

   b.  **Install Node.js dependencies:**

       ```bash
       npm install
       # or
       # yarn install
       ```
       *(Note: `package.json` will be generated in a later step.)*

   c.  **(Optional) Create a `.env` file for API URL:**
       If your FastAPI API runs on a different port or host, create a `.env` file in the root `highlight_demos` directory:
       ```
       REACT_APP_API_URL=http://localhost:5001
       ```

## Running the Application

### 1. Start the Backend (FastAPI)

   Open a terminal, navigate to the project root (`/Users/antonioreid/CODE/03_REFS_AND_ARTIFACTS/highlight_demos/`). If you installed dependencies with `pdm install`, PDM provides ways to run scripts or commands within its managed environment.

   The `api.py` file is set up to run with Uvicorn when executed directly. You can run the API using PDM:

   ```bash
   pdm run python src/highlight_demos/api.py
   ```

   Alternatively, you can activate the PDM environment shell first and then run the script:
   ```bash
   pdm shell
   # Now you are in the PDM managed environment
   python src/highlight_demos/api.py
   ```

   Or, more commonly for FastAPI applications, you can run it with Uvicorn directly, specifying the application instance:
   ```bash
   pdm run uvicorn src.highlight_demos.api:app --reload --port 5001
   ```
   (Make sure your current working directory is the project root `/Users/antonioreid/CODE/03_REFS_AND_ARTIFACTS/highlight_demos` when running the uvicorn command, so that `src.highlight_demos.api:app` resolves correctly.)


   The API will typically start on `http://localhost:5001`.
   It will attempt to connect to your local Ollama instance (default `http://localhost:11434`). Ensure Ollama is running and the specified model (e.g., `gemma3:latest`) has been pulled.

### 2. Start the Frontend (React App)

   Open another terminal, navigate to the root project directory (`/Users/antonioreid/CODE/03_REFS_AND_ARTIFACTS/highlight_demos`), and run:

   ```bash
   npm start
   # or
   # yarn start
   ```

   This will open the application in your web browser, usually at `http://localhost:3000`.

## How to Use

1.  Ensure both the backend API and frontend application are running.
2.  Open the application in your browser (e.g., `http://localhost:3000`).
3.  Enter a piece of text into the text area.
4.  Click "Generate Knowledge Graph".
5.  The system will process the text using the NLP model, extract entities and relations, and then visualize them as an interactive 3D graph.
    *   **Interaction:**
        *   **Orbit:** Drag to rotate the view.
        *   **Zoom:** Scroll to zoom in/out.
        *   **Pan:** Right-click drag (or equivalent) to pan.
        *   **Node Click:** Click on a node to see its details in the side panel.
        *   **Node Hover:** Hover over a node to highlight it.

## Key Technologies

*   **Frontend:**
    *   React
    *   React Three Fiber (for Three.js integration)
    *   Drei (helpers for React Three Fiber)
    *   react-force-graph (for 3D force-directed graph layout)
*   **Backend:**
    *   FastAPI (Python web framework)
    *   Ollama (Python client library for Ollama)
    *   Ollama (The LLM serving application itself, running locally)
*   **Visualization:**
    *   Three.js

## Further Development Ideas

*   Implement fine-tuning capabilities for the NLP model through the UI.
*   Add more sophisticated node/edge styling and customization.
*   Improve error handling and user feedback.
*   Optimize performance for very large graphs.
*   Allow saving/loading of generated graphs.
*   Integrate different layout algorithms.
*   Add search and filtering functionality for the graph.
