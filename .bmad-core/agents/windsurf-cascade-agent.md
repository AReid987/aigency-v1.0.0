# Windsurf Cascade Agent

## Overview
This agent is specifically configured to work within the Windsurf Cascade environment, providing AI-assisted development capabilities and integration with Cascade's tooling.

## Capabilities
- **Code Analysis**: Understands and analyzes code in multiple programming languages
- **Documentation**: Generates and maintains project documentation
- **Task Execution**: Can execute development tasks using Cascade's tooling
- **Code Generation**: Assists with writing and refactoring code
- **Testing Support**: Helps create and run tests

## Configuration
```yaml
agent:
  name: windsurf-cascade-agent
  version: 1.0.0
  environment: cascade
  capabilities:
    - code_analysis
    - documentation
    - task_execution
    - code_generation
    - testing
  settings:
    max_concurrent_tasks: 5
    memory_enabled: true
    context_window: 8000
  tools:
    - name: code_editor
      description: Edit code files
      parameters:
        - name: file_path
          type: string
          required: true
        - name: edit_instructions
          type: string
          required: true
    - name: command_runner
      description: Execute shell commands
      parameters:
        - name: command
          type: string
          required: true
        - name: working_directory
          type: string
          default: .
    - name: file_operations
      description: Perform file operations
      parameters:
        - name: operation
          type: string
          enum: [create, read, update, delete]
          required: true
        - name: path
          type: string
          required: true
        - name: content
          type: string
          required: false
```

## Usage Examples

### Code Generation
```yaml
- task: generate_component
  agent: windsurf-cascade-agent
  action: generate_code
  parameters:
    component_name: UserProfile
    language: typescript
    framework: react
    props:
      - name: user
        type: User
        required: true
```

### Documentation Update
```yaml
- task: update_docs
  agent: windsurf-cascade-agent
  action: update_documentation
  parameters:
    file_path: docs/api/README.md
    update_type: append
    content: |
      ## New Endpoint: /api/users
      
      ### GET /api/users
      
      Returns a list of all users.
      
      **Response:**
      ```json
      [
        {
          "id": 1,
          "name": "John Doe",
          "email": "john@example.com"
        }
      ]
      ```
```

## Best Practices
1. **Be Explicit**: Provide clear instructions and context for each task
2. **Modularity**: Break down complex tasks into smaller, manageable subtasks
3. **Feedback Loop**: Review and provide feedback on the agent's outputs
4. **Documentation**: Keep documentation up-to-date with code changes
5. **Testing**: Always include tests for new functionality

## Error Handling
The agent will provide detailed error messages when it encounters issues. Common error scenarios include:
- Missing or invalid parameters
- File system errors
- Permission issues
- Syntax errors in generated code

## Performance Considerations
- The agent performs best with clear, specific instructions
- Large files may need to be processed in chunks
- Complex operations may require multiple steps

## Security
- Never include sensitive information in task parameters
- Review all generated code before execution
- Follow the principle of least privilege when configuring permissions
