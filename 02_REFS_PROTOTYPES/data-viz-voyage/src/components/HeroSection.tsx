
import React from 'react';
import { Button } from '@/components/ui/button';
import { ParticleCloud3D } from './ParticleCloud3D';
import { ArrowRight, Check } from 'lucide-react';

export function HeroSection() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      <div className="relative z-10 max-w-7xl mx-auto px-6 py-32">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary border border-primary/20 mb-8">
            <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
            <span className="text-label-medium font-medium">Built for thinkers who build</span>
          </div>
          
          <h1 className="text-6xl md:text-8xl font-bold text-foreground mb-6 leading-none tracking-tight">
            <span className="block">Aigency</span>
            <span className="block text-primary text-4xl md:text-6xl mt-4">10x Yourself</span>
          </h1>
          
          <p className="text-xl md:text-2xl text-muted-foreground max-w-3xl mx-auto mb-12 leading-relaxed">
            Become a Super Human. Your Team of Agents are ready for takeoff.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
            <Button size="lg" className="text-lg px-10 py-6 h-auto rounded-full">
              Get Started Free
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
            <Button variant="outline" size="lg" className="text-lg px-10 py-6 h-auto rounded-full">
              Watch Demo
            </Button>
          </div>

          <div className="flex flex-wrap items-center justify-center gap-8 text-sm text-muted-foreground mb-16">
            <div className="flex items-center gap-2">
              <Check className="w-4 h-4 text-primary" />
              <span>No credit card required</span>
            </div>
            <div className="flex items-center gap-2">
              <Check className="w-4 h-4 text-primary" />
              <span>14-day free trial</span>
            </div>
            <div className="flex items-center gap-2">
              <Check className="w-4 h-4 text-primary" />
              <span>Cancel anytime</span>
            </div>
          </div>
        </div>
        
        {/* 3D Particle Cloud replacing the screenshot */}
        <div className="max-w-5xl mx-auto">
          <ParticleCloud3D />
        </div>
      </div>
      
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-background via-accent/5 to-primary/10" />
    </section>
  );
}
