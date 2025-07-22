#!/usr/bin/env python3
"""
Convert BMAD agent definitions to Cascade rules - simplified version.
This script extracts YAML content from agent Markdown files and converts them to Cascade rules.
"""

import os
import re
import yaml
import glob
from pathlib import Path

def extract_yaml_from_markdown(content):
    """Extract YAML content from markdown code blocks."""
    yaml_blocks = re.findall(r'```yaml\n(.*?)\n```', content, re.DOTALL)
    if not yaml_blocks:
        return None
    
    # Combine all YAML blocks and parse
    combined_yaml = '\n'.join(yaml_blocks)
    try:
        return yaml.safe_load(combined_yaml)
    except yaml.YAMLError as e:
        print(f"YAML parsing error: {e}")
        return None

def generate_rule_content(agent_id, yaml_content, original_content):
    """Generate Cascade rule content from YAML content."""
    if not yaml_content:
        return None
    
    agent = yaml_content.get('agent', {})
    persona = yaml_content.get('persona', {})
    
    # Extract basic info
    name = agent.get('name', agent_id.replace('-', ' ').title())
    description = agent.get('whenToUse', f'Rule for {name} agent')
    
    # Extract persona info
    role = persona.get('role', name)
    style = persona.get('style', '')
    identity = persona.get('identity', '')
    
    # Build the rule content with frontmatter
    rule_lines = [
        '---',
        f'description: {name} - {description}',
        '---\n',
        f'# {name}\n',
        '## Description\n',
        f'{description}\n',
        '## Identity\n',
        f'You are now the {name}.\n',
        f'**Role:** {role}\n',
        f'**Style:** {style}\n',
        f'**Identity:** {identity}\n\n',
    ]
    
    # Add core principles if they exist
    core_principles = persona.get('core_principles', [])
    if core_principles:
        rule_lines.append('## Core Principles\n')
        for principle in core_principles:
            rule_lines.append(f'- {principle}')
        rule_lines.append('\n')
    
    # Add commands section if they exist
    commands = yaml_content.get('commands', [])
    if commands:
        rule_lines.extend([
            '## Commands\n',
            '| Command | Description |',
            '|---------|-------------|',
        ])
        
        if isinstance(commands, dict):
            for cmd, desc in commands.items():
                if isinstance(desc, dict):
                    desc = desc.get('description', 'No description')
                rule_lines.append(f'| `{cmd}` | {desc} |')
        elif isinstance(commands, list):
            for cmd in commands:
                if isinstance(cmd, dict):
                    for k, v in cmd.items():
                        rule_lines.append(f'| `{k}` | {v} |')
                else:
                    rule_lines.append(f'| `{cmd}` | No description |')
        
        rule_lines.append('\n')
    
    # Add dependencies section if they exist
    dependencies = yaml_content.get('dependencies', {})
    if dependencies:
        rule_lines.append('## Dependencies\n')
        
        for dep_type, deps in dependencies.items():
            if not deps:
                continue
                
            rule_lines.append(f'### {dep_type.capitalize()}\n')
            
            if isinstance(deps, dict):
                for name, info in deps.items():
                    desc = info.get('description', 'No description') if isinstance(info, dict) else str(info)
                    rule_lines.append(f'- **{name}**: {desc}')
            elif isinstance(deps, list):
                for dep in deps:
                    if isinstance(dep, dict):
                        for name, info in dep.items():
                            if isinstance(info, dict):
                                desc = info.get('description', 'No description')
                                rule_lines.append(f'- **{name}**: {desc}')
                            else:
                                rule_lines.append(f'- {name}: {info}')
                    else:
                        rule_lines.append(f'- {dep}')
            
            rule_lines.append('')
    
    return '\n'.join(rule_lines)

def main():
    # Set up directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    source_dir = os.path.join(project_root, ".bmad-core", "agents")
    target_dir = os.path.join(project_root, ".windsurf", "rules")
    
    # Create target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    
    # Find all agent Markdown files
    agent_files = glob.glob(os.path.join(source_dir, "*.md"))
    
    if not agent_files:
        print(f"No agent files found in {source_dir}")
        return
    
    # Process each agent file
    for agent_file in agent_files:
        try:
            # Load agent content
            agent_id = os.path.splitext(os.path.basename(agent_file))[0]
            
            with open(agent_file, 'r') as f:
                content = f.read()
            
            # Extract YAML content
            yaml_content = extract_yaml_from_markdown(content)
            
            # Skip if no valid YAML found
            if not yaml_content:
                print(f"Skipping {agent_file} - no valid YAML content found")
                continue
            
            # Generate rule content
            rule_content = generate_rule_content(agent_id, yaml_content, content)
            
            if not rule_content:
                print(f"Skipping {agent_file} - could not generate rule content")
                continue
            
            # Determine output filename
            output_file = os.path.join(target_dir, f"agent-{agent_id}.md")
            
            # Write rule to file
            with open(output_file, 'w') as f:
                f.write(rule_content)
            
            print(f"Converted agent: {agent_file} -> {output_file}")
            
        except Exception as e:
            print(f"Error processing {agent_file}: {str(e)}")
    
    print("\nAgent conversion complete!")

if __name__ == "__main__":
    main()
