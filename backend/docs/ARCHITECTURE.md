# Boneca Backend Architecture

## Project Structure

```python
backend/
├── src/
│   ├── api/                    # API layer
│   │   ├── v1/                # API version 1
│   │   │   ├── healthcheck.py # /ping endpoint
│   │   │   └── users.py       # /users endpoint
│   │   └── router.py          # Router configuration
│   ├── core/                  # Core components
│   │   ├── config.py          # Application settings
│   │   └── repositories/      # Abstract base repositories
│   │       ├── __init__.py    
│   │       ├── base.py        # Generic abstract base repository
│   │       └── nosql.py       # (future) NoSQL base repository
│   ├── domain/                # Business logic & data access
│   │   └── users/
│   │       ├── schemas.py     # User-related schemas
│   │       └── repository.py  # Concrete user repository implementation
│   └── main.py               # Application entry point
├── tests/                    # Test directory
├── Dockerfile               # Container configuration
├── docker-compose.yml      # Container orchestration
├── Makefile               # Backend build commands
├── pyproject.toml        # Python dependencies
└── pytest.ini           # pytest configuration
```

## Key Architectural Decisions

### 1. Project Organization

#### Domain-Centric Structure

- Each domain feature has its own module in `domain/`
- Domain modules contain all related schemas and repositories
- Keeps related code together for better maintainability

#### API Versioning

- API endpoints are versioned (starting with v1)
- Each version has its own router
- Ensures backward compatibility

### 2. Repository Pattern

#### Abstract Base Repositories

- Located in `core/repositories/`
- Define common interfaces and behaviors
- Allow for specialized base repositories (SQL, NoSQL, etc.)
- Promote code reuse and consistency

#### Concrete Repositories

- Located in respective domain modules
- Implement specific entity persistence logic
- Close to the schemas they work with
- Can mix multiple repository patterns (e.g., SQL + Cache)

### 3. Clean Architecture Principles

#### Layer Separation

- API Layer: HTTP endpoints and routing
- Core Layer: Infrastructure and configuration
- Domain Layer: Business logic and data access

#### Dependencies

- Domain layer has no dependencies on external layers
- API layer depends on domain layer
- Core layer provides infrastructure abstractions

### 4. Development Environment

#### Docker-Based Development

- Development environment in containers
- Consistent environment across team
- Easy to set up and tear down

#### Makefile Automation

- Standardized commands with backend suffix
- Quick action aliases for common tasks
- Comprehensive help system

### 5. Code Organization Principles

#### Separation of Concerns

- Each module has a single responsibility
- Clear boundaries between components
- Easy to test and maintain

#### Domain-Driven Design Influence

- Business logic centered in domain layer
- Rich domain models with schemas
- Domain-specific repositories

## Implementation Guidelines

### Adding New Features

1. Create domain module:

   ```python
   domain/
   └── new_feature/
       ├── schemas.py      # Data models
       └── repository.py   # Data access
   ```

2. Add API endpoints:

   ```python
   api/
   └── v1/
       └── new_feature.py  # REST endpoints
   ```

3. Update router configuration in `api/router.py`

### Repository Implementation

1. Use appropriate base repository:

   ```python
   from core.repositories.base import BaseRepository
   
   class NewFeatureRepository(BaseRepository[NewFeature]):
       # Implementation
   ```

2. Consider mixing repository patterns if needed:

   ```python
   class NewFeatureRepository(SQLRepository[NewFeature], CacheableRepository):
       # Implementation
   ```

## Best Practices

### Code Organization

- Keep modules focused and small
- Use clear, descriptive names
- Follow Python naming conventions
- Document public interfaces

### Testing

- Mirror source structure in tests
- Test each layer independently
- Use pytest for testing
- Aim for high test coverage

### Version Control

- Use feature branches
- Keep commits focused
- Write meaningful commit messages
- Review code before merging

## Future Considerations

### Scalability

- Additional repository patterns can be added to `core/repositories/`
- New API versions can be added alongside v1
- Domain modules can be split into microservices if needed

### Maintenance

- Regular dependency updates through Poetry
- Periodic code quality checks
- Performance monitoring
- Documentation updates

## Tools and Technologies

- FastAPI: Web framework
- Poetry: Dependency management
- Docker: Containerization
- Make: Build automation
- pytest: Testing framework
