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

## Development Setup

### Prerequisites
- Docker and Docker Compose
- PowerShell (Windows) or Bash (Mac/Linux)

### Environment Setup
1. Copy the environment template:
   ```bash
   cp .env.template .env
   ```

2. Update the `.env` file with your settings:
   ```env
   # Required settings
   POSTGRES_USER=scribex
   POSTGRES_PASSWORD=your_secure_password
   POSTGRES_DB=scribex_db
   
   # JWT Settings
   JWT_SECRET_KEY=your_secure_key
   JWT_ALGORITHM=HS256
   JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
   JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
   ```

### Starting the Services
Start the database and API services:
```bash
docker compose up -d
```

### Database Migrations
We provide scripts for managing database migrations in both PowerShell and Bash.

#### Before Running Migration Scripts
The scripts expect:
1. Docker daemon to be running
2. No existing containers running for this project (if there are, run `docker compose down`)
3. A valid `.env` file in the `backend/` directory

The scripts will:
1. Build/rebuild the API container if needed
2. Start the database container
3. Wait for the database to be healthy
4. Run the migration commands

#### Migration Commands
By default, the scripts will apply existing migrations:
```bash
# Windows
./scripts/migrate.ps1

# Mac/Linux
./scripts/migrate.sh
```

To create a new migration:
```bash
# Windows
./scripts/migrate.ps1 --new "migration description"

# Mac/Linux
./scripts/migrate.sh --new "migration description"
```

The --new flag will:
1. Create a new migration based on model changes
2. Apply the new migration immediately
3. Require a description of what changed

#### Reset Database (Nuclear Option)
To completely reset the database and migrations:
```bash
# Windows
./scripts/migrate.ps1 --nuke "fresh start"

# Mac/Linux
./scripts/migrate.sh --nuke "fresh start"
```

### Accessing the API
Once running, the API will be available at:
- API: http://localhost:8000
- Swagger Documentation: http://localhost:8000/docs
- ReDoc Documentation: http://localhost:8000/redoc

### Development
The API uses FastAPI with hot-reload enabled. Any changes to the code will automatically restart the server.

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