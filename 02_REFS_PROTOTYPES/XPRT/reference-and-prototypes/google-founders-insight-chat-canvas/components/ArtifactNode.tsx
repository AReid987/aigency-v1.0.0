
import React, { memo } from 'react';
import { Handle, Position, NodeProps } from '@xyflow/react';
// Fix: Import CustomNode type
import type { ArtifactNodeData, CustomNode } from '../types';
import DocumentTextIcon from './icons/DocumentTextIcon';

// Fix: NodeProps generic should be the full Node type (CustomNode), not just the data type (ArtifactNodeData).
const ArtifactNode: React.FC<NodeProps<CustomNode>> = ({ data, selected }) => {
  const IconComponent = data.icon || DocumentTextIcon;

  const isWelcomeNode = data.type === 'WelcomeMessage';

  const nodeBaseClasses = "p-3 rounded-lg shadow-md w-64";
  const welcomeNodeClasses = "bg-pink-600 border border-pink-400 text-white";
  const defaultNodeClasses = "bg-slate-700 border border-slate-600 text-white";
  const selectedClasses = selected ? 'ring-2 ring-offset-2 ring-offset-slate-900 ring-pink-500' : '';


  return (
    <div 
      className={`
        ${nodeBaseClasses}
        ${isWelcomeNode ? welcomeNodeClasses : defaultNodeClasses}
        ${selectedClasses}
      `}
      aria-label={`Artifact: ${data.label}, Type: ${data.type}`}
    >
      <Handle type="target" position={Position.Left} className="!bg-teal-500 !w-3 !h-3" />
      <div className="flex items-center mb-2">
        <IconComponent className={`w-5 h-5 mr-2 ${isWelcomeNode ? 'text-white' : 'text-pink-400'}`} />
        <div className="font-bold text-sm truncate" title={data.label}>{data.label}</div>
      </div>
      <div className={`text-xs ${isWelcomeNode ? 'text-pink-100' : 'text-slate-300'} break-words h-16 overflow-y-auto pr-1 scrollbar-thin scrollbar-thumb-slate-500 scrollbar-track-slate-700`}>
        {data.contentSummary || "No summary available."}
      </div>
       <div className={`text-xxs ${isWelcomeNode ? 'text-pink-200' : 'text-pink-400'} mt-1 uppercase`}>{data.type}</div>
      <Handle type="source" position={Position.Right} className="!bg-sky-500 !w-3 !h-3" />
    </div>
  );
};

export default memo(ArtifactNode);