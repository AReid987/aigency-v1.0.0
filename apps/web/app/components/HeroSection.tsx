"use client";

import { useEffect, useRef } from 'react';

// Define Particle interface for type safety
interface Particle {
  x: number;
  y: number;
  radius: number;
  speed: number;
  angle: number;
  color: string;
}

export function HeroSection() {
  // Add HTMLCanvasElement type to the ref
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (typeof window === 'undefined' || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');

    // Ensure context exists before proceeding
    if (!ctx) return;

    const width = window.innerWidth;
    const height = window.innerHeight;

    // Set canvas dimensions
    canvas.width = width;
    canvas.height = height;

    // Explicitly type particles as Particle[]
    const particles: Particle[] = [];

    // Create particles for background animation
    for (let i = 0; i < 100; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        radius: Math.random() * 2 + 1,
        speed: Math.random() * 0.5 + 0.1,
        angle: Math.random() * Math.PI * 2,
        color: `rgba(14, 165, 233, ${Math.random() * 0.3 + 0.1})`
      });
    }

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);
      ctx.clearRect(0, 0, width, height);

      // Draw particles
      particles.forEach(p => {
        p.x += Math.cos(p.angle) * p.speed;
        p.y += Math.sin(p.angle) * p.speed;

        // Boundary check
        if (p.x < 0) p.x = width;
        if (p.x > width) p.x = 0;
        if (p.y < 0) p.y = height;
        if (p.y > height) p.y = 0;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.fill();
      });
    };

    animate();
  }, []);

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden px-6 py-20 md:py-32">
      {/* Animated background canvas */}
      <canvas
        ref={canvasRef}
        className="absolute inset-0 w-full h-full"
        style={{
          background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%)'
        }}
      />

      {/* Content overlay */}
      <div className="relative z-10 max-w-6xl mx-auto text-center px-4">
        <div className="inline-flex items-center px-4 py-2 rounded-full bg-teal-500/10 border border-teal-500/20 mb-8 animate-pulse">
          <span className="text-teal-400 text-sm font-medium tracking-wider">
            ✨ AI-NATIVE WORKFLOWS
          </span>
        </div>

        <h1 className="text-4xl md:text-7xl font-bold text-white mb-6 leading-tight">
          Transform Your Workflow with <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-blue-500">
            AI Agent Teams
          </span>
        </h1>

        <p className="text-xl md:text-2xl text-slate-300 mb-8 max-w-3xl mx-auto">
          Aigency connects you with specialized AI agents that collaborate to solve complex tasks,
          accelerate development, and unlock new possibilities.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
          <button className="bg-gradient-to-r from-teal-500 to-blue-600 hover:from-teal-600 hover:to-blue-700 text-white px-8 py-4 rounded-lg font-semibold text-lg transition-all transform hover:scale-105 min-w-[200px]">
            Get Started
          </button>
          <button className="bg-transparent border-2 border-slate-600 hover:border-slate-500 text-slate-300 hover:text-white px-8 py-4 rounded-lg font-semibold text-lg transition-colors min-w-[200px]">
            View Demo
          </button>
        </div>

        {/* AI Agent Visualization */}
        <div className="relative mx-auto max-w-4xl h-64 md:h-96 flex items-center justify-center">
          <div className="absolute w-24 h-24 md:w-32 md:h-32 rounded-full bg-gradient-to-r from-teal-500 to-blue-500 opacity-80 animate-pulse"></div>
          <div className="absolute w-16 h-16 md:w-24 md:h-24 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 opacity-80 top-10 left-1/4 animate-ping animate-delay-1000"></div>
          <div className="absolute w-20 h-20 md:w-28 md:h-28 rounded-full bg-gradient-to-r from-indigo-500 to-blue-400 opacity-80 top-20 right-1/4 animate-pulse animate-delay-500"></div>
          <div className="absolute w-14 h-14 md:w-20 md:h-20 rounded-full bg-gradient-to-r from-cyan-400 to-teal-400 opacity-80 bottom-10 left-1/3 animate-ping"></div>
          <div className="absolute w-18 h-18 md:w-24 md:h-24 rounded-full bg-gradient-to-r from-violet-500 to-purple-500 opacity-80 bottom-20 right-1/3 animate-pulse animate-delay-700"></div>
        </div>
      </div>
    </section>
  );
}
