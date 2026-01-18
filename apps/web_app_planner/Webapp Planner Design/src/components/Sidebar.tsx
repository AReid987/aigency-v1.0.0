import React from 'react';
import { cn } from '@/lib/utils';

interface SidebarProps {
  activeSection: string;
  onSectionChange: (section: string) => void;
  theme: string;
  onThemeToggle: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ activeSection, onSectionChange, theme, onThemeToggle }) => {
  const navItems = [
    { id: 'branding', label: 'Branding', icon: '🎨' },
    { id: 'goals', label: 'Goals & Objectives', icon: '🎯' },
    { id: 'user-stories', label: 'User Stories', icon: '👥' },
    { id: 'features', label: 'Core Features', icon: '⚡' },
    { id: 'wireframes', label: 'Wireframes', icon: '📐' },
    { id: 'atomic-design', label: 'Atomic Design System', icon: '🔬' },
    { id: 'data-points', label: 'Data Points', icon: '💾' }
  ];

  return (
    <aside className="w-72 bg-gray-800 text-gray-100 p-4 space-y-2 flex flex-col fixed inset-y-0 left-0 overflow-y-auto">
      <div className="text-2xl font-semibold text-white mb-6 text-center">
        WebApp Planner
      </div>
      
      <nav className="flex-grow">
        {navItems.map((item) => (
          <button
            key={item.id}
            onClick={() => onSectionChange(item.id)}
            className={cn(
              "sidebar-item flex items-center space-x-3 p-3 rounded-md w-full text-left transition-all duration-300",
              activeSection === item.id
                ? "bg-indigo-600 text-white"
                : "text-gray-400 hover:bg-indigo-600 hover:text-white"
            )}
          >
            <span className="text-xl">{item.icon}</span>
            <span>{item.label}</span>
          </button>
        ))}
      </nav>
      
      <div className="p-4 mt-auto border-t border-gray-700">
        <label className="flex items-center justify-center cursor-pointer">
          <span className="mr-3 text-sm font-medium text-gray-300">Light</span>
          <div className="relative">
            <input
              type="checkbox"
              checked={theme === 'dark'}
              onChange={onThemeToggle}
              className="sr-only peer"
            />
            <div className="w-10 h-6 bg-gray-600 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-500"></div>
          </div>
          <span className="ml-3 text-sm font-medium text-gray-300">Dark</span>
        </label>
      </div>
    </aside>
  );
};

export default Sidebar;