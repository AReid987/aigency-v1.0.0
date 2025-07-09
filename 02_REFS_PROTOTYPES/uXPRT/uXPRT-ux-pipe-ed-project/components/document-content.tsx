"use client"

import React from "react"
import { motion } from "framer-motion"
import ReactMarkdown from "react-markdown"

import { Separator } from "@/components/ui/separator"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Card, CardContent } from "@/components/ui/card"
import { CheckCircle, ChevronLeft, ChevronRight } from "lucide-react"
import Link from "next/link"

interface DocumentContentProps {
  title: string
  content: string
  prevDoc?: { title: string; href: string } | null
  nextDoc?: { title: string; href: string } | null
  moduleHref: string
}

export function DocumentContent({ 
  title, 
  content, 
  prevDoc, 
  nextDoc, 
  moduleHref 
}: DocumentContentProps) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="flex flex-col space-y-4"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Link href={moduleHref}>
            <Button variant="ghost" size="sm">
              <ChevronLeft className="mr-1 h-4 w-4" />
              Back to module
            </Button>
          </Link>
        </div>
        <Button variant="outline" size="sm">
          <CheckCircle className="mr-1 h-4 w-4" />
          Mark as complete
        </Button>
      </div>
      
      <Card className="overflow-hidden">
        <CardContent className="p-0">
          <ScrollArea className="h-[calc(100vh-250px)] rounded-md">
            <div className="space-y-6 p-6">
              <div className="space-y-2">
                <h1 className="text-3xl font-bold tracking-tight">{title}</h1>
                <Separator />
              </div>
              <div className="prose prose-neutral dark:prose-invert max-w-none">
                <ReactMarkdown>{content}</ReactMarkdown>
              </div>
            </div>
          </ScrollArea>
        </CardContent>
      </Card>
      
      <div className="flex items-center justify-between">
        {prevDoc ? (
          <Link href={prevDoc.href}>
            <Button variant="outline" size="sm">
              <ChevronLeft className="mr-1 h-4 w-4" />
              {prevDoc.title}
            </Button>
          </Link>
        ) : (
          <div></div>
        )}
        {nextDoc ? (
          <Link href={nextDoc.href}>
            <Button variant="outline" size="sm">
              {nextDoc.title}
              <ChevronRight className="ml-1 h-4 w-4" />
            </Button>
          </Link>
        ) : (
          <div></div>
        )}
      </div>
    </motion.div>
  )
}