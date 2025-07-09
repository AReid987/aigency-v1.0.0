
import React from 'react';
import { ReactFlow, Background, Controls, MiniMap, useNodesState, useEdgesState, BackgroundVariant } from '@xyflow/react';
import type { Node, Edge, OnConnect, OnEdgesChange, OnNodesChange } from '@xyflow/react';
import ArtifactNode from './ArtifactNode';

import '@xyflow/react/dist/style.css';

interface NodeGraphProps {
  initialNodes?: Node[];
  initialEdges?: Edge[];
  onNodesChange: OnNodesChange;
  onEdgesChange: OnEdgesChange;
  onConnect: OnConnect;
  nodes: Node[];
  edges: Edge[];
}

const nodeTypes = {
  artifactNode: ArtifactNode,
};

const NodeGraph: React.FC<NodeGraphProps> = ({ nodes, edges, onNodesChange, onEdgesChange, onConnect }) => {
  return (
    <div style={{ width: '100%', height: '100%' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        fitView
        className="bg-slate-900"
        attributionPosition="bottom-left"
      >
        <Controls className="text-white fill-white stroke-white" />
        <MiniMap nodeStrokeColor={(n) => {
          if (n.type === 'artifactNode') return '#f472b6'; // pink-400
          if (n.style?.background) return n.style.background as string;
          return '#52525b'; // slate-600
        }} nodeColor={(n) => {
          if (n.style?.background) return n.style.background as string;
          return '#334155'; // slate-700
        }} className="bg-slate-800 border border-slate-700" />
        <Background variant={BackgroundVariant.Dots} gap={16} size={1} color="#475569" />
      </ReactFlow>
    </div>
  );
};

export default NodeGraph;
