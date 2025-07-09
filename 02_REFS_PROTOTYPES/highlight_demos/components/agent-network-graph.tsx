// D3.js Force-Directed Graph for AI Agent Network (Simplified)
'use client';

import * as d3 from 'd3';
import { useEffect, useRef, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

interface Node {
  id: string;
  name: string;
  type: 'primary' | 'secondary' | 'hub';
  capabilities: string[];
  x?: number;
  y?: number;
  fx?: number | null;
  fy?: number | null;
}

interface Link {
  source: string | Node;
  target: string | Node;
  value: number;
  type: 'collaboration' | 'data-flow' | 'dependency';
}

interface NetworkData {
  nodes: Node[];
  links: Link[];
}

interface AgentNetworkGraphProps {
  data: NetworkData;
  width?: number;
  height?: number;
  onNodeClick?: (node: Node) => void;
  onNodeHover?: (node: Node | null) => void;
}

export default function AgentNetworkGraph({ 
  data, 
  width = 800, 
  height = 600,
  onNodeClick,
  onNodeHover 
}: AgentNetworkGraphProps) {
  const svgRef = useRef<SVGSVGElement>(null);
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [hoveredNode, setHoveredNode] = useState<Node | null>(null);
  const [isSimulationRunning, setIsSimulationRunning] = useState(true);
  
  useEffect(() => {
    if (!data || !svgRef.current) return;
    
    // Clear previous graph
    d3.select(svgRef.current).selectAll("*").remove();
    
    // Create SVG with responsive viewBox
    const svg = d3.select(svgRef.current)
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px;");
      
    // Add zoom behavior
    const g = svg.append("g");
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.1, 4])
      .on("zoom", (event) => {
        g.attr("transform", event.transform);
      });
    svg.call(zoom);
      
    // Create simulation
    const simulation = d3.forceSimulation(data.nodes)
      .force("link", d3.forceLink(data.links).id((d: any) => d.id).distance(120).strength(0.8))
      .force("charge", d3.forceManyBody().strength(-800).distanceMax(300))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide().radius(60).strength(0.9))
      .force("x", d3.forceX(width / 2).strength(0.1))
      .force("y", d3.forceY(height / 2).strength(0.1));
      
    // Create arrow markers for directed links
    const defs = svg.append("defs");
    
    const linkTypes = ['collaboration', 'data-flow', 'dependency'];
    const linkColors = ['#10b981', '#3b82f6', '#f59e0b'];
    
    linkTypes.forEach((type, i) => {
      defs.append("marker")
        .attr("id", `arrow-${type}`)
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 35)
        .attr("refY", 0)
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
        .append("path")
        .attr("d", "M0,-5L10,0L0,5")
        .attr("fill", linkColors[i]);
    });
      
    // Create links
    const link = g.append("g")
      .attr("class", "links")
      .selectAll("line")
      .data(data.links)
      .join("line")
      .attr("stroke", (d: any) => {
        const colorMap: Record<string, string> = {
          'collaboration': '#10b981',
          'data-flow': '#3b82f6',
          'dependency': '#f59e0b'
        };
        return colorMap[d.type] || '#6b7280';
      })
      .attr("stroke-opacity", 0.8)
      .attr("stroke-width", (d: any) => Math.sqrt(d.value) * 2)
      .attr("marker-end", (d: any) => `url(#arrow-${d.type})`)
      .style("filter", "drop-shadow(0 2px 4px rgba(0,0,0,0.1))");
      
    // Create node groups
    const node = g.append("g")
      .attr("class", "nodes")
      .selectAll("g")
      .data(data.nodes)
      .join("g")
      .attr("class", "node")
      .style("cursor", "pointer");
      
    // Add main circles to nodes
    node.append("circle")
      .attr("r", (d: any) => d.type === 'hub' ? 30 : d.type === 'primary' ? 25 : 20)
      .attr("fill", (d: any) => {
        const colorMap: Record<string, string> = {
          'primary': '#4f46e5',
          'secondary': '#10b981',
          'hub': '#dc2626'
        };
        return colorMap[d.type] || '#6b7280';
      })
      .attr("stroke", "#ffffff")
      .attr("stroke-width", 3)
      .style("filter", "drop-shadow(0 4px 8px rgba(0,0,0,0.2))")
      .on("mouseover", function(event, d: any) {
        d3.select(this)
          .transition()
          .duration(200)
          .attr("r", (d.type === 'hub' ? 35 : d.type === 'primary' ? 30 : 25))
          .attr("stroke-width", 4);
        setHoveredNode(d);
        onNodeHover?.(d);
      })
      .on("mouseout", function(event, d: any) {
        d3.select(this)
          .transition()
          .duration(200)
          .attr("r", (d.type === 'hub' ? 30 : d.type === 'primary' ? 25 : 20))
          .attr("stroke-width", 3);
        setHoveredNode(null);
        onNodeHover?.(null);
      })
      .on("click", function(event, d: any) {
        setSelectedNode(d);
        onNodeClick?.(d);
      });
      
    // Add icons to nodes
    node.append("text")
      .attr("text-anchor", "middle")
      .attr("dy", ".35em")
      .attr("fill", "#ffffff")
      .attr("font-size", (d: any) => d.type === 'hub' ? "16px" : "14px")
      .attr("font-weight", "bold")
      .style("pointer-events", "none")
      .text((d: any) => {
        const iconMap: Record<string, string> = {
          'primary': '🤖',
          'secondary': '⚡',
          'hub': '🌐'
        };
        return iconMap[d.type] || '●';
      });
      
    // Add labels below nodes
    node.append("text")
      .attr("text-anchor", "middle")
      .attr("dy", (d: any) => (d.type === 'hub' ? 45 : d.type === 'primary' ? 40 : 35))
      .attr("fill", "#ffffff")
      .attr("font-size", "12px")
      .attr("font-weight", "600")
      .style("pointer-events", "none")
      .style("text-shadow", "0 1px 2px rgba(0,0,0,0.8)")
      .text((d: any) => d.name);
      
    // Add title for tooltip
    node.append("title")
      .text((d: any) => `${d.name}\nType: ${d.type}\nCapabilities: ${d.capabilities.join(", ")}`);
      
    // Update positions on tick
    simulation.on("tick", () => {
      link
        .attr("x1", (d: any) => d.source.x)
        .attr("y1", (d: any) => d.source.y)
        .attr("x2", (d: any) => d.target.x)
        .attr("y2", (d: any) => d.target.y);
        
      node.attr("transform", (d: any) => `translate(${d.x},${d.y})`);
    });
    
    // Simulation control
    simulation.on("end", () => {
      setIsSimulationRunning(false);
    });
    
    // Simple drag behavior
    const dragHandler = d3.drag<any, any>()
      .on("start", function(event, d: any) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
        setIsSimulationRunning(true);
      })
      .on("drag", function(event, d: any) {
        d.fx = event.x;
        d.fy = event.y;
      })
      .on("end", function(event, d: any) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      });
    
    node.call(dragHandler);
    
    // Cleanup function
    return () => {
      simulation.stop();
    };
  }, [data, width, height, onNodeClick, onNodeHover]);
  
  const resetGraph = () => {
    if (!svgRef.current) return;
    
    const svg = d3.select(svgRef.current);
    const nodes = svg.selectAll(".node circle");
    const links = svg.selectAll(".links line");
    
    // Reset all styles
    nodes.attr("fill-opacity", 1);
    links.attr("stroke-opacity", 0.8);
    setSelectedNode(null);
  };
  
  const centerGraph = () => {
    if (!svgRef.current) return;
    
    const svg = d3.select(svgRef.current);
    const zoom = d3.zoom<SVGSVGElement, unknown>();
    
    svg.transition()
      .duration(750)
      .call(zoom.transform, d3.zoomIdentity);
  };
  
  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-2xl font-bold">AI Agent Network</CardTitle>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={resetGraph}>
              Reset Selection
            </Button>
            <Button variant="outline" size="sm" onClick={centerGraph}>
              Center View
            </Button>
          </div>
        </div>
        <div className="flex gap-2 mt-2">
          <Badge variant="outline" className="bg-indigo-50 text-indigo-700">
            🤖 Primary Agents
          </Badge>
          <Badge variant="outline" className="bg-green-50 text-green-700">
            ⚡ Secondary Agents
          </Badge>
          <Badge variant="outline" className="bg-red-50 text-red-700">
            🌐 Hub Nodes
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="relative">
          <svg ref={svgRef} className="border rounded-lg shadow-lg" />
          
          {/* Node Details Panel */}
          {(selectedNode || hoveredNode) && (
            <div className="absolute top-4 right-4 bg-white dark:bg-gray-800 p-4 rounded-lg shadow-lg border max-w-xs">
              <h3 className="font-semibold text-lg mb-2">
                {(selectedNode || hoveredNode)?.name}
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-300 mb-2">
                Type: <span className="capitalize">{(selectedNode || hoveredNode)?.type}</span>
              </p>
              <div className="space-y-1">
                <p className="text-sm font-medium">Capabilities:</p>
                <div className="flex flex-wrap gap-1">
                  {(selectedNode || hoveredNode)?.capabilities.map((cap, index) => (
                    <Badge key={index} variant="secondary" className="text-xs">
                      {cap}
                    </Badge>
                  ))}
                </div>
              </div>
            </div>
          )}
          
          {/* Simulation Status */}
          <div className="absolute bottom-4 left-4">
            <Badge variant={isSimulationRunning ? "default" : "secondary"}>
              {isSimulationRunning ? "Simulation Running" : "Simulation Stable"}
            </Badge>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
