import React, { useCallback, useMemo } from "react";
import ReactFlow, {
  Background,
  Controls,
  Panel,
  Node,
  Edge,
  Connection,
  addEdge,
  useNodesState,
  useEdgesState,
} from "reactflow";
import { ViewType } from "../../types";
import { canvasService } from "../../services/canvasService";

interface ArchVisionCanvasProps {
  view: ViewType;
  onViewChange?: (view: ViewType) => void;
  initialNodes?: Node[];
  initialEdges?: Edge[];
}

const defaultNodes: Node[] = [
  {
    id: "1",
    type: "default",
    position: { x: 100, y: 100 },
    data: { label: "Frontend" },
  },
  {
    id: "2",
    type: "default",
    position: { x: 300, y: 100 },
    data: { label: "API Gateway" },
  },
  {
    id: "3",
    type: "default",
    position: { x: 500, y: 100 },
    data: { label: "Database" },
  },
];

const defaultEdges: Edge[] = [
  {
    id: "e1-2",
    source: "1",
    target: "2",
    type: "smoothstep",
  },
  {
    id: "e2-3",
    source: "2",
    target: "3",
    type: "smoothstep",
  },
];

export const ArchVisionCanvas: React.FC<ArchVisionCanvasProps> = ({
  view,
  onViewChange,
  initialNodes = defaultNodes,
  initialEdges = defaultEdges,
}) => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges],
  );

  // Transform nodes based on view type
  const transformedData = useMemo(() => {
    return canvasService.transformForView(
      nodes.map((node) => ({
        id: node.id,
        type: node.type || "default",
        position: node.position,
        data: node.data,
      })),
      edges.map((edge) => ({
        id: edge.id,
        source: edge.source,
        target: edge.target,
        type: edge.type,
        data: edge.data || {},
      })),
      view,
    );
  }, [nodes, edges, view]);

  // Convert back to ReactFlow format
  const reactFlowNodes = useMemo(() => {
    return transformedData.nodes.map((node) => ({
      ...node,
      style:
        view === "iso"
          ? {
              transform: "perspective(1000px) rotateX(30deg) rotateY(-30deg)",
              ...node.style,
            }
          : node.style,
    }));
  }, [transformedData.nodes, view]);

  const handleAutoLayout = useCallback(() => {
    const layoutedNodes = canvasService.autoLayout(
      transformedData.nodes,
      transformedData.edges,
      "hierarchical",
    );

    setNodes(
      layoutedNodes.map((node) => ({
        id: node.id,
        type: node.type,
        position: node.position,
        data: node.data,
      })),
    );
  }, [transformedData, setNodes]);

  return (
    <div className="w-full h-full relative" data-oid="fg_:1l0">
      <ReactFlow
        nodes={reactFlowNodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        fitView
        className={view === "3d" ? "perspective-canvas" : ""}
        data-oid="d83mof9"
      >
        <Background
          variant={view === "iso" ? "dots" : "lines"}
          gap={view === "iso" ? 20 : 12}
          data-oid="z.raln-"
        />

        <Controls data-oid="b5a3hvp" />

        <Panel position="top-left" data-oid="sc-enqw">
          <div className="bg-white p-2 rounded shadow" data-oid="fkjhk-4">
            <h3 className="font-semibold text-sm mb-2" data-oid="9_93i18">
              ArchVision Tools
            </h3>
            <div className="flex gap-2" data-oid="_shtjgm">
              <button
                onClick={handleAutoLayout}
                className="px-2 py-1 text-xs bg-blue-500 text-white rounded hover:bg-blue-600"
                data-oid="qpb4aqe"
              >
                Auto Layout
              </button>
              <button
                className="px-2 py-1 text-xs bg-gray-500 text-white rounded hover:bg-gray-600"
                onClick={() => {
                  const newNode = canvasService.createNode(
                    "default",
                    { x: Math.random() * 400, y: Math.random() * 400 },
                    { label: `Node ${nodes.length + 1}` },
                  );
                  setNodes((prev) => [
                    ...prev,
                    {
                      id: newNode.id,
                      type: newNode.type,
                      position: newNode.position,
                      data: newNode.data,
                    },
                  ]);
                }}
                data-oid="5.m61kh"
              >
                Add Node
              </button>
            </div>
          </div>
        </Panel>

        <Panel position="top-right" data-oid="rvt0vxh">
          <div className="bg-white p-2 rounded shadow" data-oid="5h:t81c">
            <div className="text-xs text-gray-600 mb-1" data-oid="f0rrfta">
              View: {view.toUpperCase()}
            </div>
            <div className="flex gap-1" data-oid="mq8:e_o">
              {(["2d", "3d", "iso"] as ViewType[]).map((v) => (
                <button
                  key={v}
                  onClick={() => onViewChange?.(v)}
                  className={`px-2 py-1 text-xs rounded ${
                    view === v
                      ? "bg-blue-500 text-white"
                      : "bg-gray-100 hover:bg-gray-200"
                  }`}
                  data-oid="kw0z28u"
                >
                  {v.toUpperCase()}
                </button>
              ))}
            </div>
          </div>
        </Panel>
      </ReactFlow>

      <style jsx data-oid="369l_bm">{`
        .perspective-canvas {
          transform-style: preserve-3d;
        }
      `}</style>
    </div>
  );
};

export default ArchVisionCanvas;
