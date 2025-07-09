import type { Edge, EdgeTypes } from '@xyflow/react';

export const initialEdges: Edge[] = [
  { id: 'user->frontend', source: 'user', target: 'frontend', animated: true },
  { id: 'frontend->backend', source: 'frontend', target: 'backend', animated: true },
  { id: 'backend->astradb', source: 'backend', target: 'astradb', animated: true },
];

export const edgeTypes = {
  // Add your custom edge types here!
} satisfies EdgeTypes;
