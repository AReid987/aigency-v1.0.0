#!/bin/bash

# Convert BMAD YAML workflows to Markdown for Windsurf Cascade

# Source and target directories
SOURCE_DIR=".bmad-core/workflows"
TARGET_DIR=".windsurf/workflows"

# Create target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Function to convert YAML to Markdown
convert_yaml_to_md() {
    local yaml_file="$1"
    local base_name="$(basename "$yaml_file" .yaml)"
    local md_file="${TARGET_DIR}/${base_name}.md"
    
    echo "Converting $yaml_file to $md_file"
    
    # Extract metadata from YAML
    local workflow_id=$(yq e '.workflow.id' "$yaml_file")
    local workflow_name=$(yq e '.workflow.name' "$yaml_file")
    local workflow_desc=$(yq e '.workflow.description' "$yaml_file" | sed 's/^> //')
    
    # Create Markdown header
    echo "# $workflow_name
" > "$md_file"
    
    # Add workflow metadata
    echo "## Workflow Metadata" >> "$md_file"
    echo "- **ID:** $workflow_id" >> "$md_file"
    echo "- **Type:** $(yq e '.workflow.type' "$yaml_file")" >> "$md_file"
    echo "- **Project Types:** $(yq e '.workflow.project_types | join(", ")' "$yaml_file")" >> "$md_file"
    echo "" >> "$md_file"
    
    # Add description
    echo "## Description" >> "$md_file"
    echo "$workflow_desc" >> "$md_file"
    echo "" >> "$md_file"
    
    # Add sequence of steps
    echo "## Workflow Steps" >> "$md_file"
    yq e '.workflow.sequence[] | "### Step: \(.step)
- **Agent:** \(.agent)
- **Action:** \(.action)
- **Notes:**
  \(.notes | gsub("\n"; "\n  ") | gsub("^  "; ""))
"' "$yaml_file" >> "$md_file"
    
    # Add roles if they exist
    if yq e '.workflow.roles' "$yaml_file" | grep -q -v 'null'; then
        echo "## Roles" >> "$md_file"
        yq e '.workflow.roles | to_entries[] | "### \(.key)
- **Description:** \(.value.description)
- **Skills:** \(.value.skills | join(", "))
"' "$yaml_file" >> "$md_file"
    fi
    
    # Add configuration if it exists
    if yq e '.workflow.configuration' "$yaml_file" | grep -q -v 'null'; then
        echo "## Configuration" >> "$md_file"
        echo '```yaml' >> "$md_file"
        yq e '.workflow.configuration' "$yaml_file" >> "$md_file"
        echo '```' >> "$md_file"
    fi
    
    # Add flow diagram if it exists
    if yq e '.workflow.flow_diagram' "$yaml_file" | grep -q -v 'null'; then
        echo "## Flow Diagram" >> "$md_file"
        echo '```mermaid' >> "$md_file"
        yq e '.workflow.flow_diagram' "$yaml_file" | sed 's/^  //' >> "$md_file"
        echo '```' >> "$md_file"
    fi
    
    echo "Conversion complete: $md_file"
}

# Check if yq is installed
if ! command -v yq &> /dev/null; then
    echo "Error: yq is required but not installed. Please install it first."
    echo "On macOS: brew install yq"
    echo "On Linux: sudo apt-get install yq"
    exit 1
fi

# Process each YAML file
for yaml_file in "$SOURCE_DIR"/*.yaml; do
    if [ -f "$yaml_file" ]; then
        convert_yaml_to_md "$yaml_file"
    fi
done

echo "\nAll workflows have been converted to Markdown format in $TARGET_DIR"
