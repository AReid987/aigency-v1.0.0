
import React, { useState, useCallback, useEffect } from 'react';
import { useNodesState, useEdgesState, addEdge, Node, Edge, OnConnect, Connection, XYPosition, MarkerType } from '@xyflow/react';
import NodeGraph from './components/NodeGraph';
import ChatBox from './components/ChatBox';
import type { CustomNode, ArtifactNodeData } from './types';
import { ARTIFACT_GENERATED_TAG_PREFIX, ARTIFACT_RELATIONSHIP_TAG_PREFIX } from './constants';
import DocumentTextIcon from './components/icons/DocumentTextIcon'; // A default icon

const nodeIcons: { [key: string]: React.FC<{className?: string}> } = {
  default: DocumentTextIcon,
  LeanCanvas: DocumentTextIcon, // Replace with specific icons if available
  MarketResearch: DocumentTextIcon,
  UserProfile: DocumentTextIcon,
  ICP: DocumentTextIcon,
  Roadmap: DocumentTextIcon,
  SWOTAnalysis: DocumentTextIcon,
  WelcomeMessage: DocumentTextIcon, // Added for consistency
};

const WelcomeIcon = nodeIcons.WelcomeMessage || nodeIcons.default;

const initialNodes: CustomNode[] = [
  {
    id: 'initial-guide-node',
    type: 'artifactNode', // Use our custom node type
    position: { x: 150, y: 150 }, // Positioned to be visible on load
    data: {
      label: "Founder's Insight Weaver",
      type: 'WelcomeMessage',
      contentSummary: "Welcome! I'm Insight Weaver. Let's chat about your startup ideas and visualize them here. Ask me anything to get started!",
      icon: <WelcomeIcon className="w-5 h-5 mr-2 text-pink-400" />
    },
  },
];

const initialEdges: Edge[] = [];


function App() {
  // Fix: useNodesState generic should be the full Node type (CustomNode), not just the data type (ArtifactNodeData).
  const [nodes, setNodes, onNodesChange] = useNodesState<CustomNode>(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [nodeIdCounter, setNodeIdCounter] = useState(initialNodes.length > 0 ? initialNodes.length : 1); // Start counter after initial nodes

  const onConnect: OnConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge({...params, animated: true, style: {stroke: '#f472b6'}}, eds)),
    [setEdges]
  );

  const getArtifactNames = (): {name: string, type: string}[] => {
    return nodes.map(node => ({name: node.data?.label || `Node ${node.id}`, type: node.data?.type || 'Unknown'}));
  };

  const handleNewArtifact = useCallback((type: string, name: string, summary: string, fullContent: string) => {
    
    const existingNode = nodes.find(n => n.data?.label === name);
    if (existingNode) {
      console.warn(`Artifact with name "${name}" already exists. Updating existing node.`);
      setNodes((nds) =>
        nds.map((node) =>
          node.id === existingNode.id
            ? { ...node, data: { ...node.data!, contentSummary: summary, fullContent: fullContent, type: type, icon: node.data?.icon || <DocumentTextIcon className="w-5 h-5 mr-2 text-pink-400" /> } } // ensure icon is preserved or re-added
            : node
        )
      );
      return;
    }
    
    setNodeIdCounter(prev => prev + 1);
    const newNodeId = `artifact_${name.replace(/\s+/g, '_')}_${nodeIdCounter}`;
    const IconComponent = nodeIcons[type] || nodeIcons.default;

    const newNode: CustomNode = {
      id: newNodeId,
      type: 'artifactNode', // Custom node type
      position: { // Calculate position to avoid overlap, simple logic for now
        x: (nodes.length % 5) * 280 + 50,
        y: Math.floor(nodes.length / 5) * 180 + 50,
      },
      data: { 
        label: name, 
        type: type,
        contentSummary: summary,
        fullContent: fullContent,
        icon: <IconComponent className="w-5 h-5 mr-2 text-pink-400" />
      },
    };
    setNodes((nds) => nds.concat(newNode));
  }, [nodes, setNodes, nodeIdCounter]);

  const handleNewRelationship = useCallback((sourceName: string, targetName: string, label: string) => {
    const sourceNode = nodes.find(n => n.data?.label === sourceName);
    const targetNode = nodes.find(n => n.data?.label === targetName);

    if (sourceNode && targetNode) {
      const newEdge: Edge = {
        id: `edge_${sourceNode.id}-${targetNode.id}_${label.replace(/\s+/g, '_')}_${Date.now()}`, // Ensure unique edge ID
        source: sourceNode.id,
        target: targetNode.id,
        label: label,
        animated: true,
        markerEnd: {
          type: MarkerType.ArrowClosed,
          color: '#f472b6',
        },
        style: { stroke: '#f472b6', strokeWidth: 1.5 },
      };
      setEdges((eds) => addEdge(newEdge, eds));
    } else {
      console.warn(`Could not create relationship: Source "${sourceName}" or Target "${targetName}" node not found.`);
    }
  }, [nodes, setEdges]);
  

  return (
    <div className="w-screen h-screen flex flex-col bg-slate-900">
      <NodeGraph
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
      />
      <ChatBox 
        onNewArtifact={handleNewArtifact} 
        onNewRelationship={handleNewRelationship}
        currentArtifactNames={getArtifactNames()}
      />
    </div>
  );
}

export default App;