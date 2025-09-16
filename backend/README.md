# Boneca Backend

FastAPI-based backend service for the Boneca dance school management system.

## Technology Stack

- **Python 3.13+** - Modern Python with latest features
- **FastAPI** - High-performance web framework
- **Pydantic** - Data validation and settings management
- **Poetry** - Dependency management
- **Docker** - Containerization
- **pytest** - Testing framework
- **mypy** - Static type checking
- **Black** - Code formatting
- **isort** - Import sorting
- **flake8** - Code linting

## Quick Start

1. **Prerequisites:**
   - Docker and Docker Compose
   - Make

2. **Start development server:**
   ```bash
   make run-dev
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/api/v1/docs
   - Health Check: http://localhost:8000/api/v1/ping

## Development Commands

### Essential Commands
```bash
# Start development environment
make run-dev

# Run complete code quality pipeline
make commit-ready

# Run tests with coverage
make test

# View logs
make logs

# Clean up everything
make clean
```

### Code Quality
```bash
# Format code (Black + isort)
make format-backend

# Run linters (flake8 + mypy + Black check + isort check)
make lint-backend

# Format only changed files
make format-branch

# Lint only changed files
make lint-branch
```

### Testing
```bash
# Run all tests
make test

# Run tests in watch mode
make test-watch-backend
```

### Container Management
```bash
# Build containers
make build-backend

# Attach to container
make attach

# Check container status
make status

# Stop and clean everything
make clean
```

## Project Structure

```
backend/
├── src/                    # Application source code
│   ├── api/               # API routes and routers
│   │   ├── router.py      # Main API router
│   │   └── v1/           # API version 1
│   │       ├── healthcheck.py
│   │       └── users.py
│   ├── core/             # Core functionality
│   │   ├── config.py     # Application configuration
│   │   ├── exceptions.py # Custom exceptions
│   │   └── repositories/ # Data access layer
│   └── domain/           # Domain models and schemas
│       └── users/
├── tests/                # Test files
├── docs/                 # Documentation
│   ├── ARCHITECTURE.md
│   ├── LOCAL_DEVELOPMENT.md
│   └── EXAMPLE_REQUESTS.md
├── docker-compose.yml    # Docker services
├── Dockerfile           # Production container
├── Dockerfile.dev       # Development container
├── Makefile            # Development commands
└── pyproject.toml      # Python dependencies
```

## API Endpoints

- `GET /` - Welcome message
- `GET /api/v1/ping` - Health check
- `POST /api/v1/users` - Create user
- `GET /api/v1/users` - List users
- `GET /api/v1/users/{user_id}` - Get user by ID

For detailed API documentation, visit http://localhost:8000/api/v1/docs

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - Project structure and design decisions
- [Local Development](docs/LOCAL_DEVELOPMENT.md) - Detailed development setup
- [Example API Requests](docs/EXAMPLE_REQUESTS.md) - API usage examples

## Code Quality Standards

This project maintains high code quality standards with:

- **100% test coverage** - All code must be tested
- **Type safety** - mypy static type checking
- **Code formatting** - Black and isort for consistent style
- **Linting** - flake8 for code quality
- **CI/CD** - Automated testing and linting

Use `make commit-ready` to run the complete quality pipeline! 🦸

## Contributing

1. Make your changes
2. Run `make commit-ready` to ensure code quality
3. All tests must pass with 100% coverage
4. Follow the existing code style and patterns

## Environment Variables

See [Local Development Guide](docs/LOCAL_DEVELOPMENT.md) for environment configuration.

## License

MIT License - see ../LICENSE file for details.