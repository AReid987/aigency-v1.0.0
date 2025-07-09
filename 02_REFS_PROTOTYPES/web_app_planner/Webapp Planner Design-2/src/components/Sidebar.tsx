import React from 'react';
import { cn } from '@/lib/utils';
import { Palette, Target, Users, Zap, Layout, Atom, Database } from 'lucide-react';

interface SidebarProps {
  activeSection: string;
  onSectionChange: (section: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ activeSection, onSectionChange }) => {
  const navItems = [
    { id: 'branding', label: 'Branding', icon: Palette },
    { id: 'goals', label: 'Goals & Objectives', icon: Target },
    { id: 'user-stories', label: 'User Stories', icon: Users },
    { id: 'features', label: 'Core Features', icon: Zap },
    { id: 'wireframes', label: 'Wireframes', icon: Layout },
    { id: 'atomic-design', label: 'Atomic Design System', icon: Atom },
    { id: 'data-points', label: 'Data Points', icon: Database }
  ];

  return (
    <aside className="w-72 bg-card border-r border-border p-4 space-y-2 flex flex-col fixed inset-y-0 left-0 top-16 overflow-y-auto">
      <nav className="flex-grow space-y-1 pt-4">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.id}
              onClick={() => onSectionChange(item.id)}
              className={cn(
                "flex items-center space-x-3 p-3 rounded-lg w-full text-left transition-all duration-200",
                activeSection === item.id
                  ? "bg-primary text-primary-foreground shadow-sm"
                  : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
              )}
            >
              <Icon className="h-5 w-5" />
              <span className="font-medium">{item.label}</span>
            </button>
          );
        })}
      </nav>
    </aside>
  );
};

export default Sidebar;