"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import AgentNetworkGraph from "@/components/agent-network-graph";
import {
  generateAgentNetworkData,
  generateSimpleNetworkData,
  generateDynamicNetworkData,
  NetworkData,
  NetworkNode,
} from "@/lib/network-data";

export default function NetworkPage() {
  const [networkData, setNetworkData] = useState<NetworkData>(
    generateSimpleNetworkData()
  );
  const [selectedNode, setSelectedNode] = useState<NetworkNode | null>(null);
  const [hoveredNode, setHoveredNode] = useState<NetworkNode | null>(null);
  const [networkType, setNetworkType] = useState<"simple" | "full" | "dynamic">(
    "simple"
  );
  const [activeAgents, setActiveAgents] = useState<string[]>([]);

  const handleNetworkTypeChange = (type: "simple" | "full" | "dynamic") => {
    setNetworkType(type);
    switch (type) {
      case "simple":
        setNetworkData(generateSimpleNetworkData());
        break;
      case "full":
        setNetworkData(generateAgentNetworkData());
        break;
      case "dynamic":
        setNetworkData(generateDynamicNetworkData(activeAgents));
        break;
    }
  };

  const handleNodeClick = (node: NetworkNode) => {
    setSelectedNode(node);

    // Toggle agent active state for dynamic network
    if (networkType === "dynamic") {
      const newActiveAgents = activeAgents.includes(node.id)
        ? activeAgents.filter((id) => id !== node.id)
        : [...activeAgents, node.id];

      setActiveAgents(newActiveAgents);
      setNetworkData(generateDynamicNetworkData(newActiveAgents));
    }
  };

  const handleNodeHover = (node: NetworkNode | null) => {
    setHoveredNode(node);
  };

  const resetNetwork = () => {
    setActiveAgents([]);
    setSelectedNode(null);
    setHoveredNode(null);
    handleNetworkTypeChange(networkType);
  };

  return (
    <div className='min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 p-8'>
      <div className='max-w-7xl mx-auto space-y-8'>
        {/* Header */}
        <div className='text-center'>
          <h1 className='text-4xl font-bold text-gray-900 dark:text-white mb-4'>
            AI Agent Network Visualization
          </h1>
          <p className='text-lg text-gray-600 dark:text-gray-300 mb-6'>
            Explore the interconnected network of AI agents and their
            relationships
          </p>

          {/* Network Type Controls */}
          <div className='flex justify-center gap-4 mb-6'>
            <Button
              variant={networkType === "simple" ? "default" : "outline"}
              onClick={() => handleNetworkTypeChange("simple")}
            >
              Simple Network
            </Button>
            <Button
              variant={networkType === "full" ? "default" : "outline"}
              onClick={() => handleNetworkTypeChange("full")}
            >
              Full Network
            </Button>
            <Button
              variant={networkType === "dynamic" ? "default" : "outline"}
              onClick={() => handleNetworkTypeChange("dynamic")}
            >
              Dynamic Network
            </Button>
            <Button variant='secondary' onClick={resetNetwork}>
              Reset
            </Button>
          </div>
        </div>

        {/* Network Statistics */}
        <div className='grid grid-cols-1 md:grid-cols-4 gap-4 mb-6'>
          <Card>
            <CardHeader className='pb-2'>
              <CardTitle className='text-sm font-medium'>Total Nodes</CardTitle>
            </CardHeader>
            <CardContent>
              <div className='text-2xl font-bold'>
                {networkData.nodes.length}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className='pb-2'>
              <CardTitle className='text-sm font-medium'>
                Total Connections
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className='text-2xl font-bold'>
                {networkData.links.length}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className='pb-2'>
              <CardTitle className='text-sm font-medium'>
                Active Agents
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className='text-2xl font-bold'>{activeAgents.length}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className='pb-2'>
              <CardTitle className='text-sm font-medium'>
                Network Type
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className='text-lg font-semibold capitalize'>
                {networkType}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Network Graph */}
        <AgentNetworkGraph
          data={networkData}
          width={1000}
          height={700}
          onNodeClick={handleNodeClick}
          onNodeHover={handleNodeHover}
        />

        {/* Network Information Panel */}
        <div className='grid grid-cols-1 lg:grid-cols-2 gap-6'>
          {/* Connection Types Legend */}
          <Card>
            <CardHeader>
              <CardTitle>Connection Types</CardTitle>
              <CardDescription>
                Different types of relationships between agents
              </CardDescription>
            </CardHeader>
            <CardContent className='space-y-4'>
              <div className='flex items-center gap-3'>
                <div className='w-4 h-1 bg-green-500 rounded'></div>
                <div>
                  <p className='font-medium'>Collaboration</p>
                  <p className='text-sm text-gray-600 dark:text-gray-300'>
                    Agents working together on tasks
                  </p>
                </div>
              </div>

              <div className='flex items-center gap-3'>
                <div className='w-4 h-1 bg-blue-500 rounded'></div>
                <div>
                  <p className='font-medium'>Data Flow</p>
                  <p className='text-sm text-gray-600 dark:text-gray-300'>
                    Information and data exchange
                  </p>
                </div>
              </div>

              <div className='flex items-center gap-3'>
                <div className='w-4 h-1 bg-yellow-500 rounded'></div>
                <div>
                  <p className='font-medium'>Dependency</p>
                  <p className='text-sm text-gray-600 dark:text-gray-300'>
                    Service dependencies and requirements
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Active Agents Panel */}
          <Card>
            <CardHeader>
              <CardTitle>Active Agents</CardTitle>
              <CardDescription>
                Currently active agents in the network
              </CardDescription>
            </CardHeader>
            <CardContent>
              {activeAgents.length > 0 ? (
                <div className='space-y-2'>
                  {activeAgents.map((agentId) => {
                    const agent = networkData.nodes.find(
                      (n) => n.id === agentId
                    );
                    return agent ? (
                      <div
                        key={agentId}
                        className='flex items-center justify-between p-2 bg-gray-50 dark:bg-gray-700 rounded'
                      >
                        <span className='font-medium'>{agent.name}</span>
                        <Badge variant='secondary'>{agent.type}</Badge>
                      </div>
                    ) : null;
                  })}
                </div>
              ) : (
                <p className='text-gray-600 dark:text-gray-300'>
                  {networkType === "dynamic"
                    ? "Click on nodes to activate agents"
                    : "No active agents in this network type"}
                </p>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Instructions */}
        <Card>
          <CardHeader>
            <CardTitle>How to Use</CardTitle>
          </CardHeader>
          <CardContent className='space-y-2'>
            <p>
              • <strong>Click and drag</strong> nodes to reposition them
            </p>
            <p>
              • <strong>Hover</strong> over nodes to see details
            </p>
            <p>
              • <strong>Click</strong> nodes to select and highlight connections
            </p>
            <p>
              • <strong>Zoom and pan</strong> to explore different areas
            </p>
            <p>
              • <strong>Switch network types</strong> to see different
              configurations
            </p>
            {networkType === "dynamic" && (
              <p>
                • <strong>Dynamic mode:</strong> Click nodes to
                activate/deactivate agents
              </p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
