"use client"

import { motion } from "framer-motion"
import { Rocket, BookOpen, FileText, Zap } from "lucide-react"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

const features = [
  {
    icon: <BookOpen className="h-10 w-10" />,
    title: "Interactive Learning",
    description: "Learn with interactive content and examples that make complex concepts easy to understand."
  },
  {
    icon: <FileText className="h-10 w-10" />,
    title: "Comprehensive Documentation",
    description: "Access a curated library of product documentation templates and best practices."
  },
  {
    icon: <Rocket className="h-10 w-10" />,
    title: "Practical Examples",
    description: "See real-world examples of effective product documentation used by successful companies."
  },
  {
    icon: <Zap className="h-10 w-10" />,
    title: "AI Evaluation",
    description: "Coming soon: Get AI-powered feedback on your product documentation and prompt engineering skills."
  }
]

export function FeatureSection() {
  return (
    <section className="w-full py-12 md:py-20">
      <div className="container px-4 md:px-6">
        <div className="flex flex-col items-center justify-center space-y-4 text-center">
          <div className="space-y-2">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl">Features</h2>
            <p className="mx-auto max-w-[700px] text-gray-500 dark:text-gray-400 md:text-xl">
              Everything you need to master product documentation
            </p>
          </div>
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 lg:gap-8 pt-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: index * 0.1 }}
              >
                <Card className="h-full">
                  <CardHeader>
                    <div className="mb-2 rounded-md bg-primary/10 p-3 w-fit text-primary">
                      {feature.icon}
                    </div>
                    <CardTitle>{feature.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <CardDescription className="text-base">
                      {feature.description}
                    </CardDescription>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}