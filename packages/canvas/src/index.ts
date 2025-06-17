// Import styles
import './styles.css';

// Main exports for @aigency/canvas package
export { default as CanvasProvider } from './providers/CanvasProvider';
export { default as InfiniteCanvas } from './components/InfiniteCanvas';
export { default as ArchVisionCanvas } from './components/archvision/ArchVisionCanvas';
export { default as BrainCraftCanvas } from './components/braincraft/BrainCraftCanvas';
export { default as DiagramPanel } from './components/diagram/DiagramPanel';
export { default as ChatInterface } from './components/diagram/ChatInterface';
export { default as ViewSelector } from './components/ViewSelector';
export { default as Toolbar } from './components/Toolbar';

// Types
export type {
    ViewType,
    CanvasMode,
    DiagramType,
    CanvasNode,
    CanvasEdge,
    Diagram,
    ChatMessage,
    CanvasConfig,
    CanvasContextValue,
    DiagramContextValue,
    InfiniteCanvasProps,
    ViewSelectorProps,
    ToolbarProps,
    DiagramPanelProps,
    ChatInterfaceProps,
    ArchVisionCanvasProps,
    BrainCraftCanvasProps,
} from './types';

// Hooks
export { useCanvas } from './hooks/useCanvas';
export { useDiagram } from './hooks/useDiagram';

// Services
export { canvasService } from './services/canvasService';
export { diagramService } from './services/diagramService';
