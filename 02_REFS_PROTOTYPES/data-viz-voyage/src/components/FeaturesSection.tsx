
import React from 'react';
import { BarChart3, Brain, Share2, Shield, Sparkles, Target } from 'lucide-react';

const features = [
  {
    icon: BarChart3,
    title: "Interactive Dashboards",
    description: "Create stunning visualizations with real-time data updates and customizable charts that tell your story."
  },
  {
    icon: Brain,
    title: "AI-Powered Insights",
    description: "Leverage machine learning to uncover hidden patterns and generate automated research summaries."
  },
  {
    icon: Share2,
    title: "Seamless Collaboration",
    description: "Share reports instantly with stakeholders and collaborate in real-time on research projects."
  },
  {
    icon: Shield,
    title: "Enterprise Security",
    description: "Bank-level encryption and compliance standards ensure your research data stays protected."
  },
  {
    icon: Sparkles,
    title: "Smart Automation",
    description: "Automate repetitive tasks and focus on what matters most - analyzing and interpreting data."
  },
  {
    icon: Target,
    title: "Precision Analytics",
    description: "Advanced statistical models and predictive analytics for accurate market forecasting."
  }
];

export function FeaturesSection() {
  return (
    <section id="features" className="py-24 bg-muted/30">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-display-small font-bold text-foreground mb-4">
            Everything you need to 10x your research
          </h2>
          <p className="text-body-large text-muted-foreground max-w-2xl mx-auto">
            From data collection to final presentation, our platform provides all the tools 
            you need to create compelling market research.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="p-8 rounded-2xl bg-card border border-border hover:shadow-lg transition-shadow">
              <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-6">
                <feature.icon className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-title-large font-semibold text-foreground mb-3">
                {feature.title}
              </h3>
              <p className="text-body-medium text-muted-foreground leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
