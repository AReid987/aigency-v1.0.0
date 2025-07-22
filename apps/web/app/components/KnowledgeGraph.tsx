import { useEffect, useRef } from "react";
import * as d3 from "d3";
import { SimulationNodeDatum, SimulationLinkDatum } from 'd3';

interface GraphNode extends SimulationNodeDatum {
  id: string;
  label: string;
}

interface GraphLink extends SimulationLinkDatum<GraphNode> {
  source: string | GraphNode;
  target: string | GraphNode;
}

interface KnowledgeGraphProps {
  data: {
    nodes: GraphNode[];
    links: GraphLink[];
  };
}

export default function KnowledgeGraph({ data }: KnowledgeGraphProps) {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    const width = svgRef.current.clientWidth;
    const height = svgRef.current.clientHeight;

    // Clear previous content
    svg.selectAll("*").remove();

    // Create a force simulation
    const simulation = d3
      .forceSimulation<GraphNode, GraphLink>(data.nodes)
      .force(
        "link",
        d3.forceLink<GraphNode, GraphLink>(data.links).id((d) => d.id),
      )
      .force("charge", d3.forceManyBody().strength(-100))
      .force("center", d3.forceCenter(width / 2, height / 2));

    // Create links
    const link = svg
      .append("g")
      .selectAll("line")
      .data(data.links)
      .enter()
      .append("line")
      .attr("stroke", "#999")
      .attr("stroke-width", 2);

    // Create nodes
    const node = svg
      .append("g")
      .selectAll("circle")
      .data(data.nodes)
      .enter()
      .append("circle")
      .attr("r", 10)
      .attr("fill", "#69b3a2")
      .call(
        d3
          .drag<SVGCircleElement, GraphNode>()
          .on("start", (event) => {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            event.subject.fx = event.subject.x;
            event.subject.fy = event.subject.y;
          })
          .on("drag", (event) => {
            event.subject.fx = event.x;
            event.subject.fy = event.y;
          })
          .on("end", (event) => {
            if (!event.active) simulation.alphaTarget(0);
            event.subject.fx = null;
            event.subject.fy = null;
          }),
      );

    // Add labels
    const label = svg
      .append("g")
      .selectAll("text")
      .data(data.nodes)
      .enter()
      .append("text")
      .text((d) => d.label)
      .attr("font-size", 12)
      .attr("dx", 15)
      .attr("dy", 4);

    // Update positions on each tick
    simulation.on("tick", () => {
      link
        .attr("x1", (d) => (d.source as GraphNode).x!)
        .attr("y1", (d) => (d.source as GraphNode).y!)
        .attr("x2", (d) => (d.target as GraphNode).x!)
        .attr("y2", (d) => (d.target as GraphNode).y!);

      node.attr("cx", (d) => d.x!).attr("cy", (d) => d.y!);

      label.attr("x", (d) => d.x!).attr("y", (d) => d.y!);
    });

    // Cleanup on unmount
    return () => {
      simulation.stop();
    };
  }, [data]);

  return (
    <svg
      ref={svgRef}
      width="100%"
      height="500"
      style={{ border: "1px solid #ddd" }}
      data-oid="cc2egnl"
    />
  );
}
