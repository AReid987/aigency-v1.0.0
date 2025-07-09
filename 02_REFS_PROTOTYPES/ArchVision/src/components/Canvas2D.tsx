import ReactFlow, { Background, Controls } from 'reactflow';
import 'reactflow/dist/style.css';

const Canvas2D = () => {
  return (
    <div className="w-full h-full">
      <ReactFlow>
        <Background />
        <Controls />
      </ReactFlow>
    </div>
  );
};

export default Canvas2D;