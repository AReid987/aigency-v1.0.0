import { notFound } from "next/navigation"
import { modules } from "@/lib/modules"
import { DocumentContent } from "@/components/document-content"

interface DocumentPageProps {
  params: {
    moduleId: string
    documentId: string
  }
}

export async function generateStaticParams() {
  const paths = modules.flatMap((module) =>
    module.documents.map((doc) => ({
      moduleId: module.id,
      documentId: doc.href.split('/').pop(),
    }))
  )
  return paths
}

export default function DocumentPage({ params }: DocumentPageProps) {
  const module = modules.find((m) => m.id === params.moduleId)
  
  if (!module) {
    notFound()
  }
  
  const documentIndex = module.documents.findIndex(
    (d) => d.href.endsWith(params.documentId)
  )
  
  if (documentIndex === -1) {
    notFound()
  }
  
  const document = module.documents[documentIndex]
  const prevDoc = documentIndex > 0 ? module.documents[documentIndex - 1] : null
  const nextDoc = documentIndex < module.documents.length - 1 ? module.documents[documentIndex + 1] : null
  
  return (
    <div className="container py-8">
      <DocumentContent 
        title={document.title} 
        content={document.content}
        prevDoc={prevDoc}
        nextDoc={nextDoc}
        moduleHref={`/learn/${params.moduleId}`}
      />
    </div>
  )
}