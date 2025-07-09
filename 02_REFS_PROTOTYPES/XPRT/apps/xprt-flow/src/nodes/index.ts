import type { NodeTypes } from '@xyflow/react';

import { PositionLoggerNode } from './PositionLoggerNode';
import { AppNode } from './types';

export const initialNodes: AppNode[] = [
  { id: 'user', position: { x: 0, y: -100 }, data: { label: 'User' } },
  { id: 'frontend', position: { x: 100, y: 0 }, data: { label: 'Frontend' } },
  { id: 'backend', position: { x: 0, y: 100 }, data: { label: 'Backend' } },
  { id: 'astradb', position: { x: 200, y: 100 }, data: { label: 'AstraDB' } },
];

export const nodeTypes = {
  // Add any of your custom nodes here!
} satisfies NodeTypes;
