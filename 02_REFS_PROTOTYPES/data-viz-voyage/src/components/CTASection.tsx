
import React from 'react';
import { Button } from '@/components/ui/button';
import { ArrowRight, CheckCircle } from 'lucide-react';

export function CTASection() {
  return (
    <section className="py-24 bg-gradient-to-br from-primary via-primary to-primary/80">
      <div className="max-w-4xl mx-auto px-6 text-center">
        <h2 className="text-display-small font-bold text-primary-foreground mb-6">
          Ready to transform your research workflow?
        </h2>
        <p className="text-body-large text-primary-foreground/90 mb-8 max-w-2xl mx-auto">
          Join thousands of researchers, analysts, and consultants who are already 
          using Aigency to create better insights faster.
        </p>
        
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12">
          <Button size="lg" variant="secondary" className="text-label-large px-8 py-4 h-auto">
            Start Free Trial
            <ArrowRight className="w-5 h-5 ml-2" />
          </Button>
          <Button size="lg" variant="outline" className="text-label-large px-8 py-4 h-auto border-primary-foreground/20 text-primary-foreground hover:bg-primary-foreground/10">
            Schedule Demo
          </Button>
        </div>
        
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 text-primary-foreground/90">
          <div className="flex items-center justify-center gap-2">
            <CheckCircle className="w-5 h-5" />
            <span className="text-body-medium">No credit card required</span>
          </div>
          <div className="flex items-center justify-center gap-2">
            <CheckCircle className="w-5 h-5" />
            <span className="text-body-medium">14-day free trial</span>
          </div>
          <div className="flex items-center justify-center gap-2">
            <CheckCircle className="w-5 h-5" />
            <span className="text-body-medium">Cancel anytime</span>
          </div>
        </div>
      </div>
    </section>
  );
}
