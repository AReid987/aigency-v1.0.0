#!/bin/bash

# Test BMAD Setup for Windsurf Cascade
# This script verifies the BMAD configuration and integration with Windsurf Cascade

echo "🚀 Starting BMAD Setup Test for Windsurf Cascade"
echo "=========================================="

# Check if .bmad-core directory exists
if [ -d ".bmad-core" ]; then
  echo "✅ Found .bmad-core directory"
else
  echo "❌ Error: .bmad-core directory not found"
  exit 1
fi

# Check for required workflow files
required_workflows=(
  "windsurf-cascade.yaml"
  "test-windsurf-integration.yaml"
  "brownfield-fullstack.yaml"
  "brownfield-service.yaml"
  "brownfield-ui.yaml"
  "greenfield-fullstack.yaml"
  "greenfield-service.yaml"
  "greenfield-ui.yaml"
)

for workflow in "${required_workflows[@]}"; do
  if [ -f ".bmad-core/workflows/$workflow" ]; then
    echo "✅ Found workflow: $workflow"
  else
    echo "⚠️  Warning: Missing workflow: $workflow"
  fi
done

# Check for required documentation
required_docs=(
  "docs/architecture/tech-stack.md"
  "docs/architecture/coding-standards.md"
  "docs/architecture/source-tree.md"
  "docs/prd/overview.md"
)

for doc in "${required_docs[@]}"; do
  if [ -f "$doc" ]; then
    echo "✅ Found documentation: $doc"
  else
    echo "⚠️  Warning: Missing documentation: $doc"
  fi
done

# Check for required directories
required_dirs=(
  "docs/prd"
  "docs/architecture"
  "docs/stories"
  ".ai"
)

for dir in "${required_dirs[@]}"; do
  if [ -d "$dir" ]; then
    echo "✅ Found directory: $dir"
  else
    echo "⚠️  Warning: Missing directory: $dir"
  fi
done

# Test BMAD configuration
echo -e "\n🔍 Testing BMAD Configuration"
if [ -f ".bmad-core/core-config.yaml" ]; then
  echo "✅ Found core-config.yaml"
  
  # Check version
  version=$(grep "^version:" .bmad-core/core-config.yaml | awk '{print $2}')
  echo "   BMAD Version: $version"
  
  # Check markdownExploder setting
  markdown_exploder=$(grep "^markdownExploder:" .bmad-core/core-config.yaml | awk '{print $2}')
  echo "   Markdown Exploder: $markdown_exploder"
  
  # Check PRD configuration
  prd_file=$(grep "^  prdFile:" .bmad-core/core-config.yaml | awk '{print $2}')
  echo "   PRD File: $prd_file"
  
  # Check architecture configuration
  arch_file=$(grep "^  architectureFile:" .bmad-core/core-config.yaml | awk '{print $2}')
  echo "   Architecture File: $arch_file"
else
  echo "❌ Error: core-config.yaml not found"
  exit 1
fi

# Test Windsurf Cascade workflow
echo -e "\n🔍 Testing Windsurf Cascade Workflow"
if [ -f ".bmad-core/workflows/windsurf-cascade.yaml" ]; then
  echo "✅ Found Windsurf Cascade workflow"
  
  # Check workflow name
  workflow_name=$(grep "^  name:" .bmad-core/workflows/windsurf-cascade.yaml | head -1 | awk -F': ' '{print $2}')
  echo "   Workflow Name: $workflow_name"
  
  # Check workflow type
  workflow_type=$(grep "^  type:" .bmad-core/workflows/windsurf-cascade.yaml | head -1 | awk '{print $2}')
  echo "   Workflow Type: $workflow_type"
  
  # Check number of steps
  step_count=$(grep -c "^- step:" .bmad-core/workflows/windsurf-cascade.yaml)
  echo "   Number of Steps: $step_count"
else
  echo "❌ Error: Windsurf Cascade workflow not found"
  exit 1
fi

# Test Windsurf Cascade agent
echo -e "\n🔍 Testing Windsurf Cascade Agent"
if [ -f ".bmad-core/agents/windsurf-cascade-agent.md" ]; then
  echo "✅ Found Windsurf Cascade agent configuration"
  
  # Check agent capabilities
  echo "   Agent Capabilities:"
  grep "^    - " .bmad-core/agents/windsurf-cascade-agent.md | sed 's/^    - //' | sed 's/^/     - /'
else
  echo "⚠️  Warning: Windsurf Cascade agent configuration not found"
fi

echo -e "\n🎉 BMAD Setup Test Completed!"

# Check for any warnings
if grep -q "Warning:" $0; then
  echo -e "\n⚠️  Some warnings were found. Please review the output above."
  exit 1
else
  echo -e "\n✅ All tests passed successfully! BMAD is properly configured for Windsurf Cascade."
  exit 0
fi
