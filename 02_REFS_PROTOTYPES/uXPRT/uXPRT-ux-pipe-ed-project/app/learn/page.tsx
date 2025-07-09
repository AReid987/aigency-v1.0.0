import { ModuleCard } from "@/components/module-card"
import { modules } from "@/lib/modules"

export default function LearnPage() {
  return (
    <div className="container py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Learning Modules</h1>
        <p className="text-muted-foreground">
          Explore our comprehensive learning modules to master product documentation
        </p>
      </div>
      
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {modules.map((module, index) => (
          <ModuleCard key={module.id} module={module} index={index} />
        ))}
      </div>
    </div>
  )
}