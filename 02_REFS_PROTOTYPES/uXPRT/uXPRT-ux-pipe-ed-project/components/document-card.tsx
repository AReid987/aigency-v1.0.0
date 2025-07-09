"use client"

import Link from "next/link"
import { Document } from "@/lib/types"
import { cn } from "@/lib/utils"
import { motion } from "framer-motion"
import { File, FileText, Rocket, Target, Lightbulb } from "lucide-react"

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

interface DocumentCardProps {
  document: Document
  index: number
}

export function DocumentCard({ document, index }: DocumentCardProps) {
  const getIcon = () => {
    switch (document.icon) {
      case "rocket":
        return <Rocket className="h-6 w-6" />
      case "target":
        return <Target className="h-6 w-6" />
      case "file-text":
        return <FileText className="h-6 w-6" />
      case "lightbulb":
        return <Lightbulb className="h-6 w-6" />
      default:
        return <File className="h-6 w-6" />
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: index * 0.1 }}
    >
      <Link href={document.href} className="block h-full">
        <Card className="h-full transition-all duration-200 hover:shadow-md">
          <CardHeader className="flex flex-row items-center gap-4">
            <div className="rounded-md bg-primary/10 p-2 text-primary">
              {getIcon()}
            </div>
            <div>
              <CardTitle className="line-clamp-1">{document.title}</CardTitle>
              <CardDescription className="line-clamp-2">
                {document.description}
              </CardDescription>
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-sm text-muted-foreground">
              Click to view detailed content
            </div>
          </CardContent>
        </Card>
      </Link>
    </motion.div>
  )
}