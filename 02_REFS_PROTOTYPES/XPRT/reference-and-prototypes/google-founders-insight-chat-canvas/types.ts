
import { Node, Edge } from '@xyflow/react';

export enum MessageSender {
  USER = 'user',
  AI = 'ai',
  SYSTEM = 'system',
}

export interface ChatMessage {
  id: string;
  text: string;
  sender: MessageSender;
  timestamp: Date;
  imageUrl?: string; // For images sent by user or AI
  fileInfo?: { name: string; type: string }; // For other files
}

export interface ArtifactNodeData {
  label: string;
  type: string; // e.g., 'LeanCanvas', 'MarketResearch', 'UserProfile'
  contentSummary: string; // A brief summary or key points for the node
  fullContent?: string; // Full artifact content, optional for node display
  icon?: React.ReactNode;
  // Fix: Add index signature to satisfy Record<string, unknown> constraint for Node data
  [key: string]: any;
}

export type CustomNode = Node<ArtifactNodeData>;

export interface UploadedFile {
  name: string;
  type: string;
  base64Data: string;
}