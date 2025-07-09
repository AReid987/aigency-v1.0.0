// 3D Knowledge Graph Visualization with React Three Fiber
'use client';

import React, { useRef, useState, useEffect, Suspense } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Html, Line } from '@react-three/drei';
import * as THREE from 'three';
import { useSpring, animated } from '@react-spring/three';

// Types for the knowledge graph
export interface GraphNode {
  id: string;
  label: string;
  type: 'concept' | 'entity' | 'document' | 'agent' | 'user';
  position: [number, number, number];
  importance?: number;
  description?: string;
  properties?: Record<string, any>;
  connections?: string[];
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  type: 'contains' | 'related' | 'created' | 'uses';
  weight?: number;
  label?: string;
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

// Node component representing entities in the knowledge graph
function Node({
  node,
  onSelect,
  isSelected,
  connectionCount
}: {
  node: GraphNode;
  onSelect: () => void;
  isSelected: boolean;
  connectionCount: number;
}) {
  const meshRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);

  // Animation for hover and selection effects
  const { scale, emissive } = useSpring({
    scale: hovered || isSelected ? 1.2 : 1,
    emissive: hovered ? '#666' : isSelected ? '#00f' : '#000',
    config: { tension: 300, friction: 10 }
  });

  // Subtle floating animation
  useFrame((state) => {
    if (meshRef.current && !isSelected) {
      meshRef.current.position.y += Math.sin(state.clock.elapsedTime * 0.5 + node.position[0]) * 0.001;
    }
  });

  const color = getNodeColor(node.type);
  const size = getNodeSize(node.importance || 1);

  return (
    <group position={node.position}>
      <animated.mesh
        ref={meshRef}
        scale={scale}
        onClick={() => onSelect()}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        <sphereGeometry args={[size, 32, 32]} />
        <animated.meshStandardMaterial color={color} emissive={emissive} />
      </animated.mesh>

      <Html
        position={[0, size + 0.3, 0]}
        center
        style={{
          opacity: hovered || isSelected ? 1 : 0.7,
          transition: 'opacity 0.2s',
          background: 'rgba(0,0,0,0.5)',
          padding: '2px 5px',
          borderRadius: '3px',
          color: 'white',
          fontSize: '10px',
          pointerEvents: 'none',
          whiteSpace: 'nowrap'
        }}
      >
        {node.label}
      </Html>

      {/* Connection indicator */}
      {connectionCount > 0 && (
        <Html
          position={[size + 0.2, 0, 0]}
          center
          style={{
            opacity: 0.8,
            background: 'rgba(255,255,255,0.8)',
            padding: '1px 3px',
            borderRadius: '50%',
            color: 'black',
            fontSize: '8px',
            pointerEvents: 'none'
          }}
        >
          {connectionCount}
        </Html>
      )}
    </group>
  );
}

// Edge component representing relationships between nodes
function Edge({
  edge,
  startPosition,
  endPosition
}: {
  edge: GraphEdge;
  startPosition: [number, number, number];
  endPosition: [number, number, number];
}) {
  const points = [
    new THREE.Vector3(...startPosition),
    new THREE.Vector3(...endPosition)
  ];

  const color = getEdgeColor(edge.type);
  const thickness = getEdgeThickness(edge.weight || 1);

  return (
    <Line
      points={points}
      color={color}
      lineWidth={thickness}
      opacity={0.6}
      transparent
    />
  );
}

// Detail panel that appears when a node is selected
function DetailPanel({
  node,
  onClose
}: {
  node: GraphNode | null;
  onClose: () => void;
}) {
  if (!node) return null;

  return (
    <div
      style={{
        position: 'absolute',
        bottom: '20px',
        right: '20px',
        width: '300px',
        padding: '15px',
        backgroundColor: 'rgba(0,0,0,0.9)',
        color: 'white',
        borderRadius: '8px',
        zIndex: 100,
        border: '1px solid rgba(255,255,255,0.2)',
        backdropFilter: 'blur(10px)'
      }}
    >
      <h3 style={{ margin: '0 0 10px 0', color: getNodeColor(node.type) }}>
        {node.label}
      </h3>
      <p><strong>Type:</strong> {node.type}</p>
      <p><strong>Connections:</strong> {node.connections?.length || 0}</p>
      {node.description && <p><strong>Description:</strong> {node.description}</p>}

      {node.properties && (
        <div style={{ marginTop: '10px' }}>
          <strong>Properties:</strong>
          <div style={{ marginLeft: '10px', fontSize: '12px' }}>
            {Object.entries(node.properties).map(([key, value]) => (
              <div key={key} style={{ margin: '2px 0' }}>
                <strong>{key}:</strong> {String(value)}
              </div>
            ))}
          </div>
        </div>
      )}

      <button
        onClick={onClose}
        style={{
          background: '#3498db',
          border: 'none',
          padding: '8px 15px',
          marginTop: '15px',
          color: 'white',
          cursor: 'pointer',
          borderRadius: '4px',
          fontSize: '12px'
        }}
      >
        Close
      </button>
    </div>
  );
}

// Controls panel
function ControlsPanel({
  nodes,
  edges,
  onResetView,
  onLayoutChange,
  currentLayout
}: {
  nodes: GraphNode[];
  edges: GraphEdge[];
  onResetView: () => void;
  onLayoutChange: (layout: string) => void;
  currentLayout: string;
}) {
  return (
    <div
      style={{
        position: 'absolute',
        top: '20px',
        left: '20px',
        padding: '15px',
        backgroundColor: 'rgba(0,0,0,0.8)',
        color: 'white',
        borderRadius: '8px',
        border: '1px solid rgba(255,255,255,0.2)',
        backdropFilter: 'blur(10px)',
        minWidth: '200px'
      }}
    >
      <h3 style={{ margin: '0 0 15px 0' }}>3D Knowledge Graph</h3>

      <div style={{ marginBottom: '10px' }}>
        <div>Nodes: {nodes.length}</div>
        <div>Connections: {edges.length}</div>
      </div>

      <div style={{ marginBottom: '15px' }}>
        <label style={{ display: 'block', marginBottom: '5px', fontSize: '12px' }}>
          Layout:
        </label>
        <select
          value={currentLayout}
          onChange={(e) => onLayoutChange(e.target.value)}
          style={{
            background: 'rgba(255,255,255,0.1)',
            border: '1px solid rgba(255,255,255,0.3)',
            color: 'white',
            padding: '5px',
            borderRadius: '4px',
            width: '100%'
          }}
        >
          <option value="sphere">Sphere</option>
          <option value="cube">Cube</option>
          <option value="random">Random</option>
          <option value="force">Force-Directed</option>
        </select>
      </div>

      <button
        onClick={onResetView}
        style={{
          background: '#3498db',
          border: 'none',
          padding: '8px 15px',
          color: 'white',
          cursor: 'pointer',
          borderRadius: '4px',
          width: '100%',
          fontSize: '12px'
        }}
      >
        Reset View
      </button>
    </div>
  );
}

// Legend component
function Legend() {
  const nodeTypes = [
    { type: 'concept', label: 'Concept', color: '#e74c3c' },
    { type: 'entity', label: 'Entity', color: '#3498db' },
    { type: 'document', label: 'Document', color: '#2ecc71' },
    { type: 'agent', label: 'Agent', color: '#9b59b6' },
    { type: 'user', label: 'User', color: '#f39c12' }
  ];

  const edgeTypes = [
    { type: 'contains', label: 'Contains', color: '#3498db' },
    { type: 'related', label: 'Related', color: '#95a5a6' },
    { type: 'created', label: 'Created', color: '#2ecc71' },
    { type: 'uses', label: 'Uses', color: '#e74c3c' }
  ];

  return (
    <div
      style={{
        position: 'absolute',
        top: '20px',
        right: '20px',
        padding: '15px',
        backgroundColor: 'rgba(0,0,0,0.8)',
        color: 'white',
        borderRadius: '8px',
        border: '1px solid rgba(255,255,255,0.2)',
        backdropFilter: 'blur(10px)',
        fontSize: '12px'
      }}
    >
      <h4 style={{ margin: '0 0 10px 0' }}>Legend</h4>

      <div style={{ marginBottom: '15px' }}>
        <strong>Node Types:</strong>
        {nodeTypes.map(({ type, label, color }) => (
          <div key={type} style={{ display: 'flex', alignItems: 'center', margin: '5px 0' }}>
            <div
              style={{
                width: '12px',
                height: '12px',
                borderRadius: '50%',
                backgroundColor: color,
                marginRight: '8px'
              }}
            />
            {label}
          </div>
        ))}
      </div>

      <div>
        <strong>Edge Types:</strong>
        {edgeTypes.map(({ type, label, color }) => (
          <div key={type} style={{ display: 'flex', alignItems: 'center', margin: '5px 0' }}>
            <div
              style={{
                width: '20px',
                height: '2px',
                backgroundColor: color,
                marginRight: '8px'
              }}
            />
            {label}
          </div>
        ))}
      </div>
    </div>
  );
}

// Helper functions for visual properties
const getNodeColor = (type: string) => {
  const colorMap: Record<string, string> = {
    'concept': '#e74c3c',
    'entity': '#3498db',
    'document': '#2ecc71',
    'agent': '#9b59b6',
    'user': '#f39c12'
  };
  return colorMap[type] || '#95a5a6';
};

const getNodeSize = (importance: number) => {
  return 0.3 + (importance * 0.2);
};

const getEdgeColor = (type: string) => {
  const colorMap: Record<string, string> = {
    'contains': '#3498db',
    'related': '#95a5a6',
    'created': '#2ecc71',
    'uses': '#e74c3c'
  };
  return colorMap[type] || '#bdc3c7';
};

const getEdgeThickness = (weight: number) => {
  return 1 + (weight * 2);
};

// Layout algorithms
const generateLayout = (nodes: GraphNode[], layout: string): GraphNode[] => {
  const radius = 8;

  return nodes.map((node, index) => {
    let position: [number, number, number];

    switch (layout) {
      case 'sphere':
        const phi = Math.acos(-1 + (2 * index) / nodes.length);
        const theta = Math.sqrt(nodes.length * Math.PI) * phi;
        position = [
          radius * Math.cos(theta) * Math.sin(phi),
          radius * Math.sin(theta) * Math.sin(phi),
          radius * Math.cos(phi)
        ];
        break;

      case 'cube':
        const size = Math.ceil(Math.cbrt(nodes.length));
        const x = (index % size) - size / 2;
        const y = Math.floor(index / size) % size - size / 2;
        const z = Math.floor(index / (size * size)) - size / 2;
        position = [x * 2, y * 2, z * 2];
        break;

      case 'random':
        position = [
          (Math.random() - 0.5) * radius * 2,
          (Math.random() - 0.5) * radius * 2,
          (Math.random() - 0.5) * radius * 2
        ];
        break;

      case 'force':
      default:
        // Simple force-directed layout
        const angle = (index / nodes.length) * Math.PI * 2;
        const layer = Math.floor(index / 8);
        const layerRadius = radius * (0.5 + layer * 0.3);
        position = [
          layerRadius * Math.cos(angle),
          (Math.random() - 0.5) * 4,
          layerRadius * Math.sin(angle)
        ];
        break;
    }

    return { ...node, position };
  });
};

// Main knowledge graph component
export default function KnowledgeGraph3D({ data }: { data: GraphData }) {
  const [nodes, setNodes] = useState<GraphNode[]>([]);
  const [edges, setEdges] = useState<GraphEdge[]>([]);
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [cameraTarget, setCameraTarget] = useState<[number, number, number]>([0, 0, 0]);
  const [layout, setLayout] = useState('sphere');

  // Process graph data when it changes
  useEffect(() => {
    if (!data) return;

    // Apply layout to nodes
    const layoutNodes = generateLayout(data.nodes, layout);
    setNodes(layoutNodes);
    setEdges(data.edges);
  }, [data, layout]);

  // Handle node selection
  const handleNodeSelect = (node: GraphNode) => {
    setSelectedNode(node);
    setCameraTarget(node.position);
  };

  // Handle layout change
  const handleLayoutChange = (newLayout: string) => {
    setLayout(newLayout);
  };

  // Reset view
  const handleResetView = () => {
    setSelectedNode(null);
    setCameraTarget([0, 0, 0]);
  };

  // Calculate connection count for each node
  const getConnectionCount = (nodeId: string) => {
    return edges.filter(edge => edge.source === nodeId || edge.target === nodeId).length;
  };

  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      <Canvas
        camera={{ position: [0, 0, 15], fov: 60 }}
        style={{ background: 'linear-gradient(to bottom, #1a1a2e, #16213e)' }}
      >
        <Suspense fallback={null}>
          <ambientLight intensity={0.5} />
          <pointLight position={[10, 10, 10]} intensity={1} />
          <pointLight position={[-10, -10, -10]} intensity={0.5} />

          {/* Render edges */}
          {edges.map((edge) => {
            const startNode = nodes.find(node => node.id === edge.source);
            const endNode = nodes.find(node => node.id === edge.target);

            if (!startNode || !endNode) return null;

            return (
              <Edge
                key={edge.id}
                edge={edge}
                startPosition={startNode.position}
                endPosition={endNode.position}
              />
            );
          })}

          {/* Render nodes */}
          {nodes.map((node) => (
            <Node
              key={node.id}
              node={node}
              onSelect={() => handleNodeSelect(node)}
              isSelected={selectedNode?.id === node.id}
              connectionCount={getConnectionCount(node.id)}
            />
          ))}

          {/* Camera controls */}
          <OrbitControls
            enableDamping
            dampingFactor={0.1}
            rotateSpeed={0.5}
            target={new THREE.Vector3(...cameraTarget)}
            maxDistance={50}
            minDistance={5}
          />

          {/* Fog for depth effect */}
          <fog attach="fog" args={['#16213e', 10, 50]} />
        </Suspense>
      </Canvas>

      {/* UI Overlays */}
      <ControlsPanel
        nodes={nodes}
        edges={edges}
        onResetView={handleResetView}
        onLayoutChange={handleLayoutChange}
        currentLayout={layout}
      />

      <Legend />

      <DetailPanel
        node={selectedNode}
        onClose={() => setSelectedNode(null)}
      />
    </div>
  );
}
