import Link from "next/link";

import React from 'react';
import Link from "next/link";

export function HeroSection() {
  return (
    <section className="py-20 md:py-32 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-purple-600/20 rounded-full filter blur-3xl opacity-70 animate-pulse-slow"></div>
        <div className="absolute bottom-0 right-1/4 w-80 h-80 bg-blue-600/20 rounded-full filter blur-3xl opacity-70 animate-pulse-slow animation-delay-2000"></div>
      </div>

      <div className="container-padding grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
        <div className="text-center lg:text-left">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight">
            Transform Your Workflow with
            <span className="block mt-3 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
              AI-Powered Automation
            </span>
          </h1>

          <p className="mt-6 text-lg text-slate-300 max-w-2xl mx-auto lg:mx-0">
            Aigency turbocharges your development process with intelligent agents,
            seamless integrations, and powerful automation tools. Focus on what matters
            while we handle the complexity.
          </p>

          <div className="mt-10 flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
            <Link
              href="/get-started"
              className="px-8 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-medium rounded-lg hover:opacity-90 transition-opacity shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-transform duration-300"
            >
              Get Started Free
            </Link>
            <Link
              href="/demo"
              className="px-8 py-3 bg-slate-800 text-white font-medium rounded-lg hover:bg-slate-700 transition-colors border border-slate-700"
            >
              Watch Demo
            </Link>
          </div>

          <div className="mt-10 flex flex-wrap justify-center lg:justify-start gap-4 text-slate-400 text-sm">
            <div className="flex items-center">
              <div className="w-3 h-3 rounded-full bg-green-500 mr-2 animate-pulse"></div>
              <span>No credit card required</span>
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 rounded-full bg-green-500 mr-2 animate-pulse"></div>
              <span>14-day free trial</span>
            </div>
          </div>
        </div>

        <div className="relative flex justify-center">
          <div className="relative w-full max-w-md aspect-square bg-gradient-to-br from-blue-500/10 to-purple-600/10 rounded-2xl border border-slate-700/50 backdrop-blur-sm overflow-hidden">
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="grid grid-cols-3 gap-4 p-6 w-full">
                {[...Array(6)].map((_, i) => (
                  <div
                    key={i}
                    className="aspect-square bg-slate-800/50 rounded-xl border border-slate-700/50 flex items-center justify-center"
                  >
                    <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-400 to-purple-500"></div>
                  </div>
                ))}
              </div>
            </div>

            {/* Floating elements */}
            <div className="absolute top-1/4 left-1/4 w-16 h-16 rounded-full bg-blue-500/20 border border-blue-500/30 animate-float"></div>
            <div className="absolute top-1/3 right-1/4 w-12 h-12 rounded-full bg-purple-500/20 border border-purple-500/30 animate-float animation-delay-1000"></div>
            <div className="absolute bottom-1/4 left-1/3 w-10 h-10 rounded-full bg-blue-400/20 border border-blue-400/30 animate-float animation-delay-1500"></div>
          </div>
        </div>
      </div>
    </section>
  );
}
