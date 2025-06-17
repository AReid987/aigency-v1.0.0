import { useState, useCallback } from 'react';
import { DiagramData, DiagramType, ChatMessage } from '../types';
import { diagramService } from '../services/diagramService';

export function useDiagram() {
    const [currentDiagram, setCurrentDiagram] = useState<DiagramData | null>(null);
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [isGenerating, setIsGenerating] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const generateDiagram = useCallback(async (prompt: string, type?: DiagramType) => {
        try {
            setIsGenerating(true);
            setError(null);

            const diagram = await diagramService.generateFromPrompt(prompt, type);
            setCurrentDiagram(diagram);

            return diagram;
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Failed to generate diagram';
            setError(errorMessage);
            throw err;
        } finally {
            setIsGenerating(false);
        }
    }, []);

    const updateDiagram = useCallback(async (code: string, type: DiagramType) => {
        try {
            setIsGenerating(true);
            setError(null);

            const diagram = await diagramService.validateAndFormat(code, type);
            setCurrentDiagram(diagram);

            return diagram;
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Failed to update diagram';
            setError(errorMessage);
            throw err;
        } finally {
            setIsGenerating(false);
        }
    }, []);

    const addMessage = useCallback((message: Omit<ChatMessage, 'id' | 'timestamp'>) => {
        const newMessage: ChatMessage = {
            ...message,
            id: Date.now().toString(),
            timestamp: new Date(),
        };
        setMessages(prev => [...prev, newMessage]);
        return newMessage;
    }, []);

    const clearMessages = useCallback(() => {
        setMessages([]);
    }, []);

    const clearDiagram = useCallback(() => {
        setCurrentDiagram(null);
        setError(null);
    }, []);

    const exportDiagram = useCallback(async (format: 'svg' | 'png' | 'pdf' = 'svg') => {
        if (!currentDiagram) {
            throw new Error('No diagram to export');
        }

        return await diagramService.exportDiagram(currentDiagram, format);
    }, [currentDiagram]);

    return {
        // State
        currentDiagram,
        messages,
        isGenerating,
        error,

        // Actions
        generateDiagram,
        updateDiagram,
        addMessage,
        clearMessages,
        clearDiagram,
        exportDiagram,
        setCurrentDiagram,
    };
}
