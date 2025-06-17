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
      <div className="flex items-center justify-center h-64" data-oid="1l0xwtc">
        <div className="text-gray-500" data-oid="i6t.qib">
          Generating diagram...
        </div>
      </div>
    );
  }

  return (
    <div className="w-full h-full" data-oid="gyu42rb">
      <div className="p-4 border-b" data-oid="3hczgef">
        <h3 className="text-lg font-semibold" data-oid="hrmqec1">
          {type.charAt(0).toUpperCase() + type.slice(1)} Diagram
        </h3>
      </div>

      <div className="p-4" data-oid="yw5f9i9">
        {error ? (
          <div
            className="text-red-500 p-4 border border-red-200 rounded"
            data-oid="7qqrp_6"
          >
            Error: {error}
          </div>
        ) : (
          <div
            ref={containerRef}
            className="w-full min-h-64 flex items-center justify-center"
            data-oid="3xc56br"
          />
        )}
      </div>
    </div>
  );
};

export default DiagramPanel;
