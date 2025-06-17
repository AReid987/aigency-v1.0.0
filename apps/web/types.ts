// Backlog Structure Types
interface Task {
  id: string;
  title: string;
  description?: string;
  status: 'todo' | 'in-progress' | 'done';
  complexity: number;
  epicId: string;
  createdAt: string;
  updatedAt: string;
}

interface Epic {
  id: string;
  title: string;
  description?: string;
  complexity: number;
  tasks: Task[];
  createdAt: string;
  updatedAt: string;
}

interface Backlog {
  epics: Epic[];
  totalComplexity: number;
  progress: number;
}

// Kanban View Types
interface KanbanColumn {
  id: string;
  title: string;
  taskIds: string[];
}

interface KanbanView {
  columns: KanbanColumn[];
  columnOrder: string[];
}

// Document Generation Types
export type DocumentType = 'PRD' | 'FRD' | 'ERD' | 'DRD';

export interface DocumentSection {
  title: string;
  content: string;
  order: number;
}

export interface DocumentMetadata {
  id: string;
  type: DocumentType;
  title: string;
  description?: string;
  createdAt: string;
  updatedAt: string;
  version: number;
}

export interface Document {
  metadata: DocumentMetadata;
  sections: DocumentSection[];
}

export interface DocumentState {
  currentDocumentId?: string;
  documents: Document[];
  isLoading: boolean;
  error?: string;
}