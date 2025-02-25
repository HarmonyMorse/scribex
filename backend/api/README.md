# ScribeX API Structure

## API Documentation

### Interactive Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc UI: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

### Example API Calls

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Create Student Account
```bash
curl -X POST http://localhost:8000/users/students \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "password": "securepass123",
    "profile": {
      "first_name": "John",
      "last_name": "Doe",
      "grade_level": 6,
      "has_iep": false
    },
    "user_type": "student"
  }'
```

#### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "password": "securepass123"
  }'
```

#### Get User Profile (Authenticated)
```bash
curl http://localhost:8000/users/me \
  -H "Authorization: Bearer ${TOKEN}"
```

```
api/
├── app/
│   ├── core/                 # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py        # Environment and app configuration
│   │   └── security.py      # Authentication, authorization
│   │
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── base.py         # Base model class
│   │
│   ├── repositories/        # Database interaction layer
│   │   ├── __init__.py
│   │   └── base.py         # Base repository class
│   │
│   ├── services/           # Business logic layer
│   │   ├── __init__.py
│   │   ├── ai/            # AI service integrations
│   │   │   ├── __init__.py
│   │   │   ├── grammar.py  # Sapling integration
│   │   │   └── prompts.py  # OpenAI integration
│   │   └── base.py        # Base service class
│   │
│   ├── api/               # API routes
│   │   ├── __init__.py
│   │   ├── v1/           # Version 1 endpoints
│   │   │   ├── __init__.py
│   │   │   └── endpoints/
│   │   │       ├── __init__.py
│   │   │       └── health.py
│   │   └── deps.py       # Dependency injection
│   │
│   └── schemas/          # Pydantic models
│       ├── __init__.py
│       └── base.py       # Base Pydantic models
│
├── tests/                # Test directory
│   ├── __init__.py
│   ├── conftest.py      # Test configuration
│   └── api/             # API tests
│
├── alembic/             # Database migrations
├── main.py             # Application entry point
├── requirements.txt    # Project dependencies
└── Dockerfile         # Container configuration
```

## MVP Components

### Core Features
- Health check endpoint
- Basic database connectivity
- Environment configuration
- Error handling

### Models (MVP)
- User
- Student Profile
- Writing Assignment
- Writing Submission

### Repositories (MVP)
- Base Repository (CRUD operations)
- User Repository
- Assignment Repository
- Submission Repository

### Services (MVP)
- Grammar Service (Sapling)
- Assignment Service
- User Service

### Routes (MVP)
- Health Check
- Authentication
- Writing Submissions
- Basic Assignment Management

## Development Standards

### Type Hinting
- All functions must include type hints for parameters and return values
- Use Union/Optional instead of Any where possible
- Use Literal for exhaustive string/number options
- Use TypeVar for generic types

```python
# Good
from typing import Optional, Union, Literal, List

def process_submission(
    text: str,
    grade_level: Literal[6, 7, 8],
    feedback_type: Optional[Literal["basic", "detailed"]] = None
) -> List[str]:
    ...

# Avoid
def process_submission(text, grade_level, feedback_type=None):
    ...
```

### Type Definitions
- Use Pydantic models for data validation
- Define custom types for domain-specific concepts
- Document complex type hierarchies 