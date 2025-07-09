'use client';

import React, { useState, useEffect } from 'react';
import type { GraphData, GraphNode, GraphEdge } from './knowledge-graph-3d';

// Simple 2D fallback for the knowledge graph
export default function KnowledgeGraphFallback({ data }: { data: GraphData }) {
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [layout, setLayout] = useState('grid');

  if (!data) {
    return (
      <div className="flex items-center justify-center h-full">
        <p className="text-gray-600 dark:text-gray-300">No data available</p>
      </div>
    );
  }

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

  const getConnectionCount = (nodeId: string) => {
    return data.edges.filter(edge => edge.source === nodeId || edge.target === nodeId).length;
  };

  return (
    <div className="w-full h-full relative bg-gradient-to-br from-gray-900 to-gray-800 rounded-lg overflow-hidden">
      {/* Controls */}
      <div className="absolute top-4 left-4 bg-black/80 text-white p-4 rounded-lg backdrop-blur-sm z-10">
        <h3 className="text-lg font-bold mb-3">Knowledge Graph (2D View)</h3>
        <div className="mb-3">
          <div className="text-sm">Nodes: {data.nodes.length}</div>
          <div className="text-sm">Connections: {data.edges.length}</div>
        </div>
        <div className="mb-3">
          <label className="block text-xs mb-1">Layout:</label>
          <select
            value={layout}
            onChange={(e) => setLayout(e.target.value)}
            className="bg-gray-700 text-white text-xs p-1 rounded"
          >
            <option value="grid">Grid</option>
            <option value="circle">Circle</option>
            <option value="random">Random</option>
          </select>
        </div>
        <button
          onClick={() => setSelectedNode(null)}
          className="bg-blue-500 hover:bg-blue-600 text-white text-xs px-3 py-1 rounded"
        >
          Reset View
        </button>
      </div>

      {/* Legend */}
      <div className="absolute top-4 right-4 bg-black/80 text-white p-4 rounded-lg backdrop-blur-sm z-10">
        <h4 className="text-sm font-bold mb-2">Legend</h4>
        <div className="space-y-1 text-xs">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <span>Concepts</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-blue-500"></div>
            <span>Entities</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
            <span>Documents</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-purple-500"></div>
            <span>Agents</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-orange-500"></div>
            <span>Users</span>
          </div>
        </div>
      </div>

      {/* Graph Visualization */}
      <div className="w-full h-full p-20">
        <svg className="w-full h-full">
          {/* Render edges */}
          {data.edges.map((edge, index) => {
            const sourceNode = data.nodes.find(n => n.id === edge.source);
            const targetNode = data.nodes.find(n => n.id === edge.target);
            
            if (!sourceNode || !targetNode) return null;

            // Calculate positions based on layout
            const getPosition = (node: GraphNode, index: number) => {
              const centerX = 400;
              const centerY = 300;
              
              switch (layout) {
                case 'circle':
                  const angle = (index / data.nodes.length) * 2 * Math.PI;
                  return {
                    x: centerX + Math.cos(angle) * 200,
                    y: centerY + Math.sin(angle) * 200
                  };
                case 'grid':
                  const cols = Math.ceil(Math.sqrt(data.nodes.length));
                  const row = Math.floor(index / cols);
                  const col = index % cols;
                  return {
                    x: 100 + col * 150,
                    y: 100 + row * 150
                  };
                default: // random
                  return {
                    x: 100 + (index * 123) % 600,
                    y: 100 + (index * 456) % 400
                  };
              }
            };

            const sourceIndex = data.nodes.findIndex(n => n.id === edge.source);
            const targetIndex = data.nodes.findIndex(n => n.id === edge.target);
            const sourcePos = getPosition(sourceNode, sourceIndex);
            const targetPos = getPosition(targetNode, targetIndex);

            return (
              <line
                key={edge.id}
                x1={sourcePos.x}
                y1={sourcePos.y}
                x2={targetPos.x}
                y2={targetPos.y}
                stroke="#666"
                strokeWidth="1"
                opacity="0.6"
              />
            );
          })}

          {/* Render nodes */}
          {data.nodes.map((node, index) => {
            const getPosition = (node: GraphNode, index: number) => {
              const centerX = 400;
              const centerY = 300;
              
              switch (layout) {
                case 'circle':
                  const angle = (index / data.nodes.length) * 2 * Math.PI;
                  return {
                    x: centerX + Math.cos(angle) * 200,
                    y: centerY + Math.sin(angle) * 200
                  };
                case 'grid':
                  const cols = Math.ceil(Math.sqrt(data.nodes.length));
                  const row = Math.floor(index / cols);
                  const col = index % cols;
                  return {
                    x: 100 + col * 150,
                    y: 100 + row * 150
                  };
                default: // random
                  return {
                    x: 100 + (index * 123) % 600,
                    y: 100 + (index * 456) % 400
                  };
              }
            };

            const position = getPosition(node, index);
            const isSelected = selectedNode?.id === node.id;
            const connectionCount = getConnectionCount(node.id);

            return (
              <g key={node.id}>
                <circle
                  cx={position.x}
                  cy={position.y}
                  r={isSelected ? 25 : 20}
                  fill={getNodeColor(node.type)}
                  stroke={isSelected ? '#fff' : 'none'}
                  strokeWidth="2"
                  className="cursor-pointer hover:opacity-80 transition-all"
                  onClick={() => setSelectedNode(node)}
                />
                <text
                  x={position.x}
                  y={position.y - 30}
                  textAnchor="middle"
                  className="fill-white text-xs font-medium pointer-events-none"
                >
                  {node.label}
                </text>
                {connectionCount > 0 && (
                  <circle
                    cx={position.x + 15}
                    cy={position.y - 15}
                    r="8"
                    fill="rgba(255,255,255,0.9)"
                    className="pointer-events-none"
                  />
                )}
                {connectionCount > 0 && (
                  <text
                    x={position.x + 15}
                    y={position.y - 11}
                    textAnchor="middle"
                    className="fill-black text-xs font-bold pointer-events-none"
                  >
                    {connectionCount}
                  </text>
                )}
              </g>
            );
          })}
        </svg>
      </div>

      {/* Detail Panel */}
      {selectedNode && (
        <div className="absolute bottom-4 right-4 bg-black/90 text-white p-4 rounded-lg backdrop-blur-sm max-w-sm z-10">
          <h3 className="text-lg font-bold mb-2" style={{ color: getNodeColor(selectedNode.type) }}>
            {selectedNode.label}
          </h3>
          <p className="text-sm mb-1"><strong>Type:</strong> {selectedNode.type}</p>
          <p className="text-sm mb-1"><strong>Connections:</strong> {getConnectionCount(selectedNode.id)}</p>
          {selectedNode.description && (
            <p className="text-sm mb-2"><strong>Description:</strong> {selectedNode.description}</p>
          )}
          {selectedNode.properties && (
            <div className="text-xs">
              <strong>Properties:</strong>
              <div className="ml-2 mt-1">
                {Object.entries(selectedNode.properties).map(([key, value]) => (
                  <div key={key} className="mb-1">
                    <strong>{key}:</strong> {String(value)}
                  </div>
                ))}
              </div>
            </div>
          )}
          <button
            onClick={() => setSelectedNode(null)}
            className="bg-blue-500 hover:bg-blue-600 text-white text-xs px-3 py-1 rounded mt-3"
          >
            Close
          </button>
        </div>
      )}

      {/* Fallback Notice */}
      <div className="absolute bottom-4 left-4 bg-yellow-500/20 text-yellow-200 p-2 rounded text-xs">
        ⚠️ 3D view unavailable - showing 2D fallback
      </div>
    </div>
  );
}
