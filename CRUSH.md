# CRUSH Development Guidelines

## Build Commands
- `npm run build` - Build the frontend for production
- `npm run start` - Start the development server
- `uvicorn main:app --reload` - Start the backend dev server (from backend/)

## Test Commands
- `npm run test` - Run all tests
- `npm run test -- --watch` - Run tests in watch mode
- `npm run test -- src/App.test.js` - Run a single test file
- `npm run test -- --testNamePattern="pattern"` - Run tests matching a pattern

## Lint/Format Commands
- `npx eslint src/` - Lint JavaScript files
- `npx eslint src/ --fix` - Fix linting issues automatically

## Code Style Guidelines

### JavaScript/React
- Use functional components with hooks
- Use camelCase for variables and functions
- Use PascalCase for components
- Destructure props in function parameters when possible
- Use async/await instead of .then() for asynchronous operations
- Import React hooks and components at the top of the file
- Use Tailwind CSS classes for styling

### Python/FastAPI
- Use snake_case for variables and functions
- Follow PEP 8 style guide
- Use type hints where possible
- Use descriptive variable names

### General
- Use meaningful variable and function names
- Keep functions small and focused
- Add comments for complex logic
- Handle errors appropriately
- Use .env files for configuration
- Keep dependencies minimal

## Tools
- Frontend: React, Tailwind CSS, Axios
- Backend: FastAPI
- Testing: Jest, React Testing Library