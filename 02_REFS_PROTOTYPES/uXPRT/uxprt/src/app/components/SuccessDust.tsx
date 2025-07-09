"use client";

import React, { useEffect, useState } from "react";

interface SuccessDustProps {
  isActive: boolean;
  onAnimationComplete?: () => void;
}

const SuccessDust: React.FC<SuccessDustProps> = ({
  isActive,
  onAnimationComplete,
}) => {
  const [renderParticles, setRenderParticles] = useState(false);

  useEffect(() => {
    if (isActive) {
      setRenderParticles(true);
      const timer = setTimeout(() => {
        setRenderParticles(false); // Remove particles after animation
        if (onAnimationComplete) {
          onAnimationComplete();
        }
      }, 1000); // Corresponds to the longest animation duration

      return () => clearTimeout(timer);
    }
  }, [isActive, onAnimationComplete]);

  if (!renderParticles) {
    return null;
  }

  return (
    <div className='success-dust-container' aria-hidden='true'>
      <div className='success-dust-particle p1'></div>
      <div className='success-dust-particle p2'></div>
      <div className='success-dust-particle p3'></div>
      <div className='success-dust-particle p4'></div>
      <div className='success-dust-particle p5'></div>
      <div className='success-dust-particle p6'></div>
      <div className='success-dust-particle p7'></div>
      <div className='success-dust-particle p8'></div>
      <div className='success-dust-particle p9'></div>
      <div className='success-dust-particle p10'></div>
    </div>
  );
};

export default SuccessDust;
