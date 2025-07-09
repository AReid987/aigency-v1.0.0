import React, { useRef, useState, useEffect, useMemo, useCallback } from 'react';
import { Canvas, useFrame, extend, useThree } from '@react-three/fiber';
import { OrbitControls, Text, Html } from '@react-three/drei';
import * as THREE from 'three';
import { ForceGraph3D } from 'react-force-graph';

// Extend THREE namespace for custom shaders if needed (not used in this basic version)
// extend({ LineMaterial });

const Node = React.memo(({ node, onNodeClick, onNodeHover, onNodeLeave, isSelected, isHovered }) => {
  const meshRef = useRef();
  const [internalHovered, setInternalHovered] = useState(false);

  const color = useMemo(() => {
    if (isSelected) return '#ff00ff'; // Magenta for selected
    if (isHovered || internalHovered) return '#00ffff'; // Cyan for hovered
    return node.color || '#007bff'; // Default blue or node-specific color
  }, [isSelected, isHovered, internalHovered, node.color]);

  const scale = useMemo(() => {
    let baseScale = node.val || 1;
    if (isSelected) baseScale *= 1.5;
    else if (isHovered || internalHovered) baseScale *= 1.2;
    return [baseScale, baseScale, baseScale];
  }, [isSelected, isHovered, internalHovered, node.val]);

  const handlePointerOver = useCallback((event) => {
    event.stopPropagation();
    setInternalHovered(true);
    if (onNodeHover) onNodeHover(node);
  }, [node, onNodeHover]);

  const handlePointerOut = useCallback((event) => {
    event.stopPropagation();
    setInternalHovered(false);
    if (onNodeLeave) onNodeLeave(node);
  }, [node, onNodeLeave]);

  const handleClick = useCallback((event) => {
    event.stopPropagation();
    if (onNodeClick) onNodeClick(node);
  }, [node, onNodeClick]);

  return (
    <mesh
      ref={meshRef}
      position={[node.x, node.y, node.z]}
      scale={scale}
      onClick={handleClick}
      onPointerOver={handlePointerOver}
      onPointerOut={handlePointerOut}
    >
      <sphereGeometry args={[0.5, 32, 32]} />
      <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.3} roughness={0.4} metalness={0.1} />
      <Html distanceFactor={10}>
        <div style={{
          color: 'white',
          backgroundColor: 'rgba(0,0,0,0.5)',
          padding: '2px 5px',
          borderRadius: '3px',
          fontSize: '10px',
          pointerEvents: 'none', // Important for interaction with mesh
          userSelect: 'none',
          textAlign: 'center',
          minWidth: '50px'
        }}>
          {node.label || node.id}
        </div>
      </Html>
    </mesh>
  );
});

const Edge = React.memo(({ edge, nodes }) => {
  const sourceNode = nodes.find(n => n.id === edge.source);
  const targetNode = nodes.find(n => n.id === edge.target);

  if (!sourceNode || !targetNode) return null;

  const points = useMemo(() => [
    new THREE.Vector3(sourceNode.x, sourceNode.y, sourceNode.z),
    new THREE.Vector3(targetNode.x, targetNode.y, targetNode.z)
  ], [sourceNode, targetNode]);

  const lineGeometry = useMemo(() => new THREE.BufferGeometry().setFromPoints(points), [points]);

  return (
    <line geometry={lineGeometry}>
      <lineBasicMaterial color={edge.color || '#ffffff'} linewidth={edge.width || 0.5} transparent opacity={0.5} />
    </line>
  );
});

const DetailPanel = React.memo(({ node, onClose }) => {
  if (!node) return null;

  return (
    <div style={{
      position: 'absolute',
      top: '20px',
      right: '20px',
      width: '300px',
      maxHeight: '80vh',
      overflowY: 'auto',
      background: 'rgba(40, 40, 40, 0.9)',
      color: 'white',
      padding: '20px',
      borderRadius: '8px',
      boxShadow: '0 4px 15px rgba(0,0,0,0.5)',
      fontFamily: 'Arial, sans-serif',
      zIndex: 1000,
    }}>
      <button onClick={onClose} style={{
        position: 'absolute',
        top: '10px',
        right: '10px',
        background: 'transparent',
        border: 'none',
        color: 'white',
        fontSize: '20px',
        cursor: 'pointer'
      }}>×</button>
      <h3 style={{ marginTop: 0, borderBottom: '1px solid #555', paddingBottom: '10px' }}>{node.label || node.id}</h3>
      <p><strong>Type:</strong> {node.type || 'N/A'}</p>
      <p><strong>Importance:</strong> {node.importance || 'N/A'}</p>
      {node.description && <p><strong>Description:</strong> {node.description}</p>}
      {node.properties && Object.keys(node.properties).length > 0 && (
        <div>
          <h4>Properties:</h4>
          <ul style={{ listStyleType: 'none', paddingLeft: 0 }}>
            {Object.entries(node.properties).map(([key, value]) => (
              <li key={key} style={{ marginBottom: '5px' }}>
                <strong>{key}:</strong> {typeof value === 'object' ? JSON.stringify(value) : value.toString()}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
});

const KnowledgeGraph = ({ data }) => {
  const fgRef = useRef();
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [selectedNode, setSelectedNode] = useState(null);
  const [hoveredNode, setHoveredNode] = useState(null);
  const [initialCenter, setInitialCenter] = useState(false);

  useEffect(() => {
    if (data && data.nodes && data.edges) {
      const nodes = data.nodes.map(n => ({ ...n, id: String(n.id) })); // Ensure ID is string
      const links = data.edges.map(e => ({
        ...e,
        source: String(e.source),
        target: String(e.target),
        // value: e.weight || 1, // Optional: for link strength in physics
      }));
      setGraphData({ nodes, links });
      setSelectedNode(null); // Reset selection when data changes
      setInitialCenter(false); // Re-trigger centering
    } else {
      setGraphData({ nodes: [], links: [] });
    }
  }, [data]);

  useEffect(() => {
    if (fgRef.current && graphData.nodes.length > 0 && !initialCenter) {
      // Center camera on graph after initial load or data change
      fgRef.current.zoomToFit(400, 100); // Adjust padding as needed
      // Optional: Set initial rotation
      // fgRef.current.cameraPosition({ z: 150 });
      setInitialCenter(true);
    }
  }, [graphData, initialCenter]);

  const handleNodeClick = useCallback((node) => {
    setSelectedNode(prev => (prev && prev.id === node.id ? null : node));
    // Optional: Move camera to focus on clicked node
    if (fgRef.current) {
      const distance = 80; // Adjust distance as needed
      const distRatio = 1 + distance/Math.hypot(node.x, node.y, node.z);
      fgRef.current.cameraPosition(
        { x: node.x * distRatio, y: node.y * distRatio, z: node.z * distRatio }, // new position
        node, // lookAt ({ x, y, z })
        1000  // ms transition duration
      );
    }
  }, []);

  const handleNodeHover = useCallback((node) => {
    setHoveredNode(node);
    // Change cursor style
    document.body.style.cursor = node ? 'pointer' : 'default';
  }, []);

  const handleNodeLeave = useCallback(() => {
    setHoveredNode(null);
    document.body.style.cursor = 'default';
  }, []);

  const nodeCanvasObject = useCallback((node, ctx, globalScale) => {
    const label = node.label || node.id;
    const fontSize = 12 / globalScale;
    ctx.font = `${fontSize}px Sans-Serif`;
    const textWidth = ctx.measureText(label).width;
    const bgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2);

    ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
    ctx.fillRect(node.x - bgDimensions[0] / 2, node.y - bgDimensions[1] / 2 + 10, bgDimensions[0], bgDimensions[1]);

    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle = node.color || 'white';
    ctx.fillText(label, node.x, node.y + 10 + fontSize / 2);

    // Node sphere itself
    ctx.beginPath();
    let sphereRadius = (node.val || 1) * 0.5 * globalScale * 0.2; // Adjust multiplier for visual size
    sphereRadius = Math.max(1, sphereRadius); // Ensure a minimum visible size

    ctx.arc(node.x, node.y, sphereRadius, 0, 2 * Math.PI, false);
    ctx.fillStyle = selectedNode && selectedNode.id === node.id ? 'magenta' :
                    hoveredNode && hoveredNode.id === node.id ? 'cyan' :
                    node.color || 'blue';
    ctx.fill();

    node.__bckgDimensions = bgDimensions; // save BoundingBox for iteration
  }, [selectedNode, hoveredNode]);

  const linkColor = useCallback(link => {
    return link.color || 'rgba(255,255,255,0.3)';
  }, []);

  const linkWidth = useCallback(link => {
    return link.width || 0.5;
  }, []);

  if (!graphData.nodes || graphData.nodes.length === 0) {
    return (
      <div style={{ width: '100%', height: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center', background: '#111', color: 'white' }}>
        <p>Loading graph data or no data available...</p>
      </div>
    );
  }

  return (
    <div style={{ width: '100%', height: '100vh', background: '#111' }}>
      <ForceGraph3D
        ref={fgRef}
        graphData={graphData}
        nodeId="id"
        nodeLabel="label"
        nodeVal="val" // Node size
        nodeColor="color"
        nodeRelSize={4} // Adjust for overall node size scaling in ForceGraph3D
        // nodeCanvasObjectMode={() => 'after'}
        // nodeCanvasObject={nodeCanvasObject} // Using custom node rendering via <Node> component is generally preferred with R3F
        
        // Using R3F components for nodes and links for more control
        nodeThreeObject={node => (
          <Node
            node={node}
            onNodeClick={handleNodeClick}
            onNodeHover={handleNodeHover}
            onNodeLeave={handleNodeLeave}
            isSelected={selectedNode && selectedNode.id === node.id}
            isHovered={hoveredNode && hoveredNode.id === node.id}
          />
        )}
        // linkThreeObjectExtend={true} // Not needed if not extending link material
        // linkMaterial={edge => new THREE.LineBasicMaterial({ color: edge.color || '#ffffff', linewidth: edge.width || 0.5, transparent: true, opacity: 0.5 })}
        // linkThreeObject={link => {
        //   // This approach for links is more complex with ForceGraph3D as it manages them internally.
        //   // It's often easier to rely on its built-in link rendering or customize via linkMaterial, linkColor, etc.
        //   // For full R3F component-based links, you might need a different graph library or manual implementation.
        //   return null; // Placeholder if trying to use R3F components for links, which is tricky with ForceGraph3D
        // }}
        linkColor={linkColor}
        linkWidth={linkWidth}
        linkDirectionalParticles={1}
        linkDirectionalParticleWidth={1.5}
        linkDirectionalParticleSpeed={0.006}
        
        // Interaction
        onNodeClick={handleNodeClick}
        onNodeHover={handleNodeHover}
        // onNodeDragEnd={node => { ... }}

        // Physics
        dagMode="td" // Top-down DAG layout, can be null for organic
        dagLevelDistance={50} // Distance between DAG levels
        cooldownTicks={100}
        onEngineStop={() => fgRef.current.zoomToFit(400, 100)} // Re-center after physics settle
        // forceEngine="d3" // or ngraph
        // d3AlphaDecay={0.0228}
        // d3VelocityDecay={0.4}
        // d3Force('link').distance(link => link.value * 10) // Example: link distance based on value
        // d3Force('charge').strength(-120)

        // Scene
        showNavInfo={true}
        backgroundColor="#111111"
      />
      <DetailPanel node={selectedNode} onClose={() => setSelectedNode(null)} />
    </div>
  );
};

export default KnowledgeGraph;