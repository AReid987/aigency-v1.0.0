import { useCallback } from 'react';
import { useCanvasContext } from '../providers/CanvasProvider';
import { CanvasMode, ViewType, CanvasNode, CanvasEdge } from '../types';

export function useCanvas() {
    const { state, dispatch } = useCanvasContext();

    const setMode = useCallback((mode: CanvasMode) => {
        dispatch({ type: 'SET_MODE', payload: mode });
    }, [dispatch]);

    const setView = useCallback((view: ViewType) => {
        dispatch({ type: 'SET_VIEW', payload: view });
    }, [dispatch]);

    const setNodes = useCallback((nodes: CanvasNode[]) => {
        dispatch({ type: 'SET_NODES', payload: nodes });
    }, [dispatch]);

    const setEdges = useCallback((edges: CanvasEdge[]) => {
        dispatch({ type: 'SET_EDGES', payload: edges });
    }, [dispatch]);

    const selectNodes = useCallback((nodeIds: string[]) => {
        dispatch({ type: 'SELECT_NODES', payload: nodeIds });
    }, [dispatch]);

    const selectEdges = useCallback((edgeIds: string[]) => {
        dispatch({ type: 'SELECT_EDGES', payload: edgeIds });
    }, [dispatch]);

    const setLoading = useCallback((loading: boolean) => {
        dispatch({ type: 'SET_LOADING', payload: loading });
    }, [dispatch]);

    const setError = useCallback((error: string | null) => {
        dispatch({ type: 'SET_ERROR', payload: error });
    }, [dispatch]);

    const addNode = useCallback((node: CanvasNode) => {
        setNodes([...state.nodes, node]);
    }, [state.nodes, setNodes]);

    const removeNode = useCallback((nodeId: string) => {
        setNodes(state.nodes.filter(node => node.id !== nodeId));
        setEdges(state.edges.filter(edge => edge.source !== nodeId && edge.target !== nodeId));
    }, [state.nodes, state.edges, setNodes, setEdges]);

    const addEdge = useCallback((edge: CanvasEdge) => {
        setEdges([...state.edges, edge]);
    }, [state.edges, setEdges]);

    const removeEdge = useCallback((edgeId: string) => {
        setEdges(state.edges.filter(edge => edge.id !== edgeId));
    }, [state.edges, setEdges]);

    const clearCanvas = useCallback(() => {
        setNodes([]);
        setEdges([]);
        selectNodes([]);
        selectEdges([]);
    }, [setNodes, setEdges, selectNodes, selectEdges]);

    return {
        // State
        ...state,

        // Actions
        setMode,
        setView,
        setNodes,
        setEdges,
        selectNodes,
        selectEdges,
        setLoading,
        setError,
        addNode,
        removeNode,
        addEdge,
        removeEdge,
        clearCanvas,
    };
}
