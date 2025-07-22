'use client';

import React, { useState } from "react";
import { Rocket, Code, Users, Check, ChevronDown, ChevronUp, Play } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
const heroDemo = "/hero-demo.jpg";
const testimonialJane = "/testimonial-jane.jpg";

const LandingPage = (): JSX.Element => {
  const [expandedFaq, setExpandedFaq] = useState<string>("");

  const features = [
    {
      icon: Code,
      title: "Build Real Software",
      description: "AI builds scalable apps with custom logic.",
      benefit: "Produce professional-grade software, even if you've never written a line of code."
    },
    {
      icon: Rocket,
      title: "Rescue Every Idea",
      description: "Uses an intuitive 'Idea Perpetuator' board.",
      benefit: "Transform scattered thoughts into an actionable roadmap, ensuring your best concepts always gain momentum."
    },
    {
      icon: Users,
      title: "Get an AI Co-Founder",
      description: "Conversational interface provides feedback.",
      benefit: "Get instant feedback and tireless execution without the equity split. It's your strategic partner for building."
    },
    {
      icon: Check,
      title: "Seamless Handoff",
      description: "Escalates complex issues with full context.",
      benefit: "Ensure critical decisions always get your input. Let AI handle the routine, you handle the strategy."
    }
  ];

  const faqs = [
    {
      question: "How quickly can I set up Aigency?",
      answer: "Aigency is designed for instant activation. Simply join the beta, describe your first project in plain English, and your AI team begins working immediately. No complex onboarding or technical setup required."
    },
    {
      question: "Can an AI really produce high-quality, professional-grade output?",
      answer: "Yes. Aigency uses advanced AI models specifically trained for professional software development, design, and project management. Our beta users consistently report production-ready results that match or exceed traditional development standards."
    },
    {
      question: "How much control do I actually have?",
      answer: "Complete control. You set the vision and requirements, approve major decisions, and can modify direction at any time. Think of it as having a highly skilled team that follows your leadership while handling all the technical execution."
    },
    {
      question: "What happens if Aigency can't answer a question?",
      answer: "Aigency escalates complex decisions to you with full context and recommendations. For technical challenges beyond current capabilities, you'll receive detailed documentation to hand off to human specialists if needed."
    },
    {
      question: "Is my data secure when using Aigency?",
      answer: "Security is paramount. All data is encrypted in transit and at rest, with enterprise-grade security protocols. Your intellectual property remains completely yours, and we never use your data to train models for other users."
    },
    {
      question: "Is this only for technical people?",
      answer: "Not at all. Aigency is built for creators, entrepreneurs, and visionaries regardless of technical background. If you can describe what you want to build, Aigency can build it."
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="hero-gradient section-padding-lg text-center relative overflow-hidden">
        <div className="max-w-7xl mx-auto relative z-10">
          <div className="max-w-4xl mx-auto mb-16">
            <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
              Your AI Squad for{" "}
              <span className="text-accent">10x Faster</span> Launches
            </h1>
            <p className="text-xl md:text-2xl text-slate-300 mb-12 leading-relaxed">
              Stop juggling tasks. Aigency's AI team handles the development, design, and project management. 
              You just focus on the vision.
            </p>
            
            {/* Key Benefits */}
            <div className="grid md:grid-cols-3 gap-8 mb-16">
              <div className="flex items-center space-x-4 text-left">
                <Rocket className="w-8 h-8 text-accent flex-shrink-0" />
                <span className="text-lg">Launch products and services 10x faster</span>
              </div>
              <div className="flex items-center space-x-4 text-left">
                <Code className="w-8 h-8 text-accent flex-shrink-0" />
                <span className="text-lg">Build professional-grade applications without writing code</span>
              </div>
              <div className="flex items-center space-x-4 text-left">
                <Users className="w-8 h-8 text-accent flex-shrink-0" />
                <span className="text-lg">Get the power of an expert team, on-demand</span>
              </div>
            </div>

            {/* Hero Visual */}
            <div className="mb-12">
              <img 
                src={heroDemo} 
                alt="Aigency interface demonstration" 
                className="mx-auto rounded-2xl shadow-2xl hover-lift max-w-full h-auto"
              />
            </div>

            {/* Primary CTA */}
            <div className="space-y-4">
              <Button className="btn-primary text-lg">
                Join the Private Beta
              </Button>
              <p className="text-sm text-slate-400">
                Join 100+ innovators on the waitlist
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Problem/Agitation Section */}
      <section className="section-padding bg-muted">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-8">
            The Creator's Dilemma: A Universe of Ideas, A Team of One
          </h2>
          <div className="text-xl leading-relaxed text-muted-foreground space-y-6">
            <p>
              You have the ideas. But the friction is suffocating. The constant context-switching. 
              The burnout. Is your momentum gone?
            </p>
            <p>
              Great ideas are dying on the vine. Not because they lack vision, but because you lack velocity.
            </p>
            <p className="text-2xl font-semibold text-accent">
              That dream of making a massive impact feels further away every single day.
            </p>
          </div>
        </div>
      </section>

      {/* Solution/Benefits Section */}
      <section className="section-padding">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-8">
              How Aigency Transforms Your Workflow
            </h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
              Stop waiting for resources. Aigency is the dedicated AI team you need, on-demand. 
              Simply describe your vision in plain English. Your AI squad of engineers, designers, 
              and project managers gets to work instantly.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className="feature-card">
                <CardContent className="p-0">
                  <div className="flex items-start space-x-6">
                    <div className="p-4 bg-primary/10 rounded-xl">
                      <feature.icon className="w-8 h-8 text-accent" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-2xl font-semibold mb-3">{feature.title}</h3>
                      <p className="text-muted-foreground mb-4">{feature.description}</p>
                      <p className="text-lg font-medium">{feature.benefit}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Social Proof & Trust Section */}
      <section className="section-padding bg-muted">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-16">
            Join the Innovators Building with Aigency
          </h2>
          
          {/* Featured Testimonial */}
          <div className="max-w-4xl mx-auto">
            <Card className="feature-card text-center">
              <CardContent className="p-12">
                <blockquote className="text-2xl md:text-3xl font-medium mb-8 leading-relaxed">
                  "Aigency cut my development time from 3 months to 2 weeks. 
                  It's the AI co-founder I always wished I had."
                </blockquote>
                <div className="flex items-center justify-center space-x-4">
                  <img 
                    src={testimonialJane} 
                    alt="Jane Doe"
                    className="w-16 h-16 rounded-full object-cover"
                  />
                  <div className="text-left">
                    <p className="font-semibold text-lg">Jane Doe</p>
                    <p className="text-muted-foreground">Founder of Appify</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Differentiation Section */}
      <section className="section-padding">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-8">
            Don't Just Build a Website. <span className="text-accent">Build an Enterprise.</span>
          </h2>
          <p className="text-xl leading-relaxed text-muted-foreground">
            Website builders lock you into templates. Aigency sets your vision free. 
            You aren't dragging blocks; you're directing an actual AI development team 
            to build custom apps, platforms, and services from the ground up. 
            <span className="text-accent font-semibold"> This is how you scale.</span>
          </p>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="section-padding bg-muted">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-16">
            Have Questions? We've Got Answers.
          </h2>
          
          <Accordion type="single" collapsible className="space-y-4">
            {faqs.map((faq, index) => (
              <AccordionItem 
                key={index} 
                value={`item-${index}`}
                className="faq-item bg-card border border-border/50 rounded-xl px-6"
              >
                <AccordionTrigger className="text-left text-lg font-semibold py-6 hover:no-underline">
                  {faq.question}
                </AccordionTrigger>
                <AccordionContent className="text-muted-foreground leading-relaxed pb-6">
                  {faq.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="section-padding-lg text-center hero-gradient">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-bold mb-8">
            Stop Being a Solo Creator. <br />
            <span className="text-accent">Start Being a One-Person Enterprise.</span>
          </h2>
          
          <div className="space-y-6">
            <Button className="btn-primary text-lg">
              Join the Private Beta
            </Button>
            <div className="flex items-center justify-center space-x-2 text-muted-foreground">
              <Play className="w-4 h-4" />
              <span className="underline cursor-pointer hover:text-accent transition-colors">
                Or Watch a 2-Minute Overview Video
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="section-padding border-t border-border/50">
        <div className="max-w-4xl mx-auto text-center space-y-4">
          <p className="text-muted-foreground">
            © 2025 Aigency. All Rights Reserved.
          </p>
          <div className="flex justify-center space-x-8 text-sm">
            <a href="#" className="text-muted-foreground hover:text-accent transition-colors">
              Privacy Policy
            </a>
            <a href="#" className="text-muted-foreground hover:text-accent transition-colors">
              Terms of Service
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
