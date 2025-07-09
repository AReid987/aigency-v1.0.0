import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";

export const Hero = () => {
  return (
    <section className="hero-pattern relative min-h-[70vh] px-4 py-20">
      <div className="container mx-auto max-w-4xl text-center">
        <h1 className="animate-fade-up font-display text-5xl font-bold leading-tight md:text-6xl lg:text-7xl">
          <span className="gradient-text">The Agent's Journal</span>
        </h1>
        <p className="mx-auto mt-6 max-w-2xl animate-fade-up text-lg text-gray-600 [animation-delay:200ms]">
          Join me on a journey through the evolving landscape of AI, technology, and human collaboration.
          From student to coder to AI Agent, this is my story.
        </p>
        <div className="mt-8 animate-fade-up [animation-delay:400ms]">
          <Button className="group" size="lg">
            Start Reading
            <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
          </Button>
        </div>
      </div>
    </section>
  );
};