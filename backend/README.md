# Highschool AI Olympics Subscription API

Backend API for managing subscriptions to the Highschool AI Olympics in Goiás, Brazil.

## Features

- RESTful API built with FastAPI
- PostgreSQL database with SQLAlchemy ORM
- Clean architecture (Entities, Repositories, Services, Controllers)
- Docker Compose setup for easy development
- Environment variable configuration

## Project Structure

```
backend/
├── src/
│   ├── config/          # Configuration (database, etc.)
│   ├── entities/        # SQLAlchemy models
│   ├── repositories/    # Data access layer
│   ├── services/        # Business logic layer
│   ├── controllers/     # API endpoints (FastAPI routers)
│   ├── dto/             # Data Transfer Objects (Pydantic models)
│   └── app.py           # FastAPI application
├── migrations/          # Database migration scripts
├── Dockerfile           # Docker image for the application
├── docker-compose.yml   # Docker Compose configuration
└── main.py              # Application entry point
```

## Prerequisites

- Python 3.12+
- Docker and Docker Compose (for containerized setup)
- PostgreSQL (if running locally without Docker)

## Setup

### Option 1: Using Docker Compose (Recommended)

1. **Clone the repository and navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a `.env` file from the example:**
   ```bash
   cp env.example .env
   ```

3. **Edit `.env` file if needed** (default values work for Docker Compose):
   ```env
   DATABASE_URL=postgresql://ai_olympics_user:ai_olympics_password@postgres:5432/ai_olympics_db
   APP_HOST=0.0.0.0
   APP_PORT=8000
   DEBUG=True
   ```

4. **Start the services:**
   ```bash
   docker-compose up -d
   ```

5. **The API will be available at:**
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

6. **View logs:**
   ```bash
   docker-compose logs -f
   ```

7. **Stop the services:**
   ```bash
   docker-compose down
   ```

8. **Stop and remove volumes (clean database):**
   ```bash
   docker-compose down -v
   ```

### Option 2: Local Development

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -e .
   ```

3. **Create a `.env` file:**
   ```bash
   cp env.example .env
   ```

4. **Edit `.env` file for local PostgreSQL:**
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/ai_olympics_db
   APP_HOST=0.0.0.0
   APP_PORT=8000
   DEBUG=True
   ```

5. **Set up PostgreSQL database:**
   - Create a database named `ai_olympics_db`
   - Run the migration script:
     ```bash
     psql -U user -d ai_olympics_db -f migrations/001_initial_schema.sql
     ```

6. **Run the application:**
   ```bash
   python main.py
   ```
   Or:
   ```bash
   uvicorn src.app:app --reload
   ```

## API Endpoints

### Schools (Escolas)
- `GET /escolas` - List all schools
- `GET /escolas/{id}` - Get school by ID
- `POST /escolas` - Create new school
- `PUT /escolas/{id}` - Update school
- `DELETE /escolas/{id}` - Delete school
- `GET /escolas/cidade/{cidade}` - Get schools by city
- `GET /escolas/status/active` - Get active schools

### Students (Estudantes)
- `GET /estudantes` - List all students
- `GET /estudantes/{id}` - Get student by ID
- `GET /estudantes/cpf/{cpf}` - Get student by CPF
- `POST /estudantes` - Create new student
- `PUT /estudantes/{id}` - Update student
- `DELETE /estudantes/{id}` - Delete student
- `GET /estudantes/escola/{escola_id}` - Get students by school

### Subscriptions (Inscrições)
- `GET /inscricoes` - List all subscriptions
- `GET /inscricoes/{id}` - Get subscription by ID
- `POST /inscricoes` - Create new subscription
- `PUT /inscricoes/{id}` - Update subscription
- `DELETE /inscricoes/{id}` - Delete subscription
- `POST /inscricoes/{id}/confirmar` - Confirm subscription
- `POST /inscricoes/{id}/cancelar` - Cancel subscription
- `GET /inscricoes/estudante/{estudante_id}` - Get subscriptions by student
- `GET /inscricoes/escola/{escola_id}` - Get subscriptions by school
- `GET /inscricoes/ano/{ano_edicao}` - Get subscriptions by year
- `GET /inscricoes/status/{status}` - Get subscriptions by status

### Teams (Equipes)
- `GET /equipes` - List all teams
- `GET /equipes/{id}` - Get team by ID
- `POST /equipes` - Create new team
- `PUT /equipes/{id}` - Update team
- `DELETE /equipes/{id}` - Delete team
- `GET /equipes/escola/{escola_id}` - Get teams by school
- `GET /equipes/ano/{ano_edicao}` - Get teams by year
- `GET /equipes/status/{status}` - Get teams by status

### Team Members (Equipe Membros)
- `GET /equipe-membros` - List all team members
- `GET /equipe-membros/{id}` - Get team member by ID
- `POST /equipe-membros` - Add student to team
- `PUT /equipe-membros/{id}` - Update team member
- `DELETE /equipe-membros/{id}` - Remove team member
- `GET /equipe-membros/equipe/{equipe_id}` - Get members by team
- `GET /equipe-membros/estudante/{estudante_id}` - Get teams by student

## Database Schema

The database includes the following tables:
- `escolas` - Schools
- `estudantes` - Students
- `inscricoes` - Subscriptions/Registrations
- `equipes` - Teams
- `equipe_membros` - Team Members

See `migrations/001_initial_schema.sql` for the complete schema.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:password@localhost:5432/ai_olympics_db` |
| `APP_HOST` | Application host | `0.0.0.0` |
| `APP_PORT` | Application port | `8000` |
| `DEBUG` | Debug mode | `True` |

## Development

### Running Tests
(Add test instructions when tests are implemented)

### Code Style
(Add linting/formatting instructions if needed)

## License

[Add your license here]

