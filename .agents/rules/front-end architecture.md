---
trigger: always_on
---

# The Ultimate Frontend Development Guide: Principles, Patterns, and Practices

## Development Philosophy

- **First Principles**: Embrace SOLID principles, KISS (Keep It Simple, Stupid), and DRY (Don't Repeat Yourself)
- **Vanilla First**: Favor pure HTML, CSS, and JavaScript without heavy frameworks to ensure a lightweight footprint.
- **Component-Driven Development**: Build applications as compositions of well-defined, reusable HTML/JS modules.
- **Think Then Code**: Begin with step-by-step planning and detailed pseudocode before implementation.

## Code Architecture & Structure

### Project Organization
- Use lowercase with dashes for directories (`components/auth-wizard/`)
- Structure files consistently:
  - `index.html` for markup
  - `styles.css` for styling
  - `app.js` for logic

### Naming Conventions

- **camelCase** for:
  - Variables, functions, methods
  - DOM element references

- **Descriptive Prefixes**:
  - Prefix event handlers with 'handle': `handleClick`, `handleSubmit`
  - Prefix boolean variables with verbs: `isLoading`, `hasError`, `canSubmit`

## JavaScript Implementation

- Enable strict mode (`'use strict';`)
- Use ES6+ features (const/let, arrow functions, template literals)
- Use type guards and defensive programming for null/undefined values.
- Keep the global scope clean by using modules or IIFE (Immediately Invoked Function Expressions).

## UI and Styling

- Use pure CSS for utility-first, maintainable styling. Do NOT use Tailwind CSS or any heavy CSS framework.
- Design with mobile-first, responsive principles.
- Implement dark mode using CSS variables.
- Maintain consistent spacing values and design tokens.
- Use CSS transitions and animations instead of JavaScript libraries.

## Error Handling - The Art of Graceful Failures

### The Early Return Pattern

- Handle errors and edge cases at the beginning of functions
- Use early returns for error conditions
- Place the happy path last in the function
- Avoid unnecessary else statements; use if-return pattern instead

### Structured Error Handling

- Provide user-friendly error messages
- Log errors appropriately for debugging

## Form Validation

- Use native HTML5 form validation attributes (`required`, `pattern`, `min`, `max`).
- Implement custom validation logic in Vanilla JS using the Constraint Validation API.

## State Management

- Use simple JavaScript objects or classes for state management.
- Keep state localized to the components that need it.

## Accessibility (a11y)

- Use semantic HTML elements
- Apply appropriate ARIA attributes only when necessary
- Ensure keyboard navigation support
- Maintain accessible color contrast ratios
- Follow a logical heading hierarchy
- Provide clear and accessible error feedback
- Test with screen readers