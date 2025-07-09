
import React from 'react';

interface IconProps {
  className?: string;
}

const MicIcon: React.FC<IconProps> = ({ className }) => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className={className || "w-5 h-5"}>
    <path d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4z" />
    <path d="M5.5 9.5A.5.5 0 016 9h8a.5.5 0 010 1H6a.5.5 0 01-.5-.5z" />
    <path d="M9 13.5a.5.5 0 01.5-.5h1a.5.5 0 01.5.5v1.148A4.503 4.503 0 0015.5 13A.5.5 0 0116 13v1a.5.5 0 01-.5.5 5.502 5.502 0 01-11 0V13a.5.5 0 01.5-.5 4.503 4.503 0 004.5 1.648V13.5z" />
  </svg>
);
export default MicIcon;
