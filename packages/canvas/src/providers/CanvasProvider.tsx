import React, { createContext, useReducer, useContext, ReactNode } from "react";
import {
  CanvasState,
  CanvasConfig,
  CanvasMode,
  ViewType,
  CanvasNode,
  CanvasEdge,
} from "../types";

interface CanvasContextType {
  state: CanvasState;
  config: CanvasConfig;
  dispatch: React.Dispatch<CanvasAction>;
}

type CanvasAction =
  | { type: "SET_MODE"; payload: CanvasMode }
  | { type: "SET_VIEW"; payload: ViewType }
  | { type: "SET_NODES"; payload: CanvasNode[] }
  | { type: "SET_EDGES"; payload: CanvasEdge[] }
  | { type: "SELECT_NODES"; payload: string[] }
  | { type: "SELECT_EDGES"; payload: string[] }
  | { type: "SET_LOADING"; payload: boolean }
  | { type: "SET_ERROR"; payload: string | null };

const initialState: CanvasState = {
  currentView: "2d",
  currentMode: "archvision",
  mode: "archvision",
  nodes: [],
  edges: [],
  config: {
    enableAI: true,
    enableCollaboration: true,
    enableIsometric: true,
    theme: "light",
    defaultView: "2d",
    defaultMode: "hybrid",
  },
  selectedNodes: [],
  selectedEdges: [],
  isLoading: false,
  error: null,
};

const defaultConfig: CanvasConfig = {
  enableAI: true,
  enableCollaboration: true,
  enableIsometric: true,
  theme: "light",
  defaultView: "2d",
  defaultMode: "archvision",
};

const CanvasContext = createContext<CanvasContextType | undefined>(undefined);

function canvasReducer(state: CanvasState, action: CanvasAction): CanvasState {
  switch (action.type) {
    case "SET_MODE":
      return { ...state, mode: action.payload };
    case "SET_VIEW":
      return { ...state, currentView: action.payload };
    case "SET_NODES":
      return { ...state, nodes: action.payload };
    case "SET_EDGES":
      return { ...state, edges: action.payload };
    case "SELECT_NODES":
      return { ...state, selectedNodes: action.payload };
    case "SELECT_EDGES":
      return { ...state, selectedEdges: action.payload };
    case "SET_LOADING":
      return { ...state, isLoading: action.payload };
    case "SET_ERROR":
      return { ...state, error: action.payload };
    default:
      return state;
  }
}

interface CanvasProviderProps {
  children: ReactNode;
  config?: Partial<CanvasConfig>;
}

export function CanvasProvider({ children, config = {} }: CanvasProviderProps) {
  const [state, dispatch] = useReducer(canvasReducer, initialState);
  const mergedConfig = { ...defaultConfig, ...config };

  return (
    <CanvasContext.Provider
      value={{ state, config: mergedConfig, dispatch }}
      data-oid="ps8..05"
    >
      {children}
    </CanvasContext.Provider>
  );
}

export function useCanvasContext() {
  const context = useContext(CanvasContext);
  if (context === undefined) {
    throw new Error("useCanvasContext must be used within a CanvasProvider");
  }
  return context;
}

export default CanvasProvider;
