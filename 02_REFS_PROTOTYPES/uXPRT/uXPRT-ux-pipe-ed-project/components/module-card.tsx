"use client"

import Image from "next/image"
import Link from "next/link"
import { Module } from "@/lib/types"
import { cn } from "@/lib/utils"
import { motion } from "framer-motion"

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ChevronRight } from "lucide-react"

interface ModuleCardProps {
  module: Module
  index: number
}

export function ModuleCard({ module, index }: ModuleCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.1 }}
    >
      <Link href={`/learn/${module.id}`} className="block h-full">
        <Card className="h-full overflow-hidden transition-all duration-200 hover:shadow-md">
          {module.coverImage && (
            <div className="relative h-48 w-full overflow-hidden">
              <Image
                src={module.coverImage}
                alt={module.title}
                fill
                className="object-cover transition-transform duration-300 hover:scale-105"
                sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
              />
            </div>
          )}
          <CardHeader>
            <CardTitle className="line-clamp-1">{module.title}</CardTitle>
            <CardDescription className="line-clamp-2">
              {module.description}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-sm text-muted-foreground">
              {module.documents.length} documents
            </div>
          </CardContent>
          <CardFooter>
            <Button variant="ghost" className="w-full justify-between">
              <span>Start learning</span>
              <ChevronRight className="h-4 w-4" />
            </Button>
          </CardFooter>
        </Card>
      </Link>
    </motion.div>
  )
}