# RoadFlow API

A FastAPI-based backend system for managing organizations, users, and workflow automation.

## Features

- RESTful API with FastAPI
- Multiple database support (PostgreSQL, MongoDB)
- Asynchronous task processing with Celery
- Redis caching
- Docker Compose setup for local development
- Versioned API structure

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
??? lib/                        # Shared libraries and connections
?   ??? cache.py                # Redis cache implementation
?   ??? celery.py               # Celery configuration
?   ??? mongo.py                # MongoDB client
?   ??? prisma.py               # Prisma ORM setup
??? prisma/                     # Prisma schema and migrations
?   ??? schema.prisma           # Database schema
??? routes/                     # API routes
?   ??? api/
?       ??? v1/                 # API v1 endpoints
??? services/                   # Background services
?   ??? celery_jobs/            # Celery tasks
?       ??? tasks.py            # Task definitions
??? .env.example                # Example environment variables
??? docker-compose.yml          # Docker Compose configuration
??? Dockerfile                  # Docker configuration
??? README.md                   # Project documentation
??? celery_worker.py            # Celery worker entry point
??? main.py                     # FastAPI application entry point
??? requirements.txt            # Python dependencies
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
celery -A celery_worker.celery_app worker --loglevel=info
```

### Running with Docker Compose

```bash
docker-compose up -d
```

## Data Model

The application uses a PostgreSQL database with the following main entities:

- **Organizations**: Companies or teams using the platform
- **Users**: Individual users associated with organizations
- **Members**: Organization members with specific roles
- **Integrations**: External service integrations
- **Agents**: Automated workflow agents

## Environment Variables

See `.env.example` for all required environment variables.

## License

[MIT License](LICENSE)