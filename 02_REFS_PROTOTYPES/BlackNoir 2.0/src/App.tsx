import React, { useEffect, useState } from "react";
import { BadgeCheck, Bot, LineChart, Users, ArrowRight, Menu } from "lucide-react";
import { ThemeToggle } from "./components/ThemeToggle";
export function App() {
  const [isDark, setIsDark] = useState(false);
  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [isDark]);
  return <div className="w-full min-h-screen bg-white dark:bg-gray-900 transition-colors duration-200">
      <nav className="fixed w-full bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm z-50 border-b border-gray-200 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" className="text-blue-600">
                <path d="M12 2L15 8L21 9L16.5 14L18 20L12 17L6 20L7.5 14L3 9L9 8L12 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                <path d="M8 8L12 12L16 8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
              <span className="text-xl font-bold text-gray-900 dark:text-white">
                Lynx
              </span>
            </div>
            <div className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white transition-colors">
                Features
              </a>
              <a href="#how-it-works" className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white transition-colors">
                How it Works
              </a>
              <a href="#testimonials" className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white transition-colors">
                Testimonials
              </a>
              <ThemeToggle isDark={isDark} toggle={() => setIsDark(!isDark)} />
              <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                Get Started
              </button>
            </div>
            <div className="md:hidden flex items-center space-x-4">
              <ThemeToggle isDark={isDark} toggle={() => setIsDark(!isDark)} />
              <Menu className="h-6 w-6 text-gray-600 dark:text-gray-300" />
            </div>
          </div>
        </div>
      </nav>
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-blue-50 to-white dark:from-gray-800 dark:to-gray-900 transition-colors">
        <div className="max-w-7xl mx-auto">
          <div className="text-center">
            <h1 className="text-4xl sm:text-5xl font-bold text-gray-900 dark:text-white mb-6 transition-colors">
              Generate Quality Leads <br className="hidden sm:block" />
              <span className="text-blue-600 dark:text-blue-400">
                Automatically with AI
              </span>
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-2xl mx-auto transition-colors">
              Let Lynx's AI agent autonomously find and qualify leads while you
              focus on closing deals.
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <button className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center">
                Start Free Trial <ArrowRight className="ml-2 h-5 w-5" />
              </button>
              <button className="border border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 px-8 py-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                Watch Demo
              </button>
            </div>
          </div>
        </div>
      </section>
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-900 dark:text-white transition-colors">
            Why Choose Lynx
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="p-6 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 transition-colors">
              <Bot className="h-12 w-12 text-blue-600 dark:text-blue-400 mb-4" />
              <h3 className="text-xl font-semibold mb-2 text-gray-900 dark:text-white">
                AI-Powered Prospecting
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Our AI continuously searches and identifies high-quality leads
                matching your ideal customer profile.
              </p>
            </div>
            <div className="p-6 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 transition-colors">
              <BadgeCheck className="h-12 w-12 text-blue-600 dark:text-blue-400 mb-4" />
              <h3 className="text-xl font-semibold mb-2 text-gray-900 dark:text-white">
                Automated Qualification
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Smart algorithms qualify leads based on multiple data points to
                ensure they're sales-ready.
              </p>
            </div>
            <div className="p-6 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 transition-colors">
              <LineChart className="h-12 w-12 text-blue-600 dark:text-blue-400 mb-4" />
              <h3 className="text-xl font-semibold mb-2 text-gray-900 dark:text-white">
                Performance Analytics
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Detailed insights and analytics to track your pipeline and
                conversion rates.
              </p>
            </div>
          </div>
        </div>
      </section>
      <section id="testimonials" className="py-20 px-4 sm:px-6 lg:px-8 bg-gray-50 dark:bg-gray-800 transition-colors">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-900 dark:text-white transition-colors">
            Trusted by Sales Teams
          </h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-white p-6 rounded-xl shadow-sm">
              <div className="flex items-center mb-4">
                <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=100&h=100&q=80" alt="John Smith" className="w-12 h-12 rounded-full mr-4" />
                <div>
                  <h4 className="font-semibold">John Smith</h4>
                  <p className="text-gray-600">Sales Director, TechCorp</p>
                </div>
              </div>
              <p className="text-gray-600">
                "Lynx has transformed our lead generation process. We've seen a
                3x increase in qualified leads with half the effort."
              </p>
            </div>
            <div className="bg-white p-6 rounded-xl shadow-sm">
              <div className="flex items-center mb-4">
                <img src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=100&h=100&q=80" alt="Sarah Johnson" className="w-12 h-12 rounded-full mr-4" />
                <div>
                  <h4 className="font-semibold">Sarah Johnson</h4>
                  <p className="text-gray-600">VP Sales, GrowthCo</p>
                </div>
              </div>
              <p className="text-gray-600">
                "The AI-powered lead qualification has dramatically improved our
                conversion rates. It's like having an extra team member."
              </p>
            </div>
          </div>
        </div>
      </section>
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-6 text-gray-900 dark:text-white transition-colors">
            Ready to Automate Your Lead Generation?
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 transition-colors">
            Join hundreds of sales teams already using Lynx to generate better
            leads.
          </p>
          <button className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center mx-auto">
            Get Started Now <ArrowRight className="ml-2 h-5 w-5" />
          </button>
        </div>
      </section>
      <footer className="bg-gray-50 dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 py-12 px-4 sm:px-6 lg:px-8 transition-colors">
        <div className="max-w-7xl mx-auto grid md:grid-cols-4 gap-8">
          <div>
            <span className="text-xl font-bold text-blue-600 dark:text-blue-400">
              Lynx
            </span>
            <p className="mt-2 text-gray-600 dark:text-gray-300">
              AI-powered lead generation for modern sales teams.
            </p>
          </div>
          <div>
            <h3 className="font-semibold mb-3">Product</h3>
            <ul className="space-y-2 text-gray-600 dark:text-gray-300">
              <li>Features</li>
              <li>Pricing</li>
              <li>Use Cases</li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold mb-3">Company</h3>
            <ul className="space-y-2 text-gray-600 dark:text-gray-300">
              <li>About</li>
              <li>Blog</li>
              <li>Careers</li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold mb-3">Support</h3>
            <ul className="space-y-2 text-gray-600 dark:text-gray-300">
              <li>Help Center</li>
              <li>API Docs</li>
              <li>Contact</li>
            </ul>
          </div>
        </div>
      </footer>
    </div>;
}