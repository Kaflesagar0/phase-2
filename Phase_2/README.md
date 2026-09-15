# Smart Greenhouse

A modular, three-tier smart greenhouse monitoring and automation platform.

## Architecture

- **Backend**: FastAPI, SQLAlchemy 2, Alembic, Pydantic Settings, Scalar (API docs)
- **Database**: PostgreSQL 16 (via Docker Compose)
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS v4, React Router

## Prerequisites

Before running the project, verify that the following tools are installed:

- **Python**: 3.11+ (`python --version`)
- **Node.js**: 20 LTS (`node --version`)
- **Docker**: Docker Desktop with Compose (`docker --version`)
- **Git**: (`git --version`)

## First-Time Setup

**Environment Configuration**:
   Copy the example environment file:
   cp .env.example .env
Start the Database:
Launch PostgreSQL in detached mode:
docker compose up -d

Wait a few moments and verify the container is healthy:
docker compose ps

Backend Setup & Migrations:
Navigate to the backend directory, initialize a virtual environment, and install dependencies:
cd backend
python -m venv .venv

Activate the virtual environment:
Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

Linux / macOS:
source .venv/bin/activate

Install dependencies in editable mode:
pip install -e ".[dev]"

Apply the Alembic baseline migration:
alembic upgrade head

Frontend Setup:
In another terminal, install frontend dependencies:
cd frontend
npm install

Daily Start OrderTo run the full stack, use three terminal windows:

Terminal 1 : Database
docker compose up -d

Terminal 2 : Backend API 
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

Terminal 3 : Frontend UI
cd frontend
npm run dev

Service URLs
|| Service            |   URL                            |     Notes ||
|| Frontend Dashboard |  http://localhost:5173/dashboard | React UI with live status indicator ||
|| API Health  |  http://localhost:8000/health          | Service and database connectivity check    ||
|| Scalar API Reference | http://localhost:8000/scalar | Interactive API documentation ||
|| OpenAPI Specification |  http://localhost:8000/openapi.json | Raw OpenAPI 3 schema ||
|| Root Discovery | http://localhost:8000/  | Endpoint discovery payload ||

Note: Default Swagger (/docs) and ReDoc (/redoc) endpoints are disabled in favor of Scalar.

Phase Documentation

For the full assignment progression and future design pattern implementations, refer to docs/phases/README.md.
