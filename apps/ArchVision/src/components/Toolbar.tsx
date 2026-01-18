import { Square, Cube, Box, Circle, Line } from 'lucide-react';

const Toolbar = () => {
  return (
    <div className="h-full w-16 bg-white border-r border-gray-200 flex flex-col items-center py-4 gap-4">
      <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
        <Square className="w-6 h-6 text-gray-600" />
      </button>
      <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
        <Circle className="w-6 h-6 text-gray-600" />
      </button>
      <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
        <Line className="w-6 h-6 text-gray-600" />
      </button>
      <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
        <Cube className="w-6 h-6 text-gray-600" />
      </button>
      <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
        <Box className="w-6 h-6 text-gray-600" />
      </button>
    </div>
  );
};

export default Toolbar;