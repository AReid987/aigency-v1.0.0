# @aigency/canvas

A powerful canvas package that combines ArchVision's infinite canvas capabilities with BrainCraft's AI-powered diagramming features.

## Features

- 🎨 Infinite Canvas with multiple views:
  - 2D for traditional diagramming
  - 3D for spatial visualization
  - Isometric for architectural views

- 🤖 AI-Powered Diagram Generation:
  - Natural language to diagram conversion
  - Support for multiple diagram types (flowcharts, sequence diagrams, etc.)
  - Interactive chat interface

- 🔄 Real-time Collaboration Ready
- 🎯 Extensible Architecture
- 📦 Easy Integration with Aigency

## Installation

```bash
pnpm add @aigency/canvas
```

## Usage

### Basic Example

```tsx
import { InfiniteCanvas } from '@aigency/canvas';

function App() {
  return (
    <InfiniteCanvas 
      mode="hybrid"
      defaultView="2d"
      enableAI={true}
    />
  );
}
```

### With AI Diagram Generation

```tsx
import { DiagramPanel, ChatInterface } from '@aigency/canvas';

function DiagramGenerator() {
  const handleGenerate = async (prompt: string) => {
    // Handle diagram generation
  };

  return (
    <div>
      <DiagramPanel code={diagramCode} type="flowchart" />
      <ChatInterface onSendMessage={handleGenerate} />
    </div>
  );
}
```

## Integration with Aigency

1. Add the package to your workspace:

```json
{
  "dependencies": {
    "@aigency/canvas": "workspace:*"
  }
}
```

2. Import and use in your app:

```tsx
import { CanvasProvider, InfiniteCanvas } from '@aigency/canvas';

function AigencyApp() {
  return (
    <CanvasProvider>
      <InfiniteCanvas 
        mode="hybrid"
        enableAI={true}
        enableCollaboration={true}
      />
    </CanvasProvider>
  );
}
```

## Development

```bash
# Install dependencies
pnpm install

# Start development server
pnpm dev

# Build package
pnpm build
```

## Architecture

The package combines two main features:

1. **ArchVision**: Provides the infinite canvas and multiple view capabilities
2. **BrainCraft**: Handles AI-powered diagram generation and chat interface

These are unified under a single API while maintaining separation of concerns for extensibility.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
