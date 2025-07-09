
import React from 'react';

interface IconProps {
  className?: string;
}

const PaperclipIcon: React.FC<IconProps> = ({ className }) => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className={className || "w-5 h-5"}>
    <path fillRule="evenodd" d="M12.577 4.878a.75.75 0 00-1.06-1.06L4.243 11.092a3.625 3.625 0 005.125 5.125l8.131-8.131a2.125 2.125 0 00-3-3L6.375 13.25a.625.625 0 00.884.884l7.098-7.098.017-.017.017-.017a.75.75 0 00-1.06-1.06l-.017.017-.017.017-7.098 7.098a2.125 2.125 0 01-3-3L11.517 3.818a3.625 3.625 0 015.125 5.125L8.51 17.076a5.125 5.125 0 01-7.247-7.247l7.373-7.373 1.061 1.06L2.263 9.828a3.625 3.625 0 005.125 5.125l8.131-8.131a.625.625 0 00-.884-.884L7.423 13.15l-.017.017-.017.017a.75.75 0 001.06 1.06l.017-.017.017-.017 7.213-7.213z" clipRule="evenodd" />
  </svg>
);
export default PaperclipIcon;
