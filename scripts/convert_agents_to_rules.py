#!/usr/bin/env python3
"""
Convert BMAD agent definitions to Cascade rules.
"""

import os
import yaml
import glob
import re
from pathlib import Path

def load_agent_md(file_path):
    """Load agent definition from BMAD agent file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Initialize agent data structure
    agent_data = {
        'agent': {},
        'persona': {}
    }
    
    # Extract agent section
    agent_match = re.search(r'^agent:(.*?)(?=^persona:|^$)', content, re.DOTALL | re.MULTILINE)
    if agent_match:
        agent_section = agent_match.group(1).strip()
        # Parse agent properties
        agent_data['agent'] = yaml.safe_load(agent_section)
    
    # Extract persona section
    persona_match = re.search(r'^persona:(.*?)(?=^commands:|^$)', content, re.DOTALL | re.MULTILINE)
    if persona_match:
        persona_section = persona_match.group(1).strip()
        # Parse persona properties
        agent_data['persona'] = yaml.safe_load(persona_section)
    
    # Extract commands section
    commands_match = re.search(r'^commands:(.*?)(?=^dependencies:|^$)', content, re.DOTALL | re.MULTILINE)
    if commands_match:
        commands_section = commands_match.group(1).strip()
        # Parse commands as YAML list
        formatted_commands = '- ' + commands_section.replace('\n', '\n- ')
        agent_data['commands'] = yaml.safe_load(formatted_commands)
    
    # Extract dependencies section if it exists
    deps_match = re.search(r'^dependencies:(.*?)(?=^$)', content, re.DOTALL | re.MULTILINE)
    if deps_match:
        deps_section = deps_match.group(1).strip()
        # Parse dependencies as YAML
        agent_data['dependencies'] = yaml.safe_load(deps_section)
    
    return agent_data, content

def convert_agent_to_rule(agent_id, agent_content, md_content):
    """Convert agent definition to Cascade rule format."""
    agent = agent_content.get('agent', {})
    
    # Extract agent name and description
    agent_name = agent.get('name', agent_id.replace('-', ' ').title())
    agent_desc = agent.get('whenToUse', f'Rule for {agent_name} agent')
    
    # Extract persona info
    persona = agent_content.get('persona', {})
    role = persona.get('role', agent_name)
    style = persona.get('style', '')
    identity = persona.get('identity', '')
    
    # Extract core principles
    core_principles = []
    if 'core_principles' in persona and isinstance(persona['core_principles'], list):
        core_principles = [p.strip() for p in persona['core_principles'] if isinstance(p, str)]
    
    # Build the rule content with frontmatter
    rule_lines = [
        '---',
        f'name: "{agent_name} Agent"',
        f'description: "{agent_desc}"',
        'tags:',
        f'  - {agent_id}',
        '  - agent',
        '  - bmad',
        f'  - {agent_name.lower().replace(" ", "-")}',
        '---\n',
        f'# {agent_name} Agent\n',
        f'**Role:** {role}\n',
        f'**Style:** {style}\n',
        f'**Identity:** {identity}\n\n',
        '## Core Principles\n'
    ]
    
    # Add core principles
    for principle in core_principles:
        rule_lines.append(f'- {principle}')
    
    # Add commands if they exist
    if 'commands' in agent_content:
        rule_lines.extend([
            '\n## Commands\n',
            '| Command | Description |',
            '|---------|-------------|',
        ])
        
        if isinstance(agent_content['commands'], dict):
            for cmd, desc in agent_content['commands'].items():
                if isinstance(desc, dict):
                    desc = desc.get('description', 'No description')
                rule_lines.append(f'| `{cmd}` | {desc} |')
        elif isinstance(agent_content['commands'], list):
            for cmd in agent_content['commands']:
                if isinstance(cmd, dict):
                    for k, v in cmd.items():
                        rule_lines.append(f'| `{k}` | {v} |')
                else:
                    rule_lines.append(f'| `{cmd}` | No description |')
    
    # Add dependencies if they exist
    if 'dependencies' in agent_content and agent_content['dependencies']:
        rule_lines.extend(['\n## Dependencies\n'])
        
        for dep_type, deps in agent_content['dependencies'].items():
            if not deps:
                continue
                
            rule_lines.append(f'### {dep_type.capitalize()}\n')
            
            if isinstance(deps, dict):
                for name, info in deps.items():
                    desc = info.get('description', 'No description')
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
            agent_content, md_content = load_agent_md(agent_file)
            
            # Skip if not a valid agent file
            if 'agent' not in agent_content:
                print(f"Skipping {agent_file} - not a valid agent file")
                continue
            
            # Convert to rule format
            rule_content = convert_agent_to_rule(agent_id, agent_content, md_content)
            
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
