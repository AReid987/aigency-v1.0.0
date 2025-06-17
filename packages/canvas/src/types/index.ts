import type { Node, Edge } from 'reactflow';

// Basic Types
export type ViewType = '2d' | '3d' | 'iso';
export type CanvasMode = 'archvision' | 'braincraft' | 'hybrid';
export type DiagramType = 'flowchart' | 'sequence' | 'class' | 'state' | 'er' | 'gantt' | 'pie' | 'mindmap';

export interface CanvasNode {
    id: string;
    type: string;
    position: { x: number; y: number };
    data: Record<string, any>;
}

export interface CanvasEdge {
    id: string;
    source: string;
    target: string;
    type?: string;
    data?: Record<string, any>;
}

export interface Diagram {
    id: string;
    type: DiagramType;
    code: string;
    createdAt: Date;
    updatedAt: Date;
}

// Additional interfaces for compatibility
export interface DiagramData {
    id: string;
    type: DiagramType;
    code: string;
    title?: string;
    createdAt: Date;
    updatedAt: Date;
    metadata?: Record<string, any>;
}

export interface CanvasState {
    currentView: ViewType;
    currentMode: CanvasMode;
    mode: CanvasMode;
    nodes: CanvasNode[];
    edges: CanvasEdge[];
    config: CanvasConfig;
    selectedNodes: string[];
    selectedEdges: string[];
    isLoading: boolean;
    error: string | null;
}

export interface ChatMessage {
    id?: string;
    content: string;
    sender: 'user' | 'assistant';
    diagramCode?: string;
    timestamp?: Date;
}

export interface CanvasConfig {
    enableAI: boolean;
    enableCollaboration: boolean;
    enableIsometric: boolean;
    theme: 'light' | 'dark';
    defaultView: ViewType;
    defaultMode: CanvasMode;
}

export interface CanvasContextValue {
    currentView: ViewType;
    currentMode: CanvasMode;
    nodes: CanvasNode[];
    edges: CanvasEdge[];
    config: CanvasConfig;
    setView: (view: ViewType) => void;
    setMode: (mode: CanvasMode) => void;
    setNodes: (nodes: CanvasNode[]) => void;
    setEdges: (edges: CanvasEdge[]) => void;
    addNode: (node: Partial<CanvasNode>) => void;
    addEdge: (edge: Partial<CanvasEdge>) => void;
    removeNode: (nodeId: string) => void;
    removeEdge: (edgeId: string) => void;
    updateNode: (nodeId: string, data: Partial<CanvasNode>) => void;
    updateEdge: (edgeId: string, data: Partial<CanvasEdge>) => void;
    clear: () => void;
}

export interface DiagramContextValue {
    currentDiagram: Diagram | null;
    messages: ChatMessage[];
    isGenerating: boolean;
    generateDiagram: (prompt: string, type?: DiagramType) => Promise<Diagram>;
    updateDiagram: (id: string, code: string) => Promise<Diagram>;
    addMessage: (message: Omit<ChatMessage, 'id' | 'timestamp'>) => void;
    clearMessages: () => void;
}

// Component Props Types
export interface InfiniteCanvasProps {
    mode?: CanvasMode;
    defaultView?: ViewType;
    enableAI?: boolean;
    enableCollaboration?: boolean;
    onViewChange?: (view: ViewType) => void;
    onModeChange?: (mode: CanvasMode) => void;
}

export interface ViewSelectorProps {
    currentView: ViewType;
    onViewChange: (view: ViewType) => void;
}

export interface ToolbarProps {
    mode: CanvasMode;
    onModeChange: (mode: CanvasMode) => void;
    enableAI?: boolean;
}

export interface DiagramPanelProps {
    code: string;
    type?: DiagramType;
    isLoading?: boolean;
}

export interface ChatInterfaceProps {
    onSendMessage: (message: string) => Promise<void>;
    isLoading?: boolean;
    messages?: ChatMessage[];
}

export interface ArchVisionCanvasProps {
    view: ViewType;
    onViewChange?: (view: ViewType) => void;
    initialNodes?: Node[];
    initialEdges?: Edge[];
}

export interface BrainCraftCanvasProps {
    initialDiagramType?: DiagramType;
    onDiagramGenerate?: (code: string, type: DiagramType) => void;
    onDiagramUpdate?: (code: string, type: DiagramType) => void;
}
