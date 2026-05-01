# Frontend Tech Stack

This document defines the strictly enforced frontend technology stack for the VoteAssist application.

## Core Technologies
- **HTML5**: For semantic structuring of the application UI.
- **Vanilla JavaScript (ES6+)**: For DOM manipulation, API interactions, and client-side logic.
- **Vanilla CSS3**: For all styling, utilizing CSS variables, Flexbox, and CSS Grid for layout.

## Excluded Technologies
To comply with the <1 MB repository constraint and ensure a lightweight footprint, the following technologies are **strictly prohibited**:
- Frontend frameworks and libraries (e.g., React, Next.js, Angular, Vue, Svelte).
- CSS frameworks and utility libraries (e.g., Tailwind CSS, Bootstrap, Bulma).
- UI component libraries (e.g., Shadcn, Radix UI, Material UI).

## Principles
1. **Lightweight & Fast**: Minimize asset sizes to ensure rapid loading even on low-bandwidth networks.
2. **Accessible**: Rely on semantic HTML and native attributes to maintain high accessibility standards.
3. **Maintainable**: Keep styles organized using standard CSS practices and variables, and modularize JavaScript using simple functions or ES modules.
