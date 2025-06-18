import React, { useEffect, useRef, useState } from "react";
import mermaid from "mermaid";
import { DiagramType } from "../../types";

interface DiagramPanelProps {
  code: string;
  type?: DiagramType;
  isLoading?: boolean;
}

export const DiagramPanel: React.FC<DiagramPanelProps> = ({
  code,
  type = "flowchart",
  isLoading = false,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [error, setError] = useState<string | null>(null);
  const [diagramId] = useState(
    () => `mermaid-${Math.random().toString(36).substr(2, 9)}`,
  );

  useEffect(() => {
    const renderDiagram = async () => {
      if (!code || !containerRef.current) {
        return;
      }

      try {
        setError(null);

        // Clean the code
        const cleanCode = code.replace(/```mermaid|```/g, "").trim();

        // Clear container
        containerRef.current.innerHTML = "";

        // Create diagram element
        const diagramElement = document.createElement("div");
        diagramElement.id = diagramId;
        diagramElement.className = "mermaid";
        diagramElement.textContent = cleanCode;

        containerRef.current.appendChild(diagramElement);

        // Render with mermaid
        await mermaid.run({
          querySelector: `#${diagramId}`,
        });
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : "Failed to render diagram";
        setError(errorMessage);
        if (containerRef.current) {
          containerRef.current.innerHTML = `<div class="error">Error: ${errorMessage}</div>`;
        }
      }
    };

    renderDiagram();
  }, [code, diagramId]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64" data-oid="-khgins">
        <div className="text-gray-500" data-oid="d_v9aae">
          Generating diagram...
        </div>
      </div>
    );
  }

  return (
    <div className="w-full h-full" data-oid="fpnie7r">
      <div className="p-4 border-b" data-oid="_7rc8.:">
        <h3 className="text-lg font-semibold" data-oid="o_3li.l">
          {type.charAt(0).toUpperCase() + type.slice(1)} Diagram
        </h3>
      </div>

      <div className="p-4" data-oid="biso34b">
        {error ? (
          <div
            className="text-red-500 p-4 border border-red-200 rounded"
            data-oid="sdzeben"
          >
            Error: {error}
          </div>
        ) : (
          <div
            ref={containerRef}
            className="w-full min-h-64 flex items-center justify-center"
            data-oid="whb8m8z"
          />
        )}
      </div>
    </div>
  );
};

export default DiagramPanel;
