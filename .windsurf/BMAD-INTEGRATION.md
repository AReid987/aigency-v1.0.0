# BMAD Integration with Windsurf Cascade

This document provides an overview of the BMAD (Business Model Agile Development) integration with Windsurf Cascade, including how to use the converted workflows and agent rules.

## Overview

BMAD workflows and agents have been converted to work seamlessly with Windsurf Cascade. The integration includes:

- **Workflows**: Converted from YAML to Markdown with Cascade-compatible frontmatter
- **Agents**: Converted to Cascade rules with proper metadata and organization

## Directory Structure

```
.windsurf/
├── workflows/           # Converted BMAD workflows
│   ├── brownfield-fullstack.md
│   ├── greenfield-ui.md
│   └── ...
└── rules/              # Converted BMAD agents as rules
    ├── agent-architect.md
    ├── agent-dev.md
    └── ...
```

## Using BMAD Workflows

BMAD workflows are now available as slash commands in Cascade. To use them:

1. Open a chat in Cascade
2. Type `/` to see the list of available workflows
3. Select a workflow to start using it

Example:
```
/brownfield-fullstack
```

## Using BMAD Agents as Rules

BMAD agents have been converted to Cascade rules. These rules enhance Cascade's capabilities with specialized agent behaviors. The rules are automatically available in your Cascade environment.

To view available agent rules:

1. Open the Rules section in Cascade
2. Filter by the `bmad` tag to see all BMAD-related rules

## Customization

You can customize the workflows and rules by editing the Markdown files in the `.windsurf` directory. The files follow a simple format with YAML frontmatter for metadata and Markdown content.

### Workflow Frontmatter

```yaml
---
name: "Workflow Name"
description: "Description of the workflow"
tags:
  - tag1
  - tag2
  - bmad
---
```

### Rule Frontmatter

```yaml
---
name: "Agent Name"
description: "Description of the agent rule"
tags:
  - agent
  - bmad
  - agent-type
---
```

## Conversion Scripts

The following scripts were used to convert BMAD assets to Cascade-compatible formats:

1. `scripts/convert_workflows.py`: Converts BMAD workflow YAML files to Markdown
2. `scripts/convert_agents_simple.py`: Converts BMAD agent definitions to Cascade rules

### Running Conversion Scripts

To update the converted files:

```bash
# Convert workflows
python3 scripts/convert_workflows.py

# Convert agents
python3 scripts/convert_agents_simple.py
```

## Troubleshooting

If you encounter any issues:

1. Check that the BMAD core files are properly installed in the `.bmad-core` directory
2. Verify that the conversion scripts have the necessary permissions to read/write files
3. Check the script output for any error messages

## Next Steps

- [ ] Test all converted workflows in Cascade
- [ ] Validate agent rule behavior
- [ ] Gather feedback and make adjustments as needed
- [ ] Document any customizations or extensions made to the BMAD workflows/rules
