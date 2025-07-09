# @collaboratory/ui

A collection of reusable UI components for the Collaboratory platform.

## Components

### Button
A versatile button component with multiple variants and animations.

```tsx
import { Button } from '@collaboratory/ui'

<Button variant="default" size="lg">
  Click me
</Button>
```

### Card
A flexible card component for displaying content.

```tsx
import { Card, CardHeader, CardTitle, CardContent } from '@collaboratory/ui'

<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
  </CardHeader>
  <CardContent>
    Card content goes here
  </CardContent>
</Card>
```

### Avatar
A user avatar component with fallback support.

```tsx
import { Avatar } from '@collaboratory/ui'

<Avatar 
  src="/user-avatar.jpg" 
  alt="User Name" 
  fallback="UN"
  size="md" 
/>
```

### Dropdown Menu
A dropdown menu component built with Radix UI.

```tsx
import { 
  DropdownMenu, 
  DropdownMenuTrigger, 
  DropdownMenuContent, 
  DropdownMenuItem 
} from '@collaboratory/ui'

<DropdownMenu>
  <DropdownMenuTrigger>Open Menu</DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuItem>Item 1</DropdownMenuItem>
    <DropdownMenuItem>Item 2</DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

## Styling

All components are styled with Tailwind CSS and follow a dark theme by default. The components are designed to work seamlessly with the Collaboratory design system.

## Development

To add new components:

1. Create a new component file in `src/`
2. Export it from `src/index.ts`
3. Update the package.json exports
4. Document usage in this README
