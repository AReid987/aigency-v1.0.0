"use client";

import { useState, ReactNode, createContext, useContext } from "react";
import Header from "./Header"; // Assuming Header is in the same directory
import LoginForm from "./LoginForm";
import { Button } from "@/components/ui/button";

interface OverlayContextType {
  showLoginOverlay: boolean;
  toggleLoginOverlay: () => void;
}

const OverlayContext = createContext<OverlayContextType | undefined>(undefined);

export const useOverlay = () => {
  const context = useContext(OverlayContext);
  if (context === undefined) {
    throw new Error("useOverlay must be used within an OverlayProvider");
  }
  return context;
};

interface OverlayProviderProps {
  children: ReactNode;
}

export default function OverlayProvider({ children }: OverlayProviderProps) {
  const [showLoginOverlay, setShowLoginOverlay] = useState(false);

  const toggleLoginOverlay = () => {
    setShowLoginOverlay(!showLoginOverlay);
  };

  return (
    <OverlayContext.Provider value={{ showLoginOverlay, toggleLoginOverlay }}>
      <Header onLoginClick={toggleLoginOverlay} />
      {children}
      {showLoginOverlay && (
        <div className='fixed inset-0 z-20 flex items-center justify-center bg-black/30 backdrop-blur-sm p-4'>
          <div className='relative bg-card/80 backdrop-blur-lg text-card-foreground p-8 rounded-xl shadow-2xl w-full max-w-md border border-border/50'>
            <Button
              variant='ghost'
              size='sm'
              onClick={toggleLoginOverlay}
              className='absolute top-2 right-2 text-muted-foreground hover:text-foreground'
            >
              ✕
            </Button>
            <LoginForm onGoBack={toggleLoginOverlay} />
          </div>
        </div>
      )}
    </OverlayContext.Provider>
  );
}
