import React, { useCallback, useEffect } from "react";
import ReactFlow, {
  Background,
  Controls,
  Panel,
  useNodesState,
  useEdgesState,
  addEdge,
  Connection,
  Edge,
} from "reactflow";
import { useCanvas } from "../hooks/useCanvas";
import { useDiagram } from "../hooks/useDiagram";
import { ViewSelector } from "./ViewSelector";
import { Toolbar } from "./Toolbar";
import { DiagramPanel } from "./diagram/DiagramPanel";
import { ChatInterface } from "./diagram/ChatInterface";
import { CanvasMode, ViewType } from "../types";
import "reactflow/dist/style.css";

interface InfiniteCanvasProps {
  mode?: CanvasMode;
  defaultView?: ViewType;
  enableAI?: boolean;
  enableCollaboration?: boolean;
  onViewChange?: (view: ViewType) => void;
  onModeChange?: (mode: CanvasMode) => void;
}

export const InfiniteCanvas: React.FC<InfiniteCanvasProps> = ({
  mode = "archvision",
  defaultView = "2d",
  enableAI = true,
  enableCollaboration = true,
  onViewChange,
  onModeChange,
}) => {
  const { currentView, setView, setMode } = useCanvas();

  const { currentDiagram, generateDiagram, updateDiagram, isGenerating } =
    useDiagram();

  // Use ReactFlow's built-in state management
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  useEffect(() => {
    setView(defaultView);
    setMode(mode);
  }, [defaultView, mode, setView, setMode]);

  const handleViewChange = useCallback(
    (newView: ViewType) => {
      setView(newView);
      onViewChange?.(newView);
    },
    [setView, onViewChange],
  );

  const handleModeChange = useCallback(
    (newMode: CanvasMode) => {
      setMode(newMode);
      onModeChange?.(newMode);
    },
    [setMode, onModeChange],
  );

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges],
  );

  const handleDiagramGenerate = useCallback(
    async (prompt: string) => {
      try {
        const diagram = await generateDiagram(prompt);
        if (diagram) {
          // Convert diagram to nodes/edges if in hybrid mode
          if (mode === "hybrid") {
            // TODO: Implement diagram to nodes/edges conversion
          }
        }
      } catch (error) {
        console.error("Failed to generate diagram:", error);
      }
    },
    [generateDiagram, mode],
  );

  return (
    <div className="w-full h-full flex" data-oid="vlj4pvj">
      <Toolbar
        mode={mode}
        onModeChange={handleModeChange}
        enableAI={enableAI}
        data-oid="8cqgyrf"
      />

      <div className="flex-1 relative" data-oid="32aywk:">
        {(mode === "archvision" || mode === "hybrid") && (
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onNodeClick={(_, node) => console.log("Selected node:", node)}
            fitView
            data-oid="jx4c97j"
          >
            <Background data-oid="9vx0:ah" />
            <Controls data-oid="p_1ahpw" />
            <Panel position="top-right" data-oid="7kjqrgs">
              <ViewSelector
                currentView={currentView}
                onViewChange={handleViewChange}
                data-oid="n2l3q3p"
              />
            </Panel>
          </ReactFlow>
        )}

        {(mode === "braincraft" || mode === "hybrid") && (
          <div
            className="absolute top-0 right-0 w-1/3 h-full bg-white shadow-lg"
            data-oid="bo8zn4g"
          >
            <DiagramPanel
              code={currentDiagram?.code || ""}
              type={currentDiagram?.type}
              isLoading={isGenerating}
              data-oid="xbx0-hc"
            />

            <ChatInterface
              onSendMessage={handleDiagramGenerate}
              isLoading={isGenerating}
              data-oid="s1sya8b"
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default InfiniteCanvas;
