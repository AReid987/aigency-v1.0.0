import React from 'react';
import { User } from 'lucide-react';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';

interface HeaderProps {
  theme: string;
  onThemeToggle: () => void;
}

const Header: React.FC<HeaderProps> = ({ theme, onThemeToggle }) => {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between px-4">
        <div className="flex items-center space-x-3">
          <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center">
            <span className="text-primary-foreground font-bold text-sm">WP</span>
          </div>
          <h1 className="text-xl font-semibold text-foreground">WebApp Planner</h1>
        </div>
        
        <div className="flex items-center space-x-4">
          <label htmlFor="theme-toggle" className="flex items-center cursor-pointer">
            <span className="mr-2 text-sm text-muted-foreground">Light</span>
            <div className="relative">
              <input
                type="checkbox"
                id="theme-toggle"
                className="sr-only peer"
                checked={theme === 'dark'}
                onChange={onThemeToggle}
              />
              <div className="w-11 h-6 bg-muted rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
            </div>
            <span className="ml-2 text-sm text-muted-foreground">Dark</span>
          </label>
          
          <div className="flex items-center space-x-2">
            <Avatar className="h-8 w-8">
              <AvatarFallback className="bg-primary text-primary-foreground">
                <User className="h-4 w-4" />
              </AvatarFallback>
            </Avatar>
            <div className="flex items-center space-x-1">
              <div className="h-2 w-2 rounded-full bg-jade-9"></div>
              <span className="text-sm text-muted-foreground">Online</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;