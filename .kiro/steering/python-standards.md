---
inclusion: always
---

# Python Project Standards

## Code Style
- Follow PEP 8 conventions
- Use type hints for function parameters and return values
- Maximum line length: 88 characters (Black formatter standard)
- Use meaningful variable and function names

## Flask Best Practices
- Always include error handling for routes
- Use blueprints for organizing larger applications
- Include logging for debugging and monitoring
- Environment variables for configuration (never hardcode secrets)

## Dependencies
- Pin exact versions in requirements.txt for reproducibility
- Keep dependencies minimal and up-to-date
- Use virtual environments for isolation

## Testing
- Write tests for all endpoints
- Include unit tests and integration tests
- Aim for >80% code coverage

## Deployment
- Use Gunicorn or uWSGI for production
- Never run Flask development server in production
- Include health check endpoints
- Use environment-specific configuration
