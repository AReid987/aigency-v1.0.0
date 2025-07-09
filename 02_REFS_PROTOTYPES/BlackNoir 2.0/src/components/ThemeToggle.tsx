import React from "react";
import { Sun, Moon } from "lucide-react";
interface ThemeToggleProps {
  isDark: boolean;
  toggle: () => void;
}
export const ThemeToggle = ({
  isDark,
  toggle
}: ThemeToggleProps) => {
  return <button onClick={toggle} className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors" aria-label="Toggle theme">
      {isDark ? <Sun className="h-5 w-5 text-gray-600 dark:text-gray-400" /> : <Moon className="h-5 w-5 text-gray-600 dark:text-gray-400" />}
    </button>;
};