import React, { useState, useCallback, useEffect } from 'react';
import KnowledgeGraph from './components/KnowledgeGraph'; // Adjusted path
import './App.css'; // Assuming you'll create an App.css for styling

function App() {
  const [inputText, setInputText] = useState('');
  const [graphData, setGraphData] = useState({ nodes: [], edges: [] });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [apiStatus, setApiStatus] = useState('Checking API status...');

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

  const checkApiHealth = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/health`);
      if (!response.ok) {
        throw new Error(`API health check failed: ${response.statusText}`);
      }
      const data = await response.json();
      setApiStatus(`API Status: ${data.status}, NLP System: ${data.nlp_system}`);
    } catch (err) {
      console.error("API health check error:", err);
      setApiStatus(`API Status: Error - ${err.message}. Ensure the Flask API is running.`);
      setError("Could not connect to the backend API. Please ensure it's running.");
    }
  }, [API_BASE_URL]);

  useEffect(() => {
    checkApiHealth();
  }, [checkApiHealth]);

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!inputText.trim()) {
      setError('Please enter some text to generate the graph.');
      return;
    }
    setIsLoading(true);
    setError(null);
    setGraphData({ nodes: [], edges: [] }); // Clear previous graph

    try {
      const response = await fetch(`${API_BASE_URL}/api/generate-graph`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: 'Failed to parse error response from server.' }));
        throw new Error(errorData.error || `Server error: ${response.statusText}`);
      }

      const data = await response.json();
      if (data.nodes && data.edges) {
        setGraphData(data);
      } else {
        // Handle cases where the structure is not as expected, or if there's a partial error from NLP
        console.warn("Received data from API is not in the expected graph format:", data);
        setError(data.error || "Received malformed graph data from the server.");
        setGraphData({ nodes: [], edges: [] }); // Ensure it's an empty graph
      }
    } catch (err) {
      console.error('Error generating graph:', err);
      setError(`Failed to generate graph: ${err.message}`);
      setGraphData({ nodes: [], edges: [] }); // Ensure it's an empty graph on error
    }
    setIsLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Interactive Knowledge Graph Generator</h1>
        <p className="api-status">{apiStatus}</p>
      </header>
      <main className="App-main">
        <form onSubmit={handleSubmit} className="input-form">
          <textarea
            value={inputText}
            onChange={handleInputChange}
            placeholder="Enter text to analyze and visualize as a knowledge graph..."
            rows={8}
            disabled={isLoading}
          />
          <button type="submit" disabled={isLoading}>
            {isLoading ? 'Generating Graph...' : 'Generate Knowledge Graph'}
          </button>
        </form>

        {error && <p className="error-message">Error: {error}</p>}

        <div className="graph-container">
          {isLoading && (
            <div className="loading-overlay">
              <p>Processing text and building graph. This may take a moment, especially for large inputs or complex models...</p>
              <div className="spinner"></div>
            </div>
          )}
          {(!isLoading && graphData.nodes.length === 0 && !error && !inputText) &&
            <p className="placeholder-text">Enter text above and click 'Generate' to see the graph.</p>
          }
          {(!isLoading && graphData.nodes.length === 0 && !error && inputText && !error) &&
             <p className="placeholder-text">Graph generated with no nodes. The NLP model might not have found entities/relations, or there was an issue processing.</p>
          }
          {(graphData.nodes.length > 0 || graphData.edges.length > 0) &&
            <KnowledgeGraph data={graphData} />
          }
        </div>
      </main>
      <footer className="App-footer">
        <p>Powered by React, Three.js, and a Python NLP backend.</p>
      </footer>
    </div>
  );
}

export default App;