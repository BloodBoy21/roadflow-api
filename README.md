# RoadFlow API

A FastAPI-based backend system for managing organizations, users, and workflow automation.

## Features

- RESTful API with FastAPI
- Multiple database support (PostgreSQL, MongoDB)
- Asynchronous task processing with Celery
- Redis caching
- Docker Compose setup for local development
- Versioned API structure
- AI Agent system with specialized agents for different business functions
- Workflow automation and task management
- Organization and user management
- Integration support for external services

## Tech Stack

- **Framework**: FastAPI
- **ORM**: Prisma (PostgreSQL)
- **Databases**:
  - PostgreSQL: Structured data
  - MongoDB: Unstructured data
  - Redis: Caching and message broker
- **Task Queue**: Celery
- **Containerization**: Docker & Docker Compose

## Prerequisites

- Docker and Docker Compose
- Python 3.12+

## Setup & Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd roadflow-api
```

2. **Set up environment variables**

```bash
cp .env.example .env
# Edit .env file with your configuration
```

3. **Start the services with Docker Compose**

```bash
docker-compose up -d
```

4. **Access the API**

The API will be available at: [http://localhost:3000](http://localhost:3000)

API documentation is available at:
- Swagger UI: [http://localhost:3000/docs](http://localhost:3000/docs)

## Project Structure
```
roadflow-api/
├── helpers/                    # Helper utilities
│   ├── auth.py                # Authentication helpers
│   └── webhook.py             # Webhook utilities
├── lib/                        # Shared libraries and connections
│   ├── cache.py                # Redis cache implementation
│   ├── celery.py              # Celery configuration
│   ├── mongo.py               # MongoDB client
│   └── prisma.py              # Prisma ORM setup
├── middleware/                 # FastAPI middleware
│   ├── admin_middleware.py    # Admin access control
│   ├── org_middleware.py      # Organization context
│   └── workflow_middleware.py # Workflow processing
├── models/                     # Data models
│   ├── inputs/                # Input validation models
│   ├── mongo/                 # MongoDB document models
│   └── response/              # API response models
├── prisma/                     # Prisma schema and migrations
│   ├── migrations/            # Database migrations
│   └── schema.prisma          # Database schema
├── repository/                 # Data access layer
│   ├── mongo/                 # MongoDB repositories
│   └── sql/                   # SQL database repositories
├── routes/                     # API routes
│   └── api/
│       └── v1/                # API v1 endpoints
│           ├── agents.py      # Agent management
│           ├── changelog.py   # Changelog operations
│           ├── docs.py        # Documentation
│           ├── organization.py # Organization management
│           ├── users.py       # User management
│           └── workflow.py    # Workflow operations
├── services/                   # Business logic services
│   ├── agents/                # AI Agent system
│   │   ├── base.py           # Base agent class
│   │   ├── customer_agent.py # Customer service agent
│   │   ├── engineer_agent.py # Engineering agent
│   │   ├── growth_agent.py   # Growth & marketing agent
│   │   ├── operations_agent.py # Operations agent
│   │   ├── product_agent.py  # Product management agent
│   │   ├── multi_agent.py    # Multi-agent coordination
│   │   ├── helpers/          # Agent utilities
│   │   └── tools/            # Agent tools
│   │       ├── changelog.py  # Changelog management
│   │       └── out_docs.py   # Document output
│   ├── celery_jobs/           # Celery tasks
│   ├── email/                 # Email services
│   ├── organization_service/  # Organization business logic
│   ├── user_service/          # User business logic
│   └── workflows/             # Workflow services
├── templates/                  # Email templates
├── utils/                      # Utility functions
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Docker configuration
├── main.py                     # FastAPI application entry point
├── celery_worker.py            # Celery worker entry point
├── pyproject.toml              # Project configuration
└── requirements.txt            # Python dependencies
```

## Development

### Running locally (without Docker)

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

2. **Set up environment variables**

```bash
cp .env.example .env
# Edit .env file with your configuration
```

3. **Run the FastAPI server**

```bash
python main.py
```

4. **Run the Celery worker (in a separate terminal)**

```bash
uv run celery -A celery_worker.celery_app worker --loglevel=info
```

### Code Quality

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and code formatting. We use `uv` as the package manager.

**Available commands:**

```bash
# Check for linting issues (exits with error code if issues found)
uv run ruff check .

# Auto-fix linting issues (exits with error code if unfixable issues remain)
uv run ruff check --fix .

# Auto-fix with unsafe fixes (more aggressive)
uv run ruff check --fix --unsafe-fixes .

# Format code
uv run ruff format .

# Check if code is properly formatted (exits with error code if not formatted)
uv run ruff format --check .

# Run both linting and formatting checks (for CI)
uv run ruff check . && uv run ruff format --check .
```

**Ruff configuration:**
- Line length: 88 characters
- Target Python version: 3.12
- Includes rules for: pycodestyle, pyflakes, bugbear, comprehensions, pyupgrade, isort, and simplify

### Running with Docker Compose

```bash
docker compose up -d
```

### Testing

The project includes comprehensive unit tests for all services using pytest.

**Running tests:**

```bash
# Run all tests
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Run tests with coverage report
uv run pytest --cov=services --cov-report=term-missing

# Run specific test categories
python tests/test_runner.py --agents      # Agent tests only
python tests/test_runner.py --workflows   # Workflow tests only
python tests/test_runner.py --services    # All service tests

# Run specific test file
uv run pytest tests/services/agents/test_changelog_tool.py

# Run tests with coverage using the test runner
python tests/test_runner.py --coverage
```

**Test structure:**
- `tests/services/agents/` - Tests for AI agent system
- `tests/services/workflows/` - Tests for workflow services
- `tests/services/user_service/` - Tests for user services
- `tests/conftest.py` - Shared test fixtures and configuration

## AI Agent System

RoadFlow includes a comprehensive AI agent system designed to handle various business functions through specialized agents:

### Available Agents

- **EngineerAgent**: Handles engineering tasks, changelog management, and technical documentation
- **ProductAgent**: Manages product roadmaps, feature specifications, and user feedback analysis
- **OperationsAgent**: Handles system monitoring, process optimization, and incident response
- **CustomerAgent**: Manages customer inquiries, support tickets, and knowledge base maintenance
- **GrowthAgent**: Focuses on marketing campaigns, user acquisition, and growth metrics

### Agent Features

- **Tool Integration**: Each agent has access to specialized tools for their domain
- **Document Management**: Agents can save and retrieve relevant documents
- **Organization Context**: All agents operate within organization boundaries
- **Configurable Instructions**: Agent behavior can be customized per organization
- **Multi-agent Coordination**: Agents can work together on complex tasks

### Agent Tools

- **Changelog Management**: Create, update, and organize project changelogs
- **Document Output**: Save agent responses as searchable documents
- **Context Awareness**: Agents maintain organization-specific context

## Data Model

The application uses a PostgreSQL database with the following main entities:

- **Organizations**: Companies or teams using the platform
- **Users**: Individual users associated with organizations
- **Members**: Organization members with specific roles
- **Integrations**: External service integrations
- **Agents**: AI agents with configurable behavior and tools

## Environment Variables

See `.env.example` for all required environment variables.

## License

[MIT License](LICENSE)