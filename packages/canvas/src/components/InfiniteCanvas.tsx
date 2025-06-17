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
    <div className="w-full h-full flex" data-oid="2:oa5dm">
      <Toolbar
        mode={mode}
        onModeChange={handleModeChange}
        enableAI={enableAI}
        data-oid="4ceiohp"
      />

      <div className="flex-1 relative" data-oid="jt28qh.">
        {(mode === "archvision" || mode === "hybrid") && (
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onNodeClick={(_, node) => console.log("Selected node:", node)}
            fitView
            data-oid="b.k6i8t"
          >
            <Background data-oid=":mas.af" />
            <Controls data-oid="67quux2" />
            <Panel position="top-right" data-oid="30nih:2">
              <ViewSelector
                currentView={currentView}
                onViewChange={handleViewChange}
                data-oid="ggw6d7m"
              />
            </Panel>
          </ReactFlow>
        )}

        {(mode === "braincraft" || mode === "hybrid") && (
          <div
            className="absolute top-0 right-0 w-1/3 h-full bg-white shadow-lg"
            data-oid="n0htr8j"
          >
            <DiagramPanel
              code={currentDiagram?.code || ""}
              type={currentDiagram?.type}
              isLoading={isGenerating}
              data-oid="3tjsm1y"
            />

            <ChatInterface
              onSendMessage={handleDiagramGenerate}
              isLoading={isGenerating}
              data-oid="fbl4e_8"
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default InfiniteCanvas;
