import { Layout2, Boxes, Box } from 'lucide-react';

interface ViewSelectorProps {
  currentView: '2d' | '3d' | 'iso';
  onViewChange: (view: '2d' | '3d' | 'iso') => void;
}

const ViewSelector = ({ currentView, onViewChange }: ViewSelectorProps) => {
  return (
    <div className="absolute top-4 right-4 bg-white rounded-lg shadow-lg p-1 flex gap-1">
      <button
        onClick={() => onViewChange('2d')}
        className={`p-2 rounded ${
          currentView === '2d' ? 'bg-blue-100 text-blue-600' : 'hover:bg-gray-100'
        }`}
      >
        <Layout2 className="w-5 h-5" />
      </button>
      <button
        onClick={() => onViewChange('3d')}
        className={`p-2 rounded ${
          currentView === '3d' ? 'bg-blue-100 text-blue-600' : 'hover:bg-gray-100'
        }`}
      >
        <Boxes className="w-5 h-5" />
      </button>
      <button
        onClick={() => onViewChange('iso')}
        className={`p-2 rounded ${
          currentView === 'iso' ? 'bg-blue-100 text-blue-600' : 'hover:bg-gray-100'
        }`}
      >
        <Box className="w-5 h-5" />
      </button>
    </div>
  );
};

export default ViewSelector;