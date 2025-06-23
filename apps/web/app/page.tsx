"use client";
"use client";
import { Navigation } from "./components/Navigation";
import { HeroSection } from "./components/HeroSection";
import { FeaturesSection } from "./components/FeaturesSection";
import { StatsSection } from "./components/StatsSection";
import ParticleBackground from "./components/ParticleBackground";

export default function Home() {
  return (
    <main className="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white relative h-screen">
      {/* Particle Background - Fixed to cover the viewport behind content */}
      <div className="fixed inset-0 z-0">
        <ParticleBackground />
      </div>

      {/* Main Content - Positioned above the background */}
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Navigation />
        <HeroSection />
        <StatsSection />
        <FeaturesSection />
      </div>
    </main>
  );
}
