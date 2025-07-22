#!/usr/bin/env python3
"""
Convert BMAD YAML workflow files to Markdown format for Windsurf Cascade.
"""

import os
import yaml
import glob
from pathlib import Path

def load_yaml(file_path):
    """Load YAML file and return its content."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def format_notes(notes):
    """Format notes with proper indentation."""
    if not notes:
        return ""
    # Remove leading/trailing whitespace and split into lines
    lines = notes.strip().split('\n')
    # Add proper indentation
    return '\n'.join(f"  {line}" for line in lines)

def convert_workflow(yaml_content):
    """Convert YAML content to Markdown format with Cascade frontmatter."""
    workflow = yaml_content.get('workflow', {})
    workflow_id = workflow.get('id', 'untitled-workflow')
    workflow_name = workflow.get('name', 'Untitled Workflow')
    workflow_desc = workflow.get('description', 'No description provided.')
    
    # Generate frontmatter for Cascade
    frontmatter = [
        '---',
        f'name: "{workflow_name}"',
        f'description: "{workflow_desc}"',
        'tags:',
        f'  - {workflow.get("type", "general")}'
    ]
    
    # Add project types as tags
    for project_type in workflow.get('project_types', []):
        frontmatter.append(f'  - {project_type}')
    
    # Add workflow ID as a tag
    frontmatter.append(f'  - {workflow_id}')
    
    # Close frontmatter
    frontmatter.append('---\n')
    
    # Start building the markdown content
    md_lines = frontmatter + [
        f"# {workflow_name}\n",
        "## Workflow Metadata\n",
        f"- **ID:** {workflow_id}",
        f"- **Type:** {workflow.get('type', 'N/A')}",
        f"- **Project Types:** {', '.join(workflow.get('project_types', []))}\n",
        "## Description\n",
        f"{workflow_desc}\n"
    ]
    
    # Add sequence of steps
    if 'sequence' in workflow and workflow['sequence']:
        md_lines.extend(["## Workflow Steps\n"])
        for step in workflow['sequence']:
            md_lines.extend([
                f"### {step.get('step', 'Unnamed Step')}\n",
                f"- **Agent:** {step.get('agent', 'N/A')}",
                f"- **Action:** {step.get('action', 'N/A')}",
            ])
            
            if 'notes' in step:
                md_lines.append("- **Notes:**")
                # Handle multi-line notes with proper indentation
                notes = step['notes'].replace('\n', '\n  ').strip()
                md_lines.append('  ' + notes)
            
            if 'requires' in step:
                md_lines.append(f"- **Requires:** {step['requires']}")
                
            md_lines.append("")
    
    # Add roles if they exist
    if 'roles' in workflow and workflow['roles']:
        md_lines.extend(["## Roles\n"])
        
        # Handle both dictionary and list formats for roles
        if isinstance(workflow['roles'], dict):
            # Dictionary format: roles: { role_name: { description: ..., skills: [...] } }
            for role_name, role_info in workflow['roles'].items():
                md_lines.extend([
                    f"### {role_name.title()}\n",
                    f"**Description:** {role_info.get('description', 'No description')}\n",
                ])
                
                if 'skills' in role_info and role_info['skills']:
                    skills = ', '.join(role_info['skills'])
                    md_lines.append(f"**Skills:** {skills}\n")
        
        elif isinstance(workflow['roles'], list):
            # List format: roles: [ { role: name, description: ..., skills: [...] } ]
            for role_info in workflow['roles']:
                if isinstance(role_info, dict):
                    role_name = role_info.get('role', 'Unnamed Role')
                    md_lines.extend([
                        f"### {role_name.title()}\n",
                        f"**Description:** {role_info.get('description', 'No description')}\n",
                    ])
                    
                    if 'skills' in role_info and role_info['skills']:
                        skills = ', '.join(role_info['skills'])
                        md_lines.append(f"**Skills:** {skills}\n")
    
    # Add configuration if it exists
    if 'configuration' in workflow and workflow['configuration']:
        md_lines.extend([
            "## Configuration\n",
            "```yaml"
        ])
        md_lines.append(yaml.dump(workflow['configuration'], default_flow_style=False))
        md_lines.append("```\n")
    
    # Add flow diagram if it exists
    if 'flow_diagram' in workflow and workflow['flow_diagram']:
        md_lines.extend([
            "## Flow Diagram\n",
            "```mermaid"
        ])
        # Remove common indentation from the flow diagram
        flow_lines = workflow['flow_diagram'].split('\n')
        min_indent = min(len(line) - len(line.lstrip()) 
                        for line in flow_lines if line.strip())
        
        for line in flow_lines:
            md_lines.append(line[min_indent:] if line.strip() else line)
        
        md_lines.append("```\n")
    
    # Add hooks if they exist
    if 'hooks' in workflow and workflow['hooks']:
        md_lines.append("## Hooks\n")
        for hook_type, hooks in workflow['hooks'].items():
            if not hooks:
                continue
                
            md_lines.append(f"### {hook_type.title()} Hooks\n")
            
            if isinstance(hooks, list):
                for hook in hooks:
                    if 'name' in hook:
                        md_lines.append(f"- **{hook['name']}**")
                    if 'script' in hook:
                        md_lines.append(f"  - Script: `{hook['script']}`")
                    if 'description' in hook:
                        md_lines.append(f"  - {hook['description']}")
                    md_lines.append("")
            
            md_lines.append("")
    
    return '\n'.join(md_lines)

def main():
    # Set up directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    source_dir = os.path.join(project_root, ".bmad-core", "workflows")
    target_dir = os.path.join(project_root, ".windsurf", "workflows")
    
    # Create target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    
    # Find all YAML files in the source directory
    yaml_files = glob.glob(os.path.join(source_dir, "*.yaml"))
    
    if not yaml_files:
        print(f"No YAML files found in {source_dir}")
        return
    
    # Process each YAML file
    for yaml_file in yaml_files:
        try:
            # Load YAML content
            yaml_content = load_yaml(yaml_file)
            
            # Convert to Markdown
            markdown_content = convert_workflow(yaml_content)
            
            # Determine output filename
            base_name = os.path.splitext(os.path.basename(yaml_file))[0]
            output_file = os.path.join(target_dir, f"{base_name}.md")
            
            # Write Markdown to file
            with open(output_file, 'w') as f:
                f.write(markdown_content)
            
            print(f"Converted: {yaml_file} -> {output_file}")
            
        except Exception as e:
            print(f"Error processing {yaml_file}: {str(e)}")
    
    print("\nConversion complete!")

if __name__ == "__main__":
    main()
