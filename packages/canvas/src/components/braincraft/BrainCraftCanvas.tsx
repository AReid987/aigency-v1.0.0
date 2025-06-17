import React, { useState, useCallback } from "react";
import { DiagramPanel } from "../diagram/DiagramPanel";
import { ChatInterface } from "../diagram/ChatInterface";
import { useDiagram } from "../../hooks/useDiagram";
import { DiagramType, ChatMessage } from "../../types";

interface BrainCraftCanvasProps {
  initialDiagramType?: DiagramType;
  onDiagramGenerate?: (code: string, type: DiagramType) => void;
  onDiagramUpdate?: (code: string, type: DiagramType) => void;
}

export const BrainCraftCanvas: React.FC<BrainCraftCanvasProps> = ({
  initialDiagramType = "flowchart",
  onDiagramGenerate,
  onDiagramUpdate,
}) => {
  const {
    currentDiagram,
    messages,
    isGenerating,
    generateDiagram,
    updateDiagram,
    addMessage,
    clearMessages,
  } = useDiagram();

  const [selectedType, setSelectedType] =
    useState<DiagramType>(initialDiagramType);

  const handleSendMessage = useCallback(
    async (content: string) => {
      try {
        // Add user message
        addMessage({
          content,
          sender: "user",
        });

        // Generate diagram
        const diagram = await generateDiagram(content, selectedType);

        // Add assistant message with diagram
        addMessage({
          content: "Here's your diagram:",
          sender: "assistant",
          diagramCode: diagram.code,
        });

        // Notify parent
        onDiagramGenerate?.(diagram.code, diagram.type);
      } catch (error) {
        addMessage({
          content: `Error: ${error instanceof Error ? error.message : "Failed to generate diagram"}`,
          sender: "assistant",
        });
      }
    },
    [selectedType, generateDiagram, addMessage, onDiagramGenerate],
  );

  const diagramTypes: { label: string; value: DiagramType }[] = [
    { label: "Flowchart", value: "flowchart" },
    { label: "Sequence", value: "sequence" },
    { label: "Class", value: "class" },
    { label: "State", value: "state" },
    { label: "ER", value: "er" },
    { label: "Gantt", value: "gantt" },
    { label: "Pie", value: "pie" },
    { label: "Mindmap", value: "mindmap" },
  ];

  return (
    <div className="flex h-full" data-oid="na42.xl">
      {/* Main Diagram Area */}
      <div className="flex-1 flex flex-col" data-oid="9ai0.4t">
        {/* Diagram Type Selector */}
        <div className="bg-white border-b p-4" data-oid="ji3wuzg">
          <div className="flex items-center gap-4" data-oid="m.lk1:h">
            <label className="text-sm font-medium" data-oid="fz5nf_z">
              Diagram Type:
            </label>
            <select
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value as DiagramType)}
              className="px-3 py-1 border rounded text-sm"
              data-oid="wwr8z:s"
            >
              {diagramTypes.map(({ label, value }) => (
                <option key={value} value={value} data-oid="vxow0q4">
                  {label}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Diagram Display */}
        <div className="flex-1 overflow-auto" data-oid="yoormlo">
          <DiagramPanel
            code={currentDiagram?.code || ""}
            type={currentDiagram?.type || selectedType}
            isLoading={isGenerating}
            data-oid="ivg5og2"
          />
        </div>
      </div>

      {/* Chat Interface */}
      <div className="w-96 border-l flex flex-col" data-oid="xthqogs">
        <div className="bg-white border-b p-4" data-oid="lm2336r">
          <h3 className="font-semibold" data-oid="jijmx6v">
            AI Assistant
          </h3>
          <p className="text-sm text-gray-600" data-oid=":5piygz">
            Describe the diagram you want to create
          </p>
        </div>

        <div className="flex-1" data-oid="qa0jqwb">
          <ChatInterface
            onSendMessage={handleSendMessage}
            isLoading={isGenerating}
            messages={messages}
            data-oid="q.iijj-"
          />
        </div>
      </div>
    </div>
  );
};

export default BrainCraftCanvas;
