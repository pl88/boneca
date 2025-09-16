# Boneca - Dance School Management System

A modern, containerized system for managing dance schools, classes, and events.

## Documentation

- [Architecture](backend/docs/ARCHITECTURE.md) - Project structure and architectural decisions
- [Local Development](backend/docs/LOCAL_DEVELOPMENT.md) - Setting up local development environment
- [Example API Requests](backend/docs/EXAMPLE_REQUESTS.md) - Example API requests and responses

## Quick Start

1. Prerequisites:
   - Docker and Docker Compose
   - Make
   - Git

2. Clone and run:
   ```bash
   git clone git@github.com:pl88/boneca.git
   cd boneca/backend
   make run-dev
   ```

3. Check the API:
   ```bash
   curl http://localhost:8000/api/v1/ping
   ```

## Development

For detailed development instructions, see [Local Development Guide](backend/docs/LOCAL_DEVELOPMENT.md).

Quick commands for backend (running from boneca/backend/):
```bash
# Start development server
make run-dev

# View logs
make logs

# Run tests
make test

# Format code
make format-backend

# Lint code
make lint-backend

# Complete code quality pipeline (format + lint + test)
make go-go-boneca-rangers
```

## Project Status

Current features:
- [x] Project structure and architecture
- [x] Development environment setup
- [x] Health check endpoint
- [ ] Users API
- [ ] Authentication
- [ ] Classes management
- [ ] Events management
- [ ] Payments integration

## Contributing

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

For more details, see [Local Development Guide](backend/docs/LOCAL_DEVELOPMENT.md).

## License

MIT License - see LICENSE file for details.

## Team

- Owner: @pl88
- Contributors: [Your team here]

## Acknowledgments

- FastAPI for the excellent web framework
- Poetry for dependency management
- Docker for containerization
- And all other open source projects that made this possible
