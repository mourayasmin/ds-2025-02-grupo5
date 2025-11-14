# Step-by-Step Setup Guide

This guide will walk you through setting up and running the Highschool AI Olympics Subscription API.

## Prerequisites

Before starting, ensure you have:
- **Docker** and **Docker Compose** installed (recommended)
  - Check: `docker --version` and `docker-compose --version`
- OR **Python 3.12+** and **PostgreSQL** installed (for local development)

---

## Option 1: Using Docker Compose (Recommended - Easiest)

### Step 1: Navigate to the Project Directory
```bash
cd backend
```

### Step 2: Create Environment File
```bash
cp env.example .env
```

The `.env` file will contain:
```env
DATABASE_URL=postgresql://ai_olympics_user:ai_olympics_password@postgres:5432/ai_olympics_db
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True
```

**Note:** For Docker Compose, you don't need to modify this file - it's already configured correctly.

### Step 3: Build and Start Services
```bash
docker-compose up -d
```

This command will:
- Build the Python application Docker image
- Start PostgreSQL database container
- Start the backend API container
- Automatically run database migrations on first startup

### Step 4: Verify Services are Running
```bash
docker-compose ps
```

You should see both `ai_olympics_postgres` and `ai_olympics_backend` running.

### Step 5: Check Logs (Optional)
```bash
# View all logs
docker-compose logs -f

# View only backend logs
docker-compose logs -f backend

# View only database logs
docker-compose logs -f postgres
```

### Step 6: Access the API

- **API Root:** http://localhost:8000
- **Interactive API Documentation (Swagger UI):** http://localhost:8000/docs
- **Alternative API Documentation (ReDoc):** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

### Step 7: Test the API

You can test the API using:
1. **Browser:** Visit http://localhost:8000/docs for interactive testing
2. **curl:**
   ```bash
   curl http://localhost:8000/health
   ```
3. **Postman/Insomnia:** Import the API endpoints

### Useful Docker Commands

```bash
# Stop services
docker-compose stop

# Start services
docker-compose start

# Stop and remove containers (keeps volumes)
docker-compose down

# Stop and remove containers and volumes (clean slate)
docker-compose down -v

# Rebuild containers after code changes
docker-compose up -d --build

# View logs
docker-compose logs -f backend

# Execute command in backend container
docker-compose exec backend bash

# Execute command in database container
docker-compose exec postgres psql -U ai_olympics_user -d ai_olympics_db
```

---

## Option 2: Local Development (Without Docker)

### Step 1: Navigate to the Project Directory
```bash
cd backend
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -e .
```

### Step 4: Set Up PostgreSQL Database

#### 4a. Install PostgreSQL (if not already installed)
- **macOS:** `brew install postgresql`
- **Linux:** `sudo apt-get install postgresql`
- **Windows:** Download from https://www.postgresql.org/download/

#### 4b. Create Database and User
```bash
# Connect to PostgreSQL
psql -U postgres

# In PostgreSQL prompt, run:
CREATE DATABASE ai_olympics_db;
CREATE USER ai_olympics_user WITH PASSWORD 'ai_olympics_password';
GRANT ALL PRIVILEGES ON DATABASE ai_olympics_db TO ai_olympics_user;
\q
```

#### 4c. Run Migrations
```bash
psql -U ai_olympics_user -d ai_olympics_db -f migrations/001_initial_schema.sql
```

### Step 5: Create Environment File
```bash
cp env.example .env
```

Edit `.env` file for local PostgreSQL:
```env
DATABASE_URL=postgresql://ai_olympics_user:ai_olympics_password@localhost:5432/ai_olympics_db
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True
```

### Step 6: Start PostgreSQL Service
```bash
# macOS (Homebrew):
brew services start postgresql

# Linux:
sudo systemctl start postgresql

# Windows: Start PostgreSQL service from Services
```

### Step 7: Run the Application
```bash
python main.py
```

Or:
```bash
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

### Step 8: Access the API

- **API Root:** http://localhost:8000
- **Interactive API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

---

## Troubleshooting

### Issue: Port 8000 or 5432 Already in Use

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process or change port in docker-compose.yml/.env
```

### Issue: Database Connection Error

**For Docker:**
```bash
# Check if PostgreSQL container is healthy
docker-compose ps

# Check PostgreSQL logs
docker-compose logs postgres

# Restart services
docker-compose restart
```

**For Local:**
```bash
# Verify PostgreSQL is running
psql -U postgres -c "SELECT version();"

# Check connection string in .env file
# Verify database exists
psql -U ai_olympics_user -d ai_olympics_db -c "\dt"
```

### Issue: Migration Not Applied

**For Docker:**
```bash
# Remove volumes and restart (WARNING: deletes all data)
docker-compose down -v
docker-compose up -d
```

**For Local:**
```bash
# Manually run migration
psql -U ai_olympics_user -d ai_olympics_db -f migrations/001_initial_schema.sql
```

### Issue: Module Not Found Errors

**Solution:**
```bash
# Make sure you're in the backend directory
# Reinstall dependencies
pip install -e .

# For Docker, rebuild
docker-compose up -d --build
```

### Issue: Permission Denied on init_db.sh

**Solution:**
```bash
chmod +x init_db.sh
```

---

## Next Steps

1. **Explore the API:** Visit http://localhost:8000/docs
2. **Create Test Data:**
   - Create a school (Escola)
   - Create a student (Estudante)
   - Create a subscription (Inscricao)
3. **Review the Code Structure:**
   - Entities: `src/entities/`
   - Repositories: `src/repositories/`
   - Services: `src/services/`
   - Controllers: `src/controllers/`

---

## API Endpoints Overview

- **Schools:** `/escolas`
- **Students:** `/estudantes`
- **Subscriptions:** `/inscricoes`
- **Teams:** `/equipes`
- **Team Members:** `/equipe-membros`

See the full API documentation at http://localhost:8000/docs

---

## Support

If you encounter any issues, check:
1. Docker/PostgreSQL logs
2. Environment variables in `.env`
3. Database connection string format
4. Port availability

