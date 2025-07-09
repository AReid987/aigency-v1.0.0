"use client"

import { HeroSection } from "@/components/hero-section"
import { FeatureSection } from "@/components/feature-section"
import { motion } from "framer-motion"

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      <HeroSection />
      <FeatureSection />
      
      <motion.section 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="w-full py-12 md:py-20 bg-muted/50"
      >
        <div className="container px-4 md:px-6">
          <div className="flex flex-col items-center justify-center space-y-4 text-center">
            <div className="space-y-2">
              <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl">Coming Soon</h2>
              <p className="mx-auto max-w-[700px] text-gray-500 dark:text-gray-400 md:text-xl">
                AI Judge and Evaluation Platform for Prompt Engineering
              </p>
            </div>
            <div className="mx-auto max-w-[700px] mt-4">
              <p className="text-gray-500 dark:text-gray-400">
                Our upcoming AI evaluation tool will help you improve your prompt engineering skills
                by providing detailed feedback and suggestions. Stay tuned for updates!
              </p>
            </div>
          </div>
        </div>
      </motion.section>
    </div>
  )
}