
import React from 'react';

interface FileNode {
  name: string;
  type: 'file' | 'directory';
  children?: FileNode[];
}

interface FileTreeProps {
  fileTree: FileNode;
}

const FileTree: React.FC<FileTreeProps> = ({ fileTree }) => {
  const renderNode = (node: FileNode, level = 0) => (
    <div key={node.name} style={{ paddingLeft: `${level * 20}px` }}>
      <span>{node.type === 'directory' ? '??' : '??'}</span>
      <span>{node.name}</span>
      {node.children && (
        <div>
          {node.children.map((child) => renderNode(child, level + 1))}
        </div>
      )}
    </div>
  );

  return <div>{renderNode(fileTree)}</div>;
};

export default FileTree;
