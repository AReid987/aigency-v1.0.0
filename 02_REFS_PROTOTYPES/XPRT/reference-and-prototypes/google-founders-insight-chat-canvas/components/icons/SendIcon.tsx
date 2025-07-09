
import React from 'react';

interface IconProps {
  className?: string;
}

const SendIcon: React.FC<IconProps> = ({ className }) => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className={className || "w-5 h-5"}>
    <path d="M3.105 3.105a.5.5 0 01.815-.093L19.48 15.09a.5.5 0 01-.585.793L15.09 19.48a.5.5 0 01-.815.093L3.105 4.808a.5.5 0 01.093-.815zM4.994 4.994L15.09 19.48l-3.708-3.708a.5.5 0 01.093-.815L19.48 15.09l-4.386-4.386a.5.5 0 01-.793.585L4.909 3.105a.5.5 0 01.085.815z" />
  </svg>
);
export default SendIcon;
