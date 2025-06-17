import mermaid from 'mermaid';
import { DiagramData, DiagramType } from '../types';

interface DiagramServiceConfig {
    theme?: 'default' | 'forest' | 'dark' | 'neutral';
    securityLevel?: 'strict' | 'loose';
    logLevel?: 1 | 2 | 3 | 4 | 5;
}

class DiagramService {
    private config: DiagramServiceConfig;

    constructor(config: DiagramServiceConfig = {}) {
        this.config = {
            theme: 'default',
            securityLevel: 'strict',
            logLevel: 3,
            ...config,
        };

        this.initializeMermaid();
    }

    private initializeMermaid() {
        mermaid.initialize({
            startOnLoad: false,
            theme: this.config.theme,
            securityLevel: this.config.securityLevel,
            logLevel: this.config.logLevel,
        });
    }

    async generateFromPrompt(prompt: string, type: DiagramType = 'flowchart'): Promise<DiagramData> {
        try {
            // TODO: Integrate with AI service for diagram generation
            // For now, return a simple example diagram
            const code = this.getExampleDiagram(type);
            return this.validateAndFormat(code, type);
        } catch (error) {
            throw new Error(`Failed to generate diagram: ${error instanceof Error ? error.message : 'Unknown error'}`);
        }
    }

    async validateAndFormat(code: string, type: DiagramType): Promise<DiagramData> {
        try {
            // Clean the code
            const cleanCode = this.cleanMermaidCode(code);

            // Validate the code
            await mermaid.parse(cleanCode);

            return {
                id: `diagram_${Date.now()}`,
                code: cleanCode,
                type,
                title: this.extractTitle(cleanCode),
                createdAt: new Date(),
                updatedAt: new Date(),
            };
        } catch (error) {
            throw new Error(`Invalid diagram code: ${error instanceof Error ? error.message : 'Unknown error'}`);
        }
    }

    async exportDiagram(diagram: DiagramData, format: 'svg' | 'png' | 'pdf' = 'svg'): Promise<string> {
        try {
            const { code } = diagram;

            // For now, only support SVG export
            if (format !== 'svg') {
                throw new Error(`Export format '${format}' not supported yet`);
            }

            // Use mermaid's render method
            const { svg } = await mermaid.render('diagram', code);
            return svg;
        } catch (error) {
            throw new Error(`Failed to export diagram: ${error instanceof Error ? error.message : 'Unknown error'}`);
        }
    }

    private cleanMermaidCode(code: string): string {
        // Remove markdown code block syntax if present
        return code.replace(/^\`\`\`mermaid\n|\`\`\`$/g, '').trim();
    }

    private extractTitle(code: string): string {
        // Try to extract title from the first line comment if present
        const titleMatch = code.match(/^%%(.*?)%%/);
        return titleMatch && titleMatch[1] ? titleMatch[1].trim() : 'Untitled Diagram';
    }

    private getExampleDiagram(type: DiagramType): string {
        switch (type) {
            case 'flowchart':
                return `
          flowchart LR
            A[Start] --> B{Decision}
            B -->|Yes| C[Action]
            B -->|No| D[Skip]
            C --> E[End]
            D --> E
        `;
            case 'sequence':
                return `
          sequenceDiagram
            participant User
            participant System
            User->>System: Request
            System-->>User: Response
        `;
            case 'class':
                return `
          classDiagram
            class Example {
              +String data
              +process()
            }
        `;
            default:
                return `
          flowchart LR
            A[Default] --> B[Example]
        `;
        }
    }
}

// Export singleton instance
export const diagramService = new DiagramService();
