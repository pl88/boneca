# Local Development Guide

## Prerequisites

- Docker and Docker Compose
- Make
- Git
- VS Code (recommended)

## Initial Setup

1. Clone the repository:
   ```bash
   git clone git@github.com:pl88/boneca.git
   cd boneca
   ```

2. Start the development environment:
   ```bash
   cd backend
   make run-dev
   ```

## Development Workflow

### Starting the Development Server

```bash
# Start in detached mode
make run-dev

# View logs
make logs

# Check status
make status

# Attach to container
make attach

# Stop and clean up
make clean
```

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
make test-backend PYTEST_ARGS="tests/domain/users/test_repository.py"

# Run with coverage
make test-backend PYTEST_ARGS="--cov=src"
```

### Code Quality

```bash
# Format code
make format-backend

# Lint code
make lint-backend

# Format and lint only changed files
make format-branch
make lint-branch
```

### Managing Dependencies

```bash
# Add a new dependency
make poetry-add-backend ARGS="package-name"

# Add a dev dependency
make poetry-add-backend ARGS="--dev package-name"

# Update dependencies
make poetry-update-backend

# Generate/update lock file
make poetry-lock-backend
```

## Environment Variables

Development environment variables are loaded from `.env` file. Copy `.env.example` to `.env` and adjust as needed:

```bash
cp .env.example .env
```

Available environment variables:
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password
- `POSTGRES_DB` - Database name
- `DATABASE_URL` - Full database connection URL
- `API_DEBUG` - Enable debug mode (true/false)

## VS Code Setup

Recommended extensions:
- Python
- Pylance
- Docker
- YAML
- Even Better TOML
- autoDocstring

Recommended settings (`settings.json`):
```json
{
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

## Debugging

1. Start the development server:
   ```bash
   make run-dev
   ```

2. Attach VS Code debugger:
   - Open Command Palette (Ctrl+Shift+P)
   - Select "Python: Attach"
   - Choose the running container

3. Set breakpoints and debug as usual

## Common Issues

### Poetry Lock Issues
If you encounter Poetry lock issues:
```bash
make clean
make poetry-lock-backend
make run-dev
```

### Docker Permission Issues
If you encounter permission issues with Docker:
```bash
# Add your user to docker group
sudo usermod -aG docker $USER
# Log out and log back in
```

### Hot Reload Not Working
If hot reload stops working:
```bash
make clean
make run-dev
```

## Best Practices

1. Always use Makefile commands
2. Keep the development environment containerized
3. Write tests for new features
4. Follow the project's architecture (see ARCHITECTURE.md)
5. Format and lint code before committing
6. Update documentation when making significant changes

## Need Help?

- Check ARCHITECTURE.md for project structure
- Check EXAMPLE_REQUESTS.md for API examples
- Read the FastAPI documentation
- Ask the team!
