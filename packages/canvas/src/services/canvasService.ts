import { CanvasNode, CanvasEdge, ViewType } from '../types';

interface CanvasServiceConfig {
    enableAutoSave?: boolean;
    autoSaveInterval?: number;
    maxHistorySteps?: number;
}

class CanvasService {
    private config: CanvasServiceConfig;
    private history: Array<{ nodes: CanvasNode[]; edges: CanvasEdge[] }> = [];
    private currentHistoryIndex = -1;

    constructor(config: CanvasServiceConfig = {}) {
        this.config = {
            enableAutoSave: true,
            autoSaveInterval: 30000, // 30 seconds
            maxHistorySteps: 50,
            ...config,
        };
    }

    // Node operations
    createNode(type: string, position: { x: number; y: number }, data: Record<string, any> = {}): CanvasNode {
        return {
            id: this.generateId(),
            type,
            position,
            data,
        };
    }

    updateNode(nodeId: string, updates: Partial<CanvasNode>, nodes: CanvasNode[]): CanvasNode[] {
        return nodes.map(node =>
            node.id === nodeId ? { ...node, ...updates } : node
        );
    }

    deleteNode(nodeId: string, nodes: CanvasNode[], edges: CanvasEdge[]): { nodes: CanvasNode[]; edges: CanvasEdge[] } {
        const filteredNodes = nodes.filter(node => node.id !== nodeId);
        const filteredEdges = edges.filter(edge => edge.source !== nodeId && edge.target !== nodeId);

        return {
            nodes: filteredNodes,
            edges: filteredEdges,
        };
    }

    // Edge operations
    createEdge(source: string, target: string, type: string = 'default', data: Record<string, any> = {}): CanvasEdge {
        return {
            id: this.generateId(),
            source,
            target,
            type,
            data,
        };
    }

    updateEdge(edgeId: string, updates: Partial<CanvasEdge>, edges: CanvasEdge[]): CanvasEdge[] {
        return edges.map(edge =>
            edge.id === edgeId ? { ...edge, ...updates } : edge
        );
    }

    deleteEdge(edgeId: string, edges: CanvasEdge[]): CanvasEdge[] {
        return edges.filter(edge => edge.id !== edgeId);
    }

    // Layout operations
    autoLayout(nodes: CanvasNode[], edges: CanvasEdge[], algorithm: 'hierarchical' | 'force' | 'circular' = 'hierarchical'): CanvasNode[] {
        // Simple auto-layout implementation
        switch (algorithm) {
            case 'hierarchical':
                return this.hierarchicalLayout(nodes, edges);
            case 'force':
                return this.forceLayout(nodes, edges);
            case 'circular':
                return this.circularLayout(nodes);
            default:
                return nodes;
        }
    }

    // View transformations
    transformForView(nodes: CanvasNode[], edges: CanvasEdge[], view: ViewType): { nodes: CanvasNode[]; edges: CanvasEdge[] } {
        switch (view) {
            case '2d':
                return { nodes, edges };
            case '3d':
                return this.transform3D(nodes, edges);
            case 'iso':
                return this.transformIsometric(nodes, edges);
            default:
                return { nodes, edges };
        }
    }

    // History management
    saveToHistory(nodes: CanvasNode[], edges: CanvasEdge[]): void {
        // Remove any history after current index
        this.history = this.history.slice(0, this.currentHistoryIndex + 1);

        // Add new state
        this.history.push({ nodes: [...nodes], edges: [...edges] });
        this.currentHistoryIndex++;

        // Limit history size
        if (this.history.length > this.config.maxHistorySteps!) {
            this.history.shift();
            this.currentHistoryIndex--;
        }
    }

    undo(): { nodes: CanvasNode[]; edges: CanvasEdge[] } | null {
        if (this.currentHistoryIndex > 0) {
            this.currentHistoryIndex--;
            const state = this.history[this.currentHistoryIndex];
            return state !== undefined ? state : null;
        }
        return null;
    }

    redo(): { nodes: CanvasNode[]; edges: CanvasEdge[] } | null {
        if (this.currentHistoryIndex < this.history.length - 1) {
            this.currentHistoryIndex++;
            const state = this.history[this.currentHistoryIndex];
            return state !== undefined ? state : null;
        }
        return null;
    }

    // Export/Import
    exportCanvas(nodes: CanvasNode[], edges: CanvasEdge[], format: 'json' | 'svg' | 'png' = 'json'): string {
        switch (format) {
            case 'json':
                return JSON.stringify({ nodes, edges }, null, 2);
            case 'svg':
                // TODO: Implement SVG export
                throw new Error('SVG export not implemented yet');
            case 'png':
                // TODO: Implement PNG export
                throw new Error('PNG export not implemented yet');
            default:
                return JSON.stringify({ nodes, edges });
        }
    }

    importCanvas(data: string): { nodes: CanvasNode[]; edges: CanvasEdge[] } {
        try {
            const parsed = JSON.parse(data);
            return {
                nodes: parsed.nodes || [],
                edges: parsed.edges || [],
            };
        } catch (error) {
            throw new Error('Invalid canvas data format');
        }
    }

    // Private helper methods
    private generateId(): string {
        return `node_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    private hierarchicalLayout(nodes: CanvasNode[], edges: CanvasEdge[]): CanvasNode[] {
        // Simple hierarchical layout
        const levels: Record<string, number> = {};
        const visited = new Set<string>();

        // Find root nodes (nodes with no incoming edges)
        const rootNodes = nodes.filter(node =>
            !edges.some(edge => edge.target === node.id)
        );

        // Assign levels
        const assignLevel = (nodeId: string, level: number) => {
            if (visited.has(nodeId)) return;
            visited.add(nodeId);
            levels[nodeId] = level;

            const children = edges
                .filter(edge => edge.source === nodeId)
                .map(edge => edge.target);

            children.forEach(childId => assignLevel(childId, level + 1));
        };

        rootNodes.forEach(node => assignLevel(node.id, 0));

        // Position nodes
        const levelCounts: Record<number, number> = {};
        const levelPositions: Record<number, number> = {};

        Object.values(levels).forEach(level => {
            levelCounts[level] = (levelCounts[level] || 0) + 1;
        });

        return nodes.map(node => {
            const level = levels[node.id] || 0;
            const positionInLevel = levelPositions[level] || 0;
            levelPositions[level] = positionInLevel + 1;

            return {
                ...node,
                position: {
                    x: positionInLevel * 200,
                    y: level * 150,
                },
            };
        });
    }

    private forceLayout(nodes: CanvasNode[], edges: CanvasEdge[]): CanvasNode[] {
        // Simple force-directed layout simulation
        // This is a basic implementation - in production, you'd use a proper physics engine
        return nodes.map((node, index) => ({
            ...node,
            position: {
                x: Math.cos(index * 2 * Math.PI / nodes.length) * 200 + 300,
                y: Math.sin(index * 2 * Math.PI / nodes.length) * 200 + 300,
            },
        }));
    }

    private circularLayout(nodes: CanvasNode[]): CanvasNode[] {
        const radius = Math.max(100, nodes.length * 30);
        const centerX = 300;
        const centerY = 300;

        return nodes.map((node, index) => ({
            ...node,
            position: {
                x: centerX + radius * Math.cos(index * 2 * Math.PI / nodes.length),
                y: centerY + radius * Math.sin(index * 2 * Math.PI / nodes.length),
            },
        }));
    }

    private transform3D(nodes: CanvasNode[], edges: CanvasEdge[]): { nodes: CanvasNode[]; edges: CanvasEdge[] } {
        // Add z-coordinate for 3D positioning
        const transformedNodes = nodes.map(node => ({
            ...node,
            data: {
                ...node.data,
                z: node.data.z || 0,
            },
        }));

        return { nodes: transformedNodes, edges };
    }

    private transformIsometric(nodes: CanvasNode[], edges: CanvasEdge[]): { nodes: CanvasNode[]; edges: CanvasEdge[] } {
        // Transform coordinates for isometric view
        const transformedNodes = nodes.map(node => {
            const { x, y } = node.position;
            const z = node.data.z || 0;

            // Isometric projection
            const isoX = (x - y) * Math.cos(Math.PI / 6);
            const isoY = (x + y) * Math.sin(Math.PI / 6) - z;

            return {
                ...node,
                position: {
                    x: isoX,
                    y: isoY,
                },
            };
        });

        return { nodes: transformedNodes, edges };
    }
}

// Export singleton instance
export const canvasService = new CanvasService();
