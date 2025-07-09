import { notFound } from "next/navigation"
import { modules } from "@/lib/modules"
import { DocumentCard } from "@/components/document-card"

interface ModulePageProps {
  params: {
    moduleId: string
  }
}

export async function generateStaticParams() {
  return modules.map((module) => ({
    moduleId: module.id,
  }))
}

export default function ModulePage({ params }: ModulePageProps) {
  const module = modules.find((m) => m.id === params.moduleId)
  
  if (!module) {
    notFound()
  }
  
  return (
    <div className="container py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">{module.title}</h1>
        <p className="text-muted-foreground">{module.description}</p>
      </div>
      
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {module.documents.map((document, index) => (
          <DocumentCard key={document.href} document={document} index={index} />
        ))}
      </div>
    </div>
  )
}