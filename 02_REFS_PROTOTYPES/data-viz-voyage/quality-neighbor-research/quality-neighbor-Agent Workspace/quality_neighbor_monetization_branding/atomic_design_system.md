# Quality Neighbor Atomic Design System

## Introduction

This document defines Quality Neighbor's comprehensive design system using the atomic design methodology, which organizes design elements hierarchically from fundamental building blocks to complete interfaces. The system ensures visual consistency, accelerates development, and reinforces our professional community newsletter brand identity across all touchpoints.

The atomic design approach breaks down our interface into five distinct levels:
1. **Atoms**: Fundamental building blocks (colors, typography, buttons, inputs)
2. **Molecules**: Simple combinations of atoms (search bars, form groups, cards)
3. **Organisms**: Complex components (headers, article layouts, business listings)
4. **Templates**: Page layouts without content (newsletter template, profile page)
5. **Pages**: Specific implementations with real content

This structured approach ensures consistency while allowing for scalable, maintainable design that reinforces our brand identity: professional, trustworthy, community-focused, and purposeful.

---

## Design Tokens

Design tokens are the fundamental visual values that form the foundation of our design system. They define the visual characteristics that make Quality Neighbor distinctive and consistent across all touchpoints.

### Color Palette

Our color system balances professional trustworthiness with community warmth, using a sophisticated palette that conveys reliability while remaining approachable and engaging.

#### Primary Colors

| Token | Hex | RGB | Description |
|-------|-----|-----|-------------|
| `--color-primary-900` | `#062C43` | `6, 44, 67` | Deep navy - primary brand color, headers |
| `--color-primary-800` | `#113A5D` | `17, 58, 93` | Navy - secondary headers, icons |
| `--color-primary-700` | `#1D5B8C` | `29, 91, 140` | Deep blue - interactive elements |
| `--color-primary-600` | `#2978B5` | `41, 120, 181` | Medium blue - buttons, links |
| `--color-primary-500` | `#3E92CC` | `62, 146, 204` | Standard blue - primary actions |
| `--color-primary-400` | `#64A9DB` | `100, 169, 219` | Light blue - secondary actions |
| `--color-primary-300` | `#8BC1EA` | `139, 193, 234` | Pale blue - highlights, backgrounds |
| `--color-primary-200` | `#B1D4F5` | `177, 212, 245` | Very light blue - subdued backgrounds |
| `--color-primary-100` | `#D6E9FA` | `214, 233, 250` | Faintest blue - subtle highlights |
| `--color-primary-50` | `#EBF4FD` | `235, 244, 253` | Nearly white blue - page backgrounds |

#### Secondary Colors

| Token | Hex | RGB | Description |
|-------|-----|-----|-------------|
| `--color-secondary-900` | `#444130` | `68, 65, 48` | Deep sage - grounding element |
| `--color-secondary-800` | `#555144` | `85, 81, 68` | Dark sage - text on light backgrounds |
| `--color-secondary-700` | `#696257` | `105, 98, 87` | Medium sage - subdued text |
| `--color-secondary-600` | `#7D7567` | `125, 117, 103` | Light sage - borders, dividers |
| `--color-secondary-500` | `#928A7B` | `146, 138, 123` | Standard sage - neutral elements |
| `--color-secondary-400` | `#A7A194` | `167, 161, 148` | Pale sage - disabled states |
| `--color-secondary-300` | `#BDB8AE` | `189, 184, 174` | Very light sage - subtle borders |
| `--color-secondary-200` | `#D3D0C8` | `211, 208, 200` | Faint sage - subtle backgrounds |
| `--color-secondary-100` | `#E9E7E3` | `233, 231, 227` | Nearly white sage - alt backgrounds |
| `--color-secondary-50` | `#F4F3F1` | `244, 243, 241` | Whisper sage - subtle variations |

#### Accent Colors

| Token | Hex | RGB | Description |
|-------|-----|-----|-------------|
| `--color-accent-red` | `#C75D4F` | `199, 93, 79` | Warm red - alerts, errors |
| `--color-accent-green` | `#4F9D69` | `79, 157, 105` | Sage green - success, growth |
| `--color-accent-yellow` | `#E9C46A` | `233, 196, 106` | Warm yellow - warnings, highlights |
| `--color-accent-purple` | `#6A5D8C` | `106, 93, 140` | Muted purple - premium features |
| `--color-accent-teal` | `#3D8C8C` | `61, 140, 140` | Teal - informational elements |

#### Neutral Colors

| Token | Hex | RGB | Description |
|-------|-----|-----|-------------|
| `--color-neutral-900` | `#171717` | `23, 23, 23` | Nearly black - primary text |
| `--color-neutral-800` | `#333333` | `51, 51, 51` | Very dark gray - secondary text |
| `--color-neutral-700` | `#4A4A4A` | `74, 74, 74` | Dark gray - tertiary text |
| `--color-neutral-600` | `#666666` | `102, 102, 102` | Medium gray - disabled text |
| `--color-neutral-500` | `#8A8A8A` | `138, 138, 138` | Standard gray - placeholders |
| `--color-neutral-400` | `#A8A8A8` | `168, 168, 168` | Light gray - dividers |
| `--color-neutral-300` | `#CECECE` | `206, 206, 206` | Very light gray - borders |
| `--color-neutral-200` | `#E6E6E6` | `230, 230, 230` | Faint gray - backgrounds |
| `--color-neutral-100` | `#F3F3F3` | `243, 243, 243` | Nearly white - alt backgrounds |
| `--color-neutral-50` | `#FAFAFA` | `250, 250, 250` | Off-white - page backgrounds |
| `--color-white` | `#FFFFFF` | `255, 255, 255` | Pure white |

#### Semantic Colors

| Token | Hex | RGB | Description |
|-------|-----|-----|-------------|
| `--color-error` | `#C75D4F` | `199, 93, 79` | Error messages, destructive actions |
| `--color-error-light` | `#FAEAE8` | `250, 234, 232` | Error backgrounds |
| `--color-success` | `#4F9D69` | `79, 157, 105` | Success messages, confirmations |
| `--color-success-light` | `#E8F4EB` | `232, 244, 235` | Success backgrounds |
| `--color-warning` | `#E9C46A` | `233, 196, 106` | Warning messages, cautions |
| `--color-warning-light` | `#FCF7E8` | `252, 247, 232` | Warning backgrounds |
| `--color-info` | `#3E92CC` | `62, 146, 204` | Informational messages, notices |
| `--color-info-light` | `#E6F2FA` | `230, 242, 250` | Information backgrounds |

### Typography

Our typography system is inspired by traditional newspaper design while embracing digital readability, balancing professionalism with accessibility. We use a serif font for headings to evoke traditional journalism credibility and a clean sans-serif for body text to ensure optimal readability.

#### Font Families

| Token | Value | Usage |
|-------|-------|-------|
| `--font-family-heading` | `'Libre Baskerville', Georgia, serif` | Headers, titles, and feature text |
| `--font-family-body` | `'Source Sans Pro', Helvetica, Arial, sans-serif` | Body text, UI elements, labels |
| `--font-family-monospace` | `'Source Code Pro', Consolas, monospace` | Code, technical content |

#### Font Weights

| Token | Value | Usage |
|-------|-------|-------|
| `--font-weight-light` | `300` | Subtle, decorative text |
| `--font-weight-regular` | `400` | Standard body text |
| `--font-weight-medium` | `500` | Emphasis, subheadings |
| `--font-weight-semibold` | `600` | Section headers, important text |
| `--font-weight-bold` | `700` | Main headings, strong emphasis |

#### Font Sizes

| Token | Value | Rem | Usage |
|-------|-------|-----|-------|
| `--font-size-2xs` | `12px` | `0.75rem` | Fine print, legal text |
| `--font-size-xs` | `14px` | `0.875rem` | Captions, metadata |
| `--font-size-sm` | `16px` | `1rem` | Secondary body text, UI elements |
| `--font-size-md` | `18px` | `1.125rem` | Primary body text |
| `--font-size-lg` | `20px` | `1.25rem` | Lead paragraphs, subheadings |
| `--font-size-xl` | `24px` | `1.5rem` | Section headings |
| `--font-size-2xl` | `30px` | `1.875rem` | Article headings |
| `--font-size-3xl` | `36px` | `2.25rem` | Page headings |
| `--font-size-4xl` | `48px` | `3rem` | Major headings |
| `--font-size-5xl` | `60px` | `3.75rem` | Hero headings |

#### Line Heights

| Token | Value | Usage |
|-------|-------|-------|
| `--line-height-tight` | `1.1` | Headlines, very short text |
| `--line-height-condensed` | `1.25` | Subheadings, tight contexts |
| `--line-height-normal` | `1.5` | Body text, general use |
| `--line-height-relaxed` | `1.625` | Longer text blocks |
| `--line-height-loose` | `1.8` | Reader-focused long-form content |

#### Letter Spacing

| Token | Value | Usage |
|-------|-------|-------|
| `--letter-spacing-tight` | `-0.02em` | Headlines, large display text |
| `--letter-spacing-normal` | `0` | Body text, general use |
| `--letter-spacing-wide` | `0.05em` | All caps, small labels |
| `--letter-spacing-wider` | `0.1em` | Very small all caps, accents |

#### Typography Scale Combinations

| Element | Font | Weight | Size | Line Height | Letter Spacing |
|---------|------|--------|------|-------------|---------------|
| H1 (Page Title) | Heading | Bold | 4xl | Tight | Tight |
| H2 (Section Title) | Heading | Bold | 3xl | Tight | Tight |
| H3 (Subsection) | Heading | Semibold | 2xl | Condensed | Tight |
| H4 (Group Heading) | Heading | Semibold | xl | Condensed | Normal |
| H5 (Minor Heading) | Heading | Medium | lg | Normal | Normal |
| H6 (Small Heading) | Heading | Medium | md | Normal | Normal |
| Lead Paragraph | Body | Regular | lg | Relaxed | Normal |
| Body Text | Body | Regular | md | Normal | Normal |
| Small Text | Body | Regular | sm | Normal | Normal |
| Caption | Body | Regular | xs | Normal | Normal |
| Button | Body | Semibold | sm | Normal | Wide |
| Input | Body | Regular | md | Normal | Normal |
| Navigation | Body | Medium | sm | Normal | Normal |
| Footer Text | Body | Regular | xs | Normal | Normal |

### Spacing System

Our spacing system uses an 8-point grid to ensure consistent spacing throughout the interface. This grid-based approach provides flexibility while maintaining visual harmony.

#### Base Spacing Units

| Token | Value | Usage |
|-------|-------|-------|
| `--spacing-2xs` | `4px` | Minimal spacing, tight contexts |
| `--spacing-xs` | `8px` | Compact elements, icons |
| `--spacing-sm` | `12px` | Form elements, tight containers |
| `--spacing-md` | `16px` | Standard spacing, general use |
| `--spacing-lg` | `24px` | Section separators, content blocks |
| `--spacing-xl` | `32px` | Major sections, generous spacing |
| `--spacing-2xl` | `48px` | Page sections, major divisions |
| `--spacing-3xl` | `64px` | Large layout divisions |
| `--spacing-4xl` | `96px` | Very large layout sections |
| `--spacing-5xl` | `128px` | Maximum spacing, special cases |

#### Component-Specific Spacing

| Context | Inner Spacing | Outer Spacing |
|---------|---------------|---------------|
| Cards | `--spacing-md` padding | `--spacing-lg` margin |
| Buttons | `--spacing-sm` padding-y, `--spacing-md` padding-x | `--spacing-sm` margin |
| Form Fields | `--spacing-sm` padding | `--spacing-md` margin-bottom |
| Section Dividers | N/A | `--spacing-xl` margin-y |
| List Items | `--spacing-sm` padding-y | `--spacing-xs` margin-y |
| Navigation Items | `--spacing-sm` padding | `--spacing-2xs` margin |
| Page Containers | `--spacing-xl` padding | `--spacing-2xl` margin-bottom |

### Elevation (Shadows)

Our elevation system uses shadows to create depth and hierarchy, with a subtle approach that maintains our professional aesthetic while providing clear visual cues about component relationships.

| Token | Value | Usage |
|-------|-------|-------|
| `--shadow-xs` | `0 1px 2px rgba(0, 0, 0, 0.05)` | Subtle highlights, dividers |
| `--shadow-sm` | `0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06)` | Cards, contained elements |
| `--shadow-md` | `0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)` | Floating elements, popovers |
| `--shadow-lg` | `0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)` | Modals, highlighted content |
| `--shadow-xl` | `0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)` | Elevated content, drawers |
| `--shadow-2xl` | `0 25px 50px -12px rgba(0, 0, 0, 0.25)` | Maximum elevation, key focus elements |
| `--shadow-inner` | `inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)` | Inset elements, pressed states |
| `--shadow-outline` | `0 0 0 3px rgba(62, 146, 204, 0.5)` | Focus states, selections |

### Border Radius

Our border radius system uses a consistent approach to rounded corners, providing a polished, contemporary feel while maintaining our professional aesthetic.

| Token | Value | Usage |
|-------|-------|-------|
| `--radius-none` | `0` | Square elements, full-bleed components |
| `--radius-sm` | `2px` | Subtle rounding, small elements |
| `--radius-md` | `4px` | Standard buttons, cards, inputs |
| `--radius-lg` | `8px` | Featured cards, prominent elements |
| `--radius-xl` | `12px` | Modal windows, large components |
| `--radius-2xl` | `16px` | Featured containers, major elements |
| `--radius-full` | `9999px` | Pills, tags, circular elements |

### Border Widths

| Token | Value | Usage |
|-------|-------|-------|
| `--border-width-none` | `0` | No border |
| `--border-width-thin` | `1px` | Standard borders, subtle dividers |
| `--border-width-medium` | `2px` | Emphasis, focus states |
| `--border-width-thick` | `3px` | Strong emphasis, active states |

### Opacity

| Token | Value | Usage |
|-------|-------|-------|
| `--opacity-0` | `0` | Invisible elements |
| `--opacity-25` | `0.25` | Very faint elements, backgrounds |
| `--opacity-50` | `0.5` | Disabled states, placeholders |
| `--opacity-75` | `0.75` | Semi-prominent elements |
| `--opacity-100` | `1` | Fully visible elements |

### Z-Index Scale

| Token | Value | Usage |
|-------|-------|-------|
| `--z-index-behind` | `-1` | Positioned behind standard content |
| `--z-index-base` | `0` | Default stacking context |
| `--z-index-raised` | `10` | Raised elements (cards, etc.) |
| `--z-index-dropdown` | `100` | Dropdowns, popovers |
| `--z-index-sticky` | `200` | Sticky elements (headers, etc.) |
| `--z-index-modal` | `300` | Modal dialogs, overlays |
| `--z-index-toast` | `400` | Notifications, toasts |
| `--z-index-tooltip` | `500` | Tooltips |
| `--z-index-critical` | `999` | Critical notifications, errors |

### Transitions

| Token | Value | Usage |
|-------|-------|-------|
| `--transition-fast` | `150ms ease-in-out` | Quick micro-interactions |
| `--transition-normal` | `250ms ease-in-out` | Standard transitions |
| `--transition-slow` | `350ms ease-in-out` | Emphasized transitions |
| `--transition-delay-short` | `50ms` | Brief delay between related animations |
| `--transition-delay-medium` | `100ms` | Standard staggered animations |
| `--transition-delay-long` | `200ms` | Pronounced staggered animations |

---

## Atomic Components

### Atoms

Atoms are the fundamental building blocks of our interface – the basic HTML elements that serve as the foundation for all our components.

#### Buttons

Our button system includes multiple variants to clearly communicate action hierarchy and purpose.

##### Primary Button

```html
<button class="btn btn-primary">Subscribe Now</button>
```

- Purpose: Primary actions, main conversion points
- Properties:
  - Background: `--color-primary-600`
  - Text: `--color-white`
  - Font: `--font-family-body`
  - Weight: `--font-weight-semibold`
  - Size: `--font-size-sm`
  - Padding: `--spacing-sm` vertical, `--spacing-md` horizontal
  - Border-radius: `--radius-md`
  - Transition: `--transition-normal`
  
- States:
  - Hover: Darken background to `--color-primary-700`
  - Active/Pressed: Darken background to `--color-primary-800`, slight inset shadow
  - Disabled: `--opacity-50`, no hover effect
  - Focus: `--shadow-outline` in primary color

##### Secondary Button

```html
<button class="btn btn-secondary">Learn More</button>
```

- Purpose: Secondary actions, alternative choices
- Properties:
  - Background: `--color-white`
  - Text: `--color-primary-700`
  - Border: `--border-width-thin` solid `--color-primary-600`
  - Other properties same as primary

- States:
  - Hover: Background `--color-primary-50`
  - Active/Pressed: Background `--color-primary-100`
  - Disabled: `--opacity-50`, no hover effect
  - Focus: `--shadow-outline` in primary color

##### Tertiary Button

```html
<button class="btn btn-tertiary">View Details</button>
```

- Purpose: Low-emphasis actions, additional options
- Properties:
  - Background: Transparent
  - Text: `--color-primary-700`
  - Border: None
  - Other properties same as primary

- States:
  - Hover: Background `--color-primary-50`
  - Active/Pressed: Background `--color-primary-100`
  - Disabled: `--opacity-50`, no hover effect
  - Focus: `--shadow-outline` in primary color

##### Danger Button

```html
<button class="btn btn-danger">Delete Account</button>
```

- Purpose: Destructive actions, critical warnings
- Properties:
  - Background: `--color-error`
  - Text: `--color-white`
  - Other properties same as primary

- States:
  - Hover: Darken background 10%
  - Active/Pressed: Darken background 15%, slight inset shadow
  - Disabled: `--opacity-50`, no hover effect
  - Focus: `--shadow-outline` in error color

##### Button Sizes

```html
<button class="btn btn-primary btn-sm">Small</button>
<button class="btn btn-primary">Default</button>
<button class="btn btn-primary btn-lg">Large</button>
```

- Small:
  - Font: `--font-size-xs`
  - Padding: `--spacing-xs` vertical, `--spacing-sm` horizontal
  
- Default: 
  - Font: `--font-size-sm`
  - Padding: `--spacing-sm` vertical, `--spacing-md` horizontal
  
- Large:
  - Font: `--font-size-md`
  - Padding: `--spacing-md` vertical, `--spacing-lg` horizontal

##### Button with Icon

```html
<button class="btn btn-primary">
  <span class="icon icon-calendar"></span>
  <span>Schedule Event</span>
</button>
```

- Properties:
  - Icon spacing: `--spacing-xs` between icon and text
  - Icon size: 1.2em relative to button text

#### Form Elements

##### Text Input

```html
<div class="form-group">
  <label for="name">Full Name</label>
  <input type="text" id="name" class="input" placeholder="Enter your full name" />
  <div class="hint">Please provide your legal name as it appears on your ID</div>
</div>
```

- Properties:
  - Background: `--color-white`
  - Border: `--border-width-thin` solid `--color-neutral-300`
  - Text: `--color-neutral-900`
  - Placeholder: `--color-neutral-500`
  - Padding: `--spacing-sm` vertical, `--spacing-md` horizontal
  - Border-radius: `--radius-md`
  - Font: `--font-family-body`
  - Size: `--font-size-md`
  - Line-height: `--line-height-normal`
  
- States:
  - Hover: Border `--color-neutral-400`
  - Focus: Border `--color-primary-600`, `--shadow-outline`
  - Disabled: Background `--color-neutral-100`, `--opacity-50`
  - Error: Border `--color-error`, error message below
  
- Label:
  - Font: `--font-family-body`
  - Weight: `--font-weight-medium`
  - Size: `--font-size-sm`
  - Color: `--color-neutral-800`
  - Margin-bottom: `--spacing-xs`
  
- Hint/Error text:
  - Font: `--font-family-body`
  - Size: `--font-size-xs`
  - Color: `--color-neutral-600` (hint), `--color-error` (error)
  - Margin-top: `--spacing-xs`

##### Select Dropdown

```html
<div class="form-group">
  <label for="state">State</label>
  <select id="state" class="select">
    <option value="">Select your state</option>
    <option value="TX">Texas</option>
    <option value="CA">California</option>
  </select>
</div>
```

- Properties: Same as text input, with added:
  - Icon: Dropdown arrow on right side
  - Padding-right: Increased to accommodate icon

##### Checkbox

```html
<div class="checkbox-group">
  <input type="checkbox" id="subscribe" class="checkbox" />
  <label for="subscribe">Subscribe to newsletter</label>
</div>
```

- Properties:
  - Checkbox size: `20px × 20px`
  - Border: `--border-width-thin` solid `--color-neutral-400`
  - Border-radius: `--radius-sm`
  - Background (checked): `--color-primary-600`
  - Checkmark: White
  - Label spacing: `--spacing-xs` between checkbox and text
  
- States:
  - Hover: Border `--color-primary-500`
  - Focus: `--shadow-outline`
  - Disabled: `--opacity-50`

##### Radio Button

```html
<div class="radio-group">
  <div class="radio-item">
    <input type="radio" id="option1" name="options" class="radio" />
    <label for="option1">Option 1</label>
  </div>
  <div class="radio-item">
    <input type="radio" id="option2" name="options" class="radio" />
    <label for="option2">Option 2</label>
  </div>
</div>
```

- Properties:
  - Radio size: `20px × 20px`
  - Border: `--border-width-thin` solid `--color-neutral-400`
  - Border-radius: `--radius-full`
  - Background (selected): `--color-primary-600`
  - Center dot: White
  - States and layout similar to checkbox

#### Typography Elements

##### Headings

```html
<h1 class="heading-1">Page Title</h1>
<h2 class="heading-2">Section Title</h2>
<h3 class="heading-3">Subsection Title</h3>
<h4 class="heading-4">Group Heading</h4>
<h5 class="heading-5">Minor Heading</h5>
<h6 class="heading-6">Small Heading</h6>
```

- Properties: As defined in Typography Scale Combinations

##### Paragraph Text

```html
<p class="lead">This is a lead paragraph that introduces the main content.</p>
<p>This is standard body text used for the main content.</p>
<p class="small">This is smaller text used for supplementary information.</p>
```

- Properties: As defined in Typography Scale Combinations

##### Links

```html
<a href="#" class="link">Standard text link</a>
<a href="#" class="link link-prominent">Prominent link</a>
```

- Standard link:
  - Color: `--color-primary-600`
  - Text-decoration: None
  - Hover: Text-decoration underline, color `--color-primary-700`
  - Focus: `--shadow-outline`
  
- Prominent link:
  - Font-weight: `--font-weight-medium`
  - Text-decoration: Underline
  - Other properties same as standard link

#### Icons

```html
<span class="icon icon-small icon-search"></span>
<span class="icon icon-medium icon-calendar"></span>
<span class="icon icon-large icon-home"></span>
```

- Icon System: Standardized set of SVG icons
- Sizes:
  - Small: `16px × 16px`
  - Medium: `24px × 24px`
  - Large: `32px × 32px`
- Colors inherit from text color by default
- Specific color classes available (e.g., `icon-primary`, `icon-success`)

#### Labels & Badges

```html
<span class="label">Category</span>
<span class="badge badge-primary">New</span>
<span class="badge badge-success">Approved</span>
<span class="badge badge-warning">Pending</span>
<span class="badge badge-error">Rejected</span>
<span class="badge badge-info">Featured</span>
```

- Label:
  - Font: `--font-family-body`
  - Size: `--font-size-xs`
  - Weight: `--font-weight-medium`
  - Color: `--color-neutral-700`
  - Background: `--color-neutral-100`
  - Padding: `--spacing-2xs` vertical, `--spacing-xs` horizontal
  - Border-radius: `--radius-md`
  
- Badge:
  - Font: `--font-family-body`
  - Size: `--font-size-2xs`
  - Weight: `--font-weight-medium`
  - Letter-spacing: `--letter-spacing-wide`
  - Text-transform: Uppercase
  - Padding: `--spacing-2xs` vertical, `--spacing-xs` horizontal
  - Border-radius: `--radius-full`
  - Colors based on semantic variants (primary, success, etc.)

#### Dividers

```html
<hr class="divider" />
<hr class="divider divider-light" />
<div class="divider-with-text"><span>OR</span></div>
```

- Standard divider:
  - Height: `1px`
  - Background: `--color-neutral-200`
  - Margin: `--spacing-lg` vertical
  
- Light divider:
  - Background: `--color-neutral-100`
  
- Divider with text:
  - Text centered with lines extending on both sides
  - Font: `--font-size-xs`, `--color-neutral-500`
  - Line style same as standard divider

### Molecules

Molecules combine atoms to create more complex, functional components that serve specific purposes in the interface.

#### Search Bar

```html
<div class="search-bar">
  <span class="icon icon-search"></span>
  <input type="text" placeholder="Search directory..." class="search-input" />
  <button class="btn btn-tertiary btn-sm">Search</button>
</div>
```

- Properties:
  - Container: Display flex, align items center
  - Background: `--color-white`
  - Border: `--border-width-thin` solid `--color-neutral-300`
  - Border-radius: `--radius-md`
  - Icon: `--color-neutral-500`, positioned left with `--spacing-sm` padding
  - Input: Flex grow, border none, focus ring none
  - Button: Optional, right-aligned

#### Navigation Item

```html
<a href="#" class="nav-item">
  <span class="icon icon-home"></span>
  <span class="nav-text">Home</span>
</a>
```

- Properties:
  - Display: Flex, align items center
  - Padding: `--spacing-sm` vertical, `--spacing-md` horizontal
  - Font: `--font-family-body`
  - Size: `--font-size-sm`
  - Weight: `--font-weight-medium`
  - Color: `--color-neutral-700`
  - Icon spacing: `--spacing-xs` right margin
  
- States:
  - Hover: Background `--color-primary-50`, color `--color-primary-700`
  - Active: Background `--color-primary-100`, color `--color-primary-800`
  - Current: Background `--color-primary-100`, color `--color-primary-800`, left border `--color-primary-600`

#### Card

```html
<div class="card">
  <div class="card-header">
    <h3 class="card-title">Card Title</h3>
  </div>
  <div class="card-body">
    <p>Card content goes here.</p>
  </div>
  <div class="card-footer">
    <button class="btn btn-secondary btn-sm">Action</button>
  </div>
</div>
```

- Properties:
  - Background: `--color-white`
  - Border: `--border-width-thin` solid `--color-neutral-200`
  - Border-radius: `--radius-lg`
  - Shadow: `--shadow-sm`
  - Transition: `--transition-normal`
  
- Header:
  - Padding: `--spacing-md`
  - Border-bottom: `--border-width-thin` solid `--color-neutral-100`
  - Title: `--font-size-lg`, `--font-weight-semibold`, `--color-neutral-900`
  
- Body:
  - Padding: `--spacing-md`
  
- Footer:
  - Padding: `--spacing-md`
  - Border-top: `--border-width-thin` solid `--color-neutral-100`
  - Display: Flex, justify-content flex-end

- States:
  - Hover: `--shadow-md`
  - Interactive: Cursor pointer

#### Alert

```html
<div class="alert alert-info">
  <span class="icon icon-info"></span>
  <div class="alert-content">
    <div class="alert-title">Information</div>
    <div class="alert-message">This is an informational message.</div>
  </div>
  <button class="alert-close">
    <span class="icon icon-close"></span>
  </button>
</div>
```

- Base Properties:
  - Display: Flex, align items flex-start
  - Padding: `--spacing-md`
  - Border-radius: `--radius-md`
  - Border-left: `--border-width-thick` solid (variant color)
  
- Variants:
  - Info: Background `--color-info-light`, border `--color-info`
  - Success: Background `--color-success-light`, border `--color-success`
  - Warning: Background `--color-warning-light`, border `--color-warning`
  - Error: Background `--color-error-light`, border `--color-error`
  
- Icon:
  - Size: `24px × 24px`
  - Color: Variant color
  - Margin-right: `--spacing-sm`
  
- Content:
  - Flex grow
  
- Title:
  - Font-weight: `--font-weight-semibold`
  - Margin-bottom: `--spacing-2xs`
  
- Close button:
  - Color: `--color-neutral-500`
  - Hover: `--color-neutral-700`

#### Form Group

```html
<div class="form-group">
  <label for="email">Email Address</label>
  <div class="input-wrapper">
    <span class="icon icon-email"></span>
    <input type="email" id="email" class="input" placeholder="Enter your email" />
  </div>
  <div class="hint">We'll never share your email with anyone else</div>
</div>
```

- Properties:
  - Margin-bottom: `--spacing-md`
  
- Input wrapper:
  - Position: Relative
  - Display: Flex, align items center
  
- Icon:
  - Position: Absolute, left
  - Padding-left: When icon present, add `--spacing-xl`
  - Color: `--color-neutral-500`

#### Tag Group

```html
<div class="tag-group">
  <div class="tag">Local News</div>
  <div class="tag">Community</div>
  <div class="tag">Events</div>
  <div class="tag-more">+2 more</div>
</div>
```

- Tag Group:
  - Display: Flex, gap `--spacing-xs`
  - Flex-wrap: Wrap
  
- Tag:
  - Background: `--color-neutral-100`
  - Color: `--color-neutral-700`
  - Font-size: `--font-size-xs`
  - Padding: `--spacing-2xs` vertical, `--spacing-xs` horizontal
  - Border-radius: `--radius-full`
  
- Tag More:
  - Similar to tag but with `--color-primary-100` background and `--color-primary-700` text

#### Pagination

```html
<div class="pagination">
  <a href="#" class="pagination-item pagination-prev">
    <span class="icon icon-chevron-left"></span>
    <span>Previous</span>
  </a>
  <a href="#" class="pagination-item">1</a>
  <a href="#" class="pagination-item pagination-current">2</a>
  <a href="#" class="pagination-item">3</a>
  <span class="pagination-ellipsis">...</span>
  <a href="#" class="pagination-item">12</a>
  <a href="#" class="pagination-item pagination-next">
    <span>Next</span>
    <span class="icon icon-chevron-right"></span>
  </a>
</div>
```

- Container:
  - Display: Flex, align items center, justify-content center
  - Gap: `--spacing-xs`
  
- Pagination item:
  - Min-width: `40px`
  - Height: `40px`
  - Display: Flex, align items center, justify-content center
  - Padding: `--spacing-2xs` vertical, `--spacing-xs` horizontal
  - Border-radius: `--radius-md`
  - Font-size: `--font-size-sm`
  - Color: `--color-neutral-700`
  
- States:
  - Hover: Background `--color-primary-50`, color `--color-primary-700`
  - Current: Background `--color-primary-600`, color `--color-white`
  
- Previous/Next:
  - Display text on larger screens, only icons on mobile

#### Breadcrumbs

```html
<nav class="breadcrumbs">
  <ol>
    <li><a href="#">Home</a></li>
    <li><a href="#">Community</a></li>
    <li><a href="#">Events</a></li>
    <li class="breadcrumbs-current">Summer Festival</li>
  </ol>
</nav>
```

- Container:
  - Margin: `--spacing-lg` bottom
  
- List:
  - Display: Flex, flex-wrap wrap
  - List-style: None
  - Padding: 0
  
- Items:
  - Display: Flex, align items center
  - Font-size: `--font-size-sm`
  - Color: `--color-neutral-600`
  
- Separator:
  - Content: "/"
  - Margin: `--spacing-xs` horizontal
  - Color: `--color-neutral-400`
  
- Current:
  - Color: `--color-neutral-900`
  - Font-weight: `--font-weight-medium`

#### Comment

```html
<div class="comment">
  <div class="comment-avatar">
    <img src="avatar.jpg" alt="User Avatar" />
  </div>
  <div class="comment-content">
    <div class="comment-header">
      <span class="comment-author">Jane Smith</span>
      <span class="comment-meta">Posted 2 days ago</span>
    </div>
    <div class="comment-body">
      <p>This is a comment on the article.</p>
    </div>
    <div class="comment-actions">
      <button class="btn btn-tertiary btn-sm">Reply</button>
      <button class="btn btn-tertiary btn-sm">Like</button>
    </div>
  </div>
</div>
```

- Container:
  - Display: Flex
  - Margin-bottom: `--spacing-md`
  
- Avatar:
  - Width/Height: `40px`
  - Border-radius: `--radius-full`
  - Margin-right: `--spacing-sm`
  
- Content:
  - Flex grow
  
- Header:
  - Display: Flex, align items center, justify-content space-between
  - Margin-bottom: `--spacing-xs`
  
- Author:
  - Font-weight: `--font-weight-medium`
  - Color: `--color-neutral-900`
  
- Meta:
  - Font-size: `--font-size-xs`
  - Color: `--color-neutral-500`
  
- Actions:
  - Margin-top: `--spacing-xs`
  - Display: Flex, gap `--spacing-xs`

### Organisms

Organisms are complex components composed of molecules and atoms that form distinct sections of the interface.

#### Navigation Bar

```html
<header class="navbar">
  <div class="navbar-container">
    <div class="navbar-brand">
      <a href="/">
        <img src="logo.svg" alt="Quality Neighbor" class="navbar-logo" />
      </a>
    </div>
    <nav class="navbar-nav">
      <a href="#" class="nav-item nav-item-current">Home</a>
      <a href="#" class="nav-item">Community</a>
      <a href="#" class="nav-item">Events</a>
      <a href="#" class="nav-item">Business Directory</a>
      <a href="#" class="nav-item">About</a>
    </nav>
    <div class="navbar-actions">
      <div class="search-bar navbar-search">
        <span class="icon icon-search"></span>
        <input type="text" placeholder="Search..." class="search-input" />
      </div>
      <button class="btn btn-primary">Subscribe</button>
      <button class="navbar-toggle">
        <span class="icon icon-menu"></span>
      </button>
    </div>
  </div>
</header>
```

- Container:
  - Background: `--color-white`
  - Border-bottom: `--border-width-thin` solid `--color-neutral-200`
  - Box-shadow: `--shadow-sm`
  - Position: Sticky, top 0
  - Z-index: `--z-index-sticky`
  
- Inner container:
  - Max-width: `1200px`
  - Margin: 0 auto
  - Padding: `--spacing-md`
  - Display: Flex, align items center, justify-content space-between
  
- Brand/Logo:
  - Height: `40px`
  - Margin-right: `--spacing-lg`
  
- Navigation:
  - Display: Flex, gap `--spacing-sm`
  - Mobile: Hidden, shown in dropdown
  
- Actions:
  - Display: Flex, align items center, gap `--spacing-md`
  
- Toggle button:
  - Display: None (visible on mobile only)
  - Responsive behavior defined in media queries

#### Footer

```html
<footer class="footer">
  <div class="footer-container">
    <div class="footer-branding">
      <img src="logo.svg" alt="Quality Neighbor" class="footer-logo" />
      <p class="footer-tagline">Your Community, Professionally Delivered</p>
      <div class="social-links">
        <a href="#" class="social-link"><span class="icon icon-facebook"></span></a>
        <a href="#" class="social-link"><span class="icon icon-twitter"></span></a>
        <a href="#" class="social-link"><span class="icon icon-instagram"></span></a>
      </div>
    </div>
    <div class="footer-links">
      <div class="footer-group">
        <h4 class="footer-heading">Navigation</h4>
        <ul class="footer-menu">
          <li><a href="#">Home</a></li>
          <li><a href="#">Community</a></li>
          <li><a href="#">Events</a></li>
          <li><a href="#">Business Directory</a></li>
          <li><a href="#">About</a></li>
        </ul>
      </div>
      <div class="footer-group">
        <h4 class="footer-heading">Legal</h4>
        <ul class="footer-menu">
          <li><a href="#">Terms of Service</a></li>
          <li><a href="#">Privacy Policy</a></li>
          <li><a href="#">Cookie Policy</a></li>
          <li><a href="#">Accessibility</a></li>
        </ul>
      </div>
      <div class="footer-group">
        <h4 class="footer-heading">Contact</h4>
        <ul class="footer-menu">
          <li><a href="#">Email Us</a></li>
          <li><a href="#">Support</a></li>
          <li><a href="#">Advertising</a></li>
          <li><a href="#">FAQ</a></li>
        </ul>
      </div>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="footer-container">
      <p class="copyright">© 2025 Quality Neighbor. All rights reserved.</p>
      <p class="attribution">Made with ♥ for Hartland Ranch</p>
    </div>
  </div>
</footer>
```

- Container:
  - Background: `--color-primary-900`
  - Color: `--color-white`
  - Padding: `--spacing-2xl` top, `--spacing-xl` bottom
  
- Inner container:
  - Max-width: `1200px`
  - Margin: 0 auto
  - Padding: `--spacing-md`
  - Display: Flex, flex-wrap wrap, justify-content space-between
  
- Branding:
  - Width: `25%` (responsive)
  - Logo: Height `40px`, margin-bottom `--spacing-md`
  - Tagline: Font-size `--font-size-sm`, margin-bottom `--spacing-lg`
  
- Links:
  - Display: Flex, flex-wrap wrap, width `75%` (responsive)
  
- Group:
  - Width: `33.33%` (responsive)
  - Padding-right: `--spacing-xl`
  
- Heading:
  - Font-family: `--font-family-heading`
  - Font-size: `--font-size-md`
  - Font-weight: `--font-weight-bold`
  - Margin-bottom: `--spacing-md`
  
- Menu:
  - List-style: None
  - Padding: 0
  - Line-height: `--line-height-relaxed`
  
- Links:
  - Color: `--color-neutral-300`
  - Hover: `--color-white`, text-decoration underline
  
- Social links:
  - Display: Flex, gap `--spacing-sm`
  - Link: `36px` diameter, border-radius `--radius-full`
  - Background: `rgba(255, 255, 255, 0.1)`
  - Hover: `rgba(255, 255, 255, 0.2)`
  
- Footer bottom:
  - Border-top: `1px solid rgba(255, 255, 255, 0.1)`
  - Margin-top: `--spacing-xl`
  - Padding-top: `--spacing-lg`
  - Display: Flex, justify-content space-between
  - Font-size: `--font-size-xs`
  - Color: `--color-neutral-400`

#### Newsletter Article

```html
<article class="article">
  <header class="article-header">
    <div class="article-meta">
      <div class="article-category">Community News</div>
      <time class="article-date">June 7, 2025</time>
    </div>
    <h1 class="article-title">New Community Park Expansion Approved by City Council</h1>
    <div class="article-lead">
      <p>Hartland Ranch residents will soon enjoy expanded recreational facilities following unanimous approval of the park expansion project.</p>
    </div>
  </header>
  <div class="article-image">
    <img src="park-rendering.jpg" alt="Park Expansion Rendering" />
    <div class="article-image-caption">Artist rendering of the expanded community park facilities</div>
  </div>
  <div class="article-content">
    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit...</p>
    <!-- More content paragraphs -->
  </div>
  <footer class="article-footer">
    <div class="article-tags">
      <span class="tag">Parks</span>
      <span class="tag">Development</span>
      <span class="tag">City Council</span>
    </div>
    <div class="article-share">
      <span class="article-share-label">Share:</span>
      <a href="#" class="article-share-link"><span class="icon icon-facebook"></span></a>
      <a href="#" class="article-share-link"><span class="icon icon-twitter"></span></a>
      <a href="#" class="article-share-link"><span class="icon icon-email"></span></a>
    </div>
  </footer>
</article>
```

- Container:
  - Max-width: `800px`
  - Margin: `--spacing-2xl` auto
  
- Header:
  - Margin-bottom: `--spacing-xl`
  
- Meta:
  - Display: Flex, justify-content space-between
  - Margin-bottom: `--spacing-sm`
  - Font-size: `--font-size-sm`
  
- Category:
  - Color: `--color-primary-600`
  - Font-weight: `--font-weight-medium`
  
- Date:
  - Color: `--color-neutral-600`
  
- Title:
  - Font-family: `--font-family-heading`
  - Font-size: `--font-size-3xl` (responsive)
  - Line-height: `--line-height-tight`
  - Margin-bottom: `--spacing-md`
  
- Lead:
  - Font-size: `--font-size-lg`
  - Line-height: `--line-height-relaxed`
  - Color: `--color-neutral-800`
  
- Image:
  - Margin: `--spacing-lg` 0
  - Border-radius: `--radius-md`
  
- Image caption:
  - Font-size: `--font-size-xs`
  - Color: `--color-neutral-600`
  - Margin-top: `--spacing-xs`
  - Text-align: center
  
- Content:
  - Font-size: `--font-size-md`
  - Line-height: `--line-height-relaxed`
  - Color: `--color-neutral-900`
  
  - Paragraphs:
    - Margin-bottom: `--spacing-md`
  
  - Headings within content:
    - Margin-top: `--spacing-xl`
    - Margin-bottom: `--spacing-md`
  
- Footer:
  - Margin-top: `--spacing-xl`
  - Padding-top: `--spacing-lg`
  - Border-top: `--border-width-thin` solid `--color-neutral-200`
  - Display: Flex, justify-content space-between, align-items center
  - Flex-wrap: wrap

#### Business Directory Card

```html
<div class="business-card">
  <div class="business-card-badge">Featured</div>
  <div class="business-card-header">
    <img src="business-logo.jpg" alt="Business Name" class="business-logo" />
    <div class="business-header-content">
      <h3 class="business-name">Martinez Family Bakery</h3>
      <div class="business-category">Food & Dining</div>
    </div>
  </div>
  <div class="business-card-body">
    <p class="business-description">Family-owned bakery specializing in traditional pastries, custom cakes, and fresh bread. Serving Hartland Ranch since 2018.</p>
    <div class="business-details">
      <div class="business-detail">
        <span class="icon icon-location"></span>
        <span>123 Main Street, Hartland Ranch</span>
      </div>
      <div class="business-detail">
        <span class="icon icon-phone"></span>
        <span>(555) 123-4567</span>
      </div>
      <div class="business-detail">
        <span class="icon icon-clock"></span>
        <span>Mon-Sat: 7am-6pm, Sun: 8am-2pm</span>
      </div>
    </div>
  </div>
  <div class="business-card-footer">
    <div class="business-tags">
      <span class="tag">Bakery</span>
      <span class="tag">Cakes</span>
      <span class="tag">Catering</span>
    </div>
    <a href="#" class="btn btn-primary btn-sm">Visit Website</a>
  </div>
</div>
```

- Container:
  - Position: Relative
  - Background: `--color-white`
  - Border: `--border-width-thin` solid `--color-neutral-200`
  - Border-radius: `--radius-lg`
  - Box-shadow: `--shadow-sm`
  - Transition: `--transition-normal`
  - Hover: `--shadow-md`
  
- Badge:
  - Position: Absolute, top right
  - Background: `--color-primary-600`
  - Color: `--color-white`
  - Font-size: `--font-size-xs`
  - Font-weight: `--font-weight-medium`
  - Padding: `--spacing-2xs` vertical, `--spacing-xs` horizontal
  - Border-radius: `0 ${--radius-lg} 0 ${--radius-md}`
  
- Header:
  - Padding: `--spacing-md`
  - Border-bottom: `--border-width-thin` solid `--color-neutral-100`
  - Display: Flex, align items center
  
- Logo:
  - Width: `60px`
  - Height: `60px`
  - Border-radius: `--radius-md`
  - Object-fit: Cover
  - Margin-right: `--spacing-md`
  
- Business name:
  - Font-family: `--font-family-heading`
  - Font-size: `--font-size-lg`
  - Margin-bottom: `--spacing-2xs`
  
- Category:
  - Font-size: `--font-size-sm`
  - Color: `--color-neutral-600`
  
- Body:
  - Padding: `--spacing-md`
  
- Description:
  - Margin-bottom: `--spacing-md`
  
- Details:
  - Font-size: `--font-size-sm`
  
- Detail:
  - Display: Flex, align items center
  - Margin-bottom: `--spacing-xs`
  
  - Icon:
    - Color: `--color-primary-600`
    - Margin-right: `--spacing-xs`
  
- Footer:
  - Padding: `--spacing-md`
  - Border-top: `--border-width-thin` solid `--color-neutral-100`
  - Display: Flex, justify-content space-between, align-items center

#### Event Card

```html
<div class="event-card">
  <div class="event-date">
    <div class="event-month">JUN</div>
    <div class="event-day">12</div>
  </div>
  <div class="event-content">
    <h3 class="event-title">Summer Block Party</h3>
    <div class="event-meta">
      <div class="event-time">
        <span class="icon icon-clock"></span>
        <span>5:00 PM - 9:00 PM</span>
      </div>
      <div class="event-location">
        <span class="icon icon-location"></span>
        <span>Community Park</span>
      </div>
    </div>
    <p class="event-description">Join your neighbors for our annual summer celebration with food trucks, live music, and activities for all ages.</p>
    <div class="event-footer">
      <button class="btn btn-primary btn-sm">RSVP</button>
      <button class="btn btn-secondary btn-sm">Add to Calendar</button>
    </div>
  </div>
</div>
```

- Container:
  - Display: Flex
  - Background: `--color-white`
  - Border: `--border-width-thin` solid `--color-neutral-200`
  - Border-radius: `--radius-lg`
  - Box-shadow: `--shadow-sm`
  - Transition: `--transition-normal`
  - Hover: `--shadow-md`
  
- Date:
  - Width: `80px`
  - Background: `--color-primary-600`
  - Color: `--color-white`
  - Border-radius: `--radius-lg 0 0 --radius-lg`
  - Display: Flex
  - Flex-direction: Column
  - Justify-content: Center
  - Align-items: Center
  - Padding: `--spacing-md`
  
- Month:
  - Font-size: `--font-size-sm`
  - Font-weight: `--font-weight-bold`
  - Text-transform: Uppercase
  
- Day:
  - Font-size: `--font-size-3xl`
  - Font-weight: `--font-weight-bold`
  - Line-height: 1
  
- Content:
  - Padding: `--spacing-md`
  - Flex-grow: 1
  
- Title:
  - Font-family: `--font-family-heading`
  - Font-size: `--font-size-xl`
  - Margin-bottom: `--spacing-xs`
  
- Meta:
  - Display: Flex
  - Gap: `--spacing-md`
  - Margin-bottom: `--spacing-sm`
  - Font-size: `--font-size-sm`
  - Color: `--color-neutral-700`
  
- Time/Location:
  - Display: Flex
  - Align-items: Center
  
  - Icon:
    - Color: `--color-primary-600`
    - Margin-right: `--spacing-xs`
  
- Description:
  - Margin-bottom: `--spacing-md`
  
- Footer:
  - Display: Flex
  - Gap: `--spacing-sm`

#### Community Need Card

```html
<div class="need-card">
  <div class="need-header">
    <div class="need-author">
      <img src="avatar.jpg" alt="User Avatar" class="need-avatar" />
      <div class="need-author-info">
        <div class="need-author-name">Michael Thompson</div>
        <div class="need-meta">Posted 2 days ago</div>
      </div>
    </div>
    <div class="need-category">
      <span class="label">Request</span>
    </div>
  </div>
  <div class="need-content">
    <h3 class="need-title">Looking for Lawn Care Recommendations</h3>
    <p class="need-description">We just moved to Hartland Ranch and need recommendations for reliable lawn care services. Preferably someone who offers organic options and can handle regular maintenance.</p>
  </div>
  <div class="need-footer">
    <div class="need-stats">
      <div class="need-stat">
        <span class="icon icon-comment"></span>
        <span>8 responses</span>
      </div>
    </div>
    <button class="btn btn-primary btn-sm">Respond</button>
  </div>
</div>
```

- Container:
  - Background: `--color-white`
  - Border: `--border-width-thin` solid `--color-neutral-200`
  - Border-radius: `--radius-lg`
  - Box-shadow: `--shadow-sm`
  
- Header:
  - Padding: `--spacing-md`
  - Border-bottom: `--border-width-thin` solid `--color-neutral-100`
  - Display: Flex
  - Justify-content: Space-between
  - Align-items: Center
  
- Author:
  - Display: Flex
  - Align-items: Center
  
- Avatar:
  - Width/Height: `40px`
  - Border-radius: `--radius-full`
  - Margin-right: `--spacing-sm`
  
- Author info:
  - Font-size: `--font-size-sm`
  
- Author name:
  - Font-weight: `--font-weight-medium`
  - Color: `--color-neutral-900`
  
- Meta:
  - Color: `--color-neutral-500`
  - Font-size: `--font-size-xs`
  
- Content:
  - Padding: `--spacing-md`
  
- Title:
  - Font-family: `--font-family-heading`
  - Font-size: `--font-size-lg`
  - Margin-bottom: `--spacing-sm`
  
- Description:
  - Color: `--color-neutral-800`
  
- Footer:
  - Padding: `--spacing-md`
  - Border-top: `--border-width-thin` solid `--color-neutral-100`
  - Display: Flex
  - Justify-content: Space-between
  - Align-items: Center
  
- Stats:
  - Font-size: `--font-size-sm`
  - Color: `--color-neutral-600`
  
- Stat:
  - Display: Flex
  - Align-items: Center
  
  - Icon:
    - Margin-right: `--spacing-xs`

### Templates

Templates arrange organisms, molecules, and atoms into page-level structures without specific content.

#### Newsletter Template

```html
<div class="newsletter-template">
  <header class="newsletter-header">
    <div class="newsletter-brand">
      <img src="logo.svg" alt="Quality Neighbor" class="newsletter-logo" />
      <div class="newsletter-info">
        <h1 class="newsletter-title">Hartland Ranch Community Newsletter</h1>
        <div class="newsletter-meta">June 7, 2025 | Volume 3, Issue 24</div>
      </div>
    </div>
    <div class="newsletter-weather">
      <div class="weather-icon">
        <span class="icon icon-sun"></span>
      </div>
      <div class="weather-info">
        <div class="weather-temp">72°F</div>
        <div class="weather-forecast">Sunny, High 78°F</div>
      </div>
    </div>
  </header>

  <nav class="newsletter-nav">
    <div class="nav-item">Community News</div>
    <div class="nav-item">Events</div>
    <div class="nav-item">Local Business</div>
    <div class="nav-item">Neighbor Needs</div>
    <div class="nav-item">HOA Updates</div>
  </nav>

  <div class="newsletter-highlight">
    <!-- Feature article placeholder -->
  </div>

  <div class="newsletter-grid">
    <div class="newsletter-main">
      <section class="newsletter-section">
        <div class="section-header">
          <h2 class="section-title">Community News</h2>
        </div>
        <div class="section-content">
          <!-- Article placeholders -->
        </div>
      </section>

      <section class="newsletter-section">
        <div class="section-header">
          <h2 class="section-title">Upcoming Events</h2>
        </div>
        <div class="section-content">
          <!-- Event placeholders -->
        </div>
      </section>
    </div>

    <aside class="newsletter-sidebar">
      <section class="sidebar-section">
        <div class="section-header">
          <h3 class="section-title">Community Resources</h3>
        </div>
        <div class="section-content">
          <!-- Resource links placeholder -->
        </div>
      </section>

      <section class="sidebar-section">
        <div class="section-header">
          <h3 class="section-title">Business Spotlight</h3>
        </div>
        <div class="section-content">
          <!-- Business spotlight placeholder -->
        </div>
      </section>

      <section class="sidebar-section">
        <div class="section-header">
          <h3 class="section-title">Neighbor Needs</h3>
        </div>
        <div class="section-content">
          <!-- Neighbor needs placeholder -->
        </div>
      </section>
    </aside>
  </div>

  <footer class="newsletter-footer">
    <div class="footer-info">
      <p>Quality Neighbor | Hartland Ranch Community Newsletter</p>
      <p>Contact: editor@qualityneighbor.com | (555) 123-4567</p>
    </div>
    <div class="footer-links">
      <a href="#">Subscribe</a>
      <a href="#">Website</a>
      <a href="#">Archive</a>
      <a href="#">Submit Content</a>
    </div>
  </footer>
</div>
```

- Newsletter template styles would define the layout structure, spacing, and responsive behavior without specific content styles.

#### Business Directory Template

```html
<div class="directory-template">
  <header class="page-header">
    <h1 class="page-title">Hartland Ranch Business Directory</h1>
    <p class="page-description">Discover and support quality local businesses in our community.</p>
  </header>

  <div class="directory-actions">
    <div class="directory-search">
      <!-- Search component placeholder -->
    </div>
    <div class="directory-filters">
      <!-- Filter components placeholder -->
    </div>
  </div>

  <div class="directory-categories">
    <!-- Category navigation placeholder -->
  </div>

  <div class="directory-grid">
    <!-- Business card placeholders -->
  </div>

  <div class="directory-pagination">
    <!-- Pagination component placeholder -->
  </div>
</div>
```

- Directory template styles would define the layout structure, grid system, and responsive behavior without specific business card styles.

#### Community Profile Template

```html
<div class="profile-template">
  <div class="profile-header">
    <div class="profile-cover">
      <!-- Cover image placeholder -->
    </div>
    <div class="profile-basics">
      <div class="profile-avatar">
        <!-- Avatar placeholder -->
      </div>
      <div class="profile-info">
        <h1 class="profile-name"><!-- Name placeholder --></h1>
        <div class="profile-meta">
          <!-- Meta information placeholder -->
        </div>
      </div>
      <div class="profile-actions">
        <!-- Action buttons placeholder -->
      </div>
    </div>
  </div>

  <div class="profile-navigation">
    <!-- Profile navigation tabs placeholder -->
  </div>

  <div class="profile-content">
    <div class="profile-main">
      <!-- Main content section placeholder -->
    </div>
    <aside class="profile-sidebar">
      <!-- Sidebar content placeholder -->
    </aside>
  </div>
</div>
```

- Profile template styles would define the layout structure, spacing, and responsive behavior without specific content styles.

### Pages

Pages are specific instances of templates with real content representing the final interface.

- **Newsletter Page**: Complete newsletter with actual articles, events, and business features
- **Business Directory Page**: Directory with filter options and actual business listings
- **Community Profile Page**: Member profile with actual content and activity history
- **Event Calendar Page**: Calendar view with actual community events
- **Homepage**: Main entry point with featured content from various sections

---

## Implementation Guidelines

### CSS Architecture

Quality Neighbor's design system will be implemented using a modular CSS architecture following these principles:

1. **Component-Based**: Each UI component has its own self-contained styles
2. **Namespaced**: CSS classes follow a consistent naming convention
3. **Hierarchical**: Styles match the atomic design hierarchy
4. **Responsive**: All components adapt to different screen sizes
5. **Performance-Focused**: Minimize CSS size and complexity

#### CSS Variables Implementation

```css
:root {
  /* Color Variables */
  --color-primary-900: #062C43;
  --color-primary-800: #113A5D;
  /* All other design tokens as CSS variables */
}
```

#### Responsive Breakpoints

```css
/* Mobile First Approach */
/* Base styles for mobile */

/* Small tablets and large phones */
@media (min-width: 640px) {
  /* Small screen adjustments */
}

/* Tablets and small laptops */
@media (min-width: 768px) {
  /* Medium screen adjustments */
}

/* Laptops and desktops */
@media (min-width: 1024px) {
  /* Large screen adjustments */
}

/* Large desktops */
@media (min-width: 1280px) {
  /* Extra large screen adjustments */
}
```

### Design System Integration

#### Design Tool Setup

1. **Figma Component Library**:
   - Create component library with all atoms, molecules, and organisms
   - Set up design tokens as Figma variables
   - Document component usage and variants
   - Create reusable templates and page examples

2. **Developer Handoff**:
   - Export component specifications
   - Document component behavior and interactions
   - Provide responsive behavior guidelines
   - Create implementation checklist

#### Development Implementation

1. **CSS Framework**:
   - Implement design tokens as CSS variables
   - Create utility classes for common patterns
   - Build component library following atomic structure
   - Set up responsive mixins and functions

2. **Component Documentation**:
   - Create living style guide
   - Document component usage with examples
   - Provide code snippets for implementation
   - Include accessibility requirements

3. **Quality Assurance**:
   - Cross-browser testing
   - Responsive behavior validation
   - Accessibility compliance checking
   - Performance optimization

---

## Accessibility Guidelines

Quality Neighbor's design system is built with accessibility as a core requirement, ensuring all components meet WCAG 2.1 AA standards:

### Color & Contrast

- Maintain minimum 4.5:1 contrast ratio for normal text
- Maintain minimum 3:1 contrast ratio for large text
- Never use color alone to convey meaning
- Provide sufficient contrast between UI elements

### Typography & Readability

- Ensure text can be resized up to 200% without loss of functionality
- Maintain appropriate line length and spacing for readability
- Use relative units (rem) for font sizes to respect user preferences
- Provide clear heading hierarchy and consistent text styles

### Component-Specific Guidelines

- **Buttons & Controls**: Clear focus states, descriptive text, appropriate sizing
- **Forms**: Associated labels, clear error messages, logical tab order
- **Navigation**: Multiple navigation methods, skip links, consistent patterns
- **Cards & Containers**: Logical reading order, sufficient spacing, clear boundaries
- **Media**: Alternative text, captions, transcripts, non-autoplaying content

### Keyboard Navigation

- All interactive elements are focusable and operable via keyboard
- Focus order follows logical reading sequence
- Focus states are clearly visible
- No keyboard traps
- Custom components follow WAI-ARIA authoring practices

---

## Conclusion

The Quality Neighbor Atomic Design System provides a comprehensive framework for creating consistent, cohesive user interfaces that embody our brand values: professional, trustworthy, community-focused, and purposeful. By following this system, we ensure that all touchpoints provide a unified experience that strengthens our brand identity and delivers on our promise: Your Community, Professionally Delivered.

This living document will evolve as our platform grows, with regular updates to reflect new components, patterns, and best practices. All team members are encouraged to contribute to the ongoing development and refinement of this design system to maintain its relevance and effectiveness.