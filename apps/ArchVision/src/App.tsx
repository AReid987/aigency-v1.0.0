import { useState } from 'react';
import './index.css';
import Canvas2D from './components/Canvas2D';
import Canvas3D from './components/Canvas3D';
import CanvasIso from './components/CanvasIso';
import Toolbar from './components/Toolbar';
import ViewSelector from './components/ViewSelector';

type ViewType = '2d' | '3d' | 'iso';

function App() {
  const [currentView, setCurrentView] = useState<ViewType>('2d');

  const renderCanvas = () => {
    switch (currentView) {
      case '2d':
        return <Canvas2D />;
      case '3d':
        return <Canvas3D />;
      case 'iso':
        return <CanvasIso />;
    }
  };

  return (
    <div className="min-h-screen w-full bg-gray-50">
      <div className="flex h-screen">
        <Toolbar />
        <div className="flex-1 relative">
          {renderCanvas()}
          <ViewSelector currentView={currentView} onViewChange={setCurrentView} />
        </div>
      </div>
    </div>
  );
}

export default App;