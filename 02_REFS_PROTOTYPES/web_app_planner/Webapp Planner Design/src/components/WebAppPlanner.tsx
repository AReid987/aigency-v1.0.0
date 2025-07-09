import React, { useState, useEffect } from 'react';
import { useLocalStorage } from '@/hooks/useLocalStorage';
import Sidebar from './Sidebar';
import BrandingSection from './sections/BrandingSection';
import GoalsSection from './sections/GoalsSection';
import UserStoriesSection from './sections/UserStoriesSection';
import FeaturesSection from './sections/FeaturesSection';
import WireframesSection from './sections/WireframesSection';
import AtomicDesignSection from './sections/AtomicDesignSection';
import DataPointsSection from './sections/DataPointsSection';

interface AppData {
  branding: {
    mission: string;
    values: string[];
    audience: string;
    personality: string;
    moodboard: string;
  };
  goals: {
    problem: string;
    audience: string;
    mvp: string;
    outcomes: string;
  };
  userStories: Array<{
    id: string;
    userType: string;
    action: string;
    benefit: string;
  }>;
  features: Array<{
    id: string;
    name: string;
  }>;
  wireframes: Array<{
    id: string;
    screenName: string;
    keyElements: string;
    interactions: string;
  }>;
  atomicDesign: {
    colorPrimary: string;
    colorSecondary: string;
    colorAccent: string;
    neutralPalette: string;
    colorSuccess: string;
    colorError: string;
    colorWarning: string;
    colorInfo: string;
    fontHeading: string;
    fontBody: string;
    iconography: string;
    typeScale: string;
    colorScale: string;
    molecules: string;
    organisms: string;
    templates: string;
    pages: string;
  };
  dataPoints: Array<{
    id: string;
    name: string;
    type: string;
    description: string;
  }>;
}

const defaultData: AppData = {
  branding: {
    mission: '',
    values: [],
    audience: '',
    personality: '',
    moodboard: ''
  },
  goals: {
    problem: '',
    audience: '',
    mvp: '',
    outcomes: ''
  },
  userStories: [],
  features: [],
  wireframes: [],
  atomicDesign: {
    colorPrimary: '',
    colorSecondary: '',
    colorAccent: '',
    neutralPalette: '',
    colorSuccess: '',
    colorError: '',
    colorWarning: '',
    colorInfo: '',
    fontHeading: '',
    fontBody: '',
    iconography: '',
    typeScale: '',
    colorScale: '',
    molecules: '',
    organisms: '',
    templates: '',
    pages: ''
  },
  dataPoints: []
};

const WebAppPlanner: React.FC = () => {
  const [activeSection, setActiveSection] = useState('branding');
  const [theme, setTheme] = useLocalStorage('theme', 'dark');
  const [appData, setAppData] = useLocalStorage<AppData>('webapp-planner-data', defaultData);

  useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [theme]);

  const handleThemeToggle = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  const updateBranding = (branding: AppData['branding']) => {
    setAppData(prev => ({ ...prev, branding }));
  };

  const updateGoals = (goals: AppData['goals']) => {
    setAppData(prev => ({ ...prev, goals }));
  };

  const updateUserStories = (userStories: AppData['userStories']) => {
    setAppData(prev => ({ ...prev, userStories }));
  };

  const updateFeatures = (features: AppData['features']) => {
    setAppData(prev => ({ ...prev, features }));
  };

  const updateWireframes = (wireframes: AppData['wireframes']) => {
    setAppData(prev => ({ ...prev, wireframes }));
  };

  const updateAtomicDesign = (atomicDesign: AppData['atomicDesign']) => {
    setAppData(prev => ({ ...prev, atomicDesign }));
  };

  const updateDataPoints = (dataPoints: AppData['dataPoints']) => {
    setAppData(prev => ({ ...prev, dataPoints }));
  };

  const renderSection = () => {
    switch (activeSection) {
      case 'branding':
        return <BrandingSection data={appData.branding} onSave={updateBranding} />;
      case 'goals':
        return <GoalsSection data={appData.goals} onSave={updateGoals} />;
      case 'user-stories':
        return <UserStoriesSection data={appData.userStories} onSave={updateUserStories} />;
      case 'features':
        return <FeaturesSection data={appData.features} onSave={updateFeatures} />;
      case 'wireframes':
        return <WireframesSection data={appData.wireframes} onSave={updateWireframes} />;
      case 'atomic-design':
        return <AtomicDesignSection data={appData.atomicDesign} onSave={updateAtomicDesign} />;
      case 'data-points':
        return <DataPointsSection data={appData.dataPoints} onSave={updateDataPoints} />;
      default:
        return <BrandingSection data={appData.branding} onSave={updateBranding} />;
    }
  };

  return (
    <div className="flex h-screen overflow-hidden bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
      <Sidebar
        activeSection={activeSection}
        onSectionChange={setActiveSection}
        theme={theme}
        onThemeToggle={handleThemeToggle}
      />
      <main className="flex-1 ml-72 p-6 sm:p-8 overflow-y-auto">
        {renderSection()}
      </main>
    </div>
  );
};

export default WebAppPlanner;