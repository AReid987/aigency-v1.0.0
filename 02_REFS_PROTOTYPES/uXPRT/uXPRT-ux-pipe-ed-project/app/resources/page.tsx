"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { motion } from "framer-motion"
import { Download, ExternalLink } from "lucide-react"

const resources = [
  {
    title: "GTM Template",
    description: "Comprehensive go-to-market template for product launches",
    link: "#",
    category: "Template"
  },
  {
    title: "One Pager Template",
    description: "Simple template for creating effective one-pagers",
    link: "#",
    category: "Template"
  },
  {
    title: "Product Strategy Framework",
    description: "Framework for developing a comprehensive product strategy",
    link: "#",
    category: "Framework"
  },
  {
    title: "Product Management Books",
    description: "Curated list of essential product management books",
    link: "#",
    category: "Reading List"
  },
  {
    title: "Launch Checklist",
    description: "Comprehensive checklist for product launches",
    link: "#",
    category: "Checklist"
  },
  {
    title: "Prompt Engineering Guide",
    description: "Guide to effective prompt engineering for LLMs",
    link: "#",
    category: "Guide"
  }
]

export default function ResourcesPage() {
  return (
    <div className="container py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="mb-8"
      >
        <h1 className="text-3xl font-bold mb-2">Resources</h1>
        <p className="text-muted-foreground">
          Download templates and access additional resources
        </p>
      </motion.div>
      
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {resources.map((resource, index) => (
          <motion.div
            key={resource.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: index * 0.1 }}
          >
            <Card className="h-full">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <CardTitle className="line-clamp-1">{resource.title}</CardTitle>
                  <span className="text-xs bg-primary/10 text-primary rounded-full px-2 py-1">
                    {resource.category}
                  </span>
                </div>
                <CardDescription className="line-clamp-2">
                  {resource.description}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button variant="outline" className="w-full" asChild>
                  <a href={resource.link} target="_blank" rel="noreferrer">
                    {resource.category === "Template" || resource.category === "Checklist" ? (
                      <>
                        <Download className="mr-2 h-4 w-4" />
                        Download
                      </>
                    ) : (
                      <>
                        <ExternalLink className="mr-2 h-4 w-4" />
                        View Resource
                      </>
                    )}
                  </a>
                </Button>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>
    </div>
  )
}