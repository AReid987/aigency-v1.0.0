
import React from 'react';

export function ParticleCloud3D() {
  const particles = Array.from({ length: 50 }, (_, i) => ({
    id: i,
    x: Math.random() * 100,
    y: Math.random() * 100,
    size: Math.random() * 4 + 1,
    animationDelay: Math.random() * 2,
    animationDuration: Math.random() * 3 + 2,
  }));

  return (
    <div className="w-full h-64 md:h-80 rounded-2xl overflow-hidden bg-gradient-to-br from-primary/10 to-accent/20 border border-border/50 relative">
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-primary/5 to-accent/10" />
      
      {particles.map((particle) => (
        <div
          key={particle.id}
          className="absolute rounded-full bg-primary/60 animate-pulse"
          style={{
            left: `${particle.x}%`,
            top: `${particle.y}%`,
            width: `${particle.size}px`,
            height: `${particle.size}px`,
            animationDelay: `${particle.animationDelay}s`,
            animationDuration: `${particle.animationDuration}s`,
            boxShadow: '0 0 6px rgba(13, 148, 136, 0.6)',
          }}
        />
      ))}
      
      {/* Floating orbs */}
      <div className="absolute top-1/4 left-1/4 w-16 h-16 rounded-full bg-gradient-to-r from-primary/30 to-accent/30 animate-bounce" style={{ animationDelay: '0.5s', animationDuration: '3s' }} />
      <div className="absolute top-3/4 right-1/4 w-12 h-12 rounded-full bg-gradient-to-r from-accent/40 to-primary/40 animate-bounce" style={{ animationDelay: '1s', animationDuration: '2.5s' }} />
      <div className="absolute top-1/2 left-1/2 w-8 h-8 rounded-full bg-gradient-to-r from-primary/50 to-accent/50 animate-bounce" style={{ animationDelay: '1.5s', animationDuration: '2s' }} />
      
      {/* Central glow effect */}
      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-32 h-32 rounded-full bg-primary/20 blur-xl animate-pulse" />
    </div>
  );
}
