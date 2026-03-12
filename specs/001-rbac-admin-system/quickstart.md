# Quickstart: RBAC Admin System

**Feature**: 001-rbac-admin-system
**Date**: 2026-03-12

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- Git

## Quick Start

### 1. Clone and Start

```bash
# Clone repository
git clone <repository-url>
cd my-awesome-app

# Copy environment file
cp .env.example .env

# Start all services
docker-compose up -d
```

### 2. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **API Documentation (ReDoc)**: http://localhost:8000/redoc

### 3. Default Credentials

- **Username**: `admin`
- **Password**: `Admin@123`

## Development Setup

### Backend Development

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## Environment Variables

Create `.env` file with the following variables:

```env
# Database
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=root123
MYSQL_DATABASE=rbac_admin

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0

# JWT
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120
REFRESH_TOKEN_EXPIRE_DAYS=7

# Application
APP_ENV=development
DEBUG=true
CORS_ORIGINS=http://localhost:3000

# File Upload
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=5242880  # 5MB in bytes
```

## Database Initialization

The system automatically creates:
- Default super admin user
- Default roles (super_admin, admin, user)
- Default menu structure
- Required indexes

## API Testing

### Login Request

```bash
# Get captcha first
curl http://localhost:8000/api/v1/auth/captcha

# Login (use captcha_key and captcha_code from previous response)
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "Admin@123",
    "captcha_key": "<captcha_key>",
    "captcha_code": "<code>"
  }'
```

### Get User Info

```bash
curl http://localhost:8000/api/v1/auth/user/info \
  -H "Authorization: Bearer <access_token>"
```

## Troubleshooting

### Database Connection Failed

1. Check MySQL is running: `docker-compose ps`
2. Verify credentials in `.env`
3. Check MySQL logs: `docker-compose logs mysql`

### Redis Connection Failed

1. Check Redis is running: `docker-compose ps`
2. Verify Redis config in `.env`
3. Check Redis logs: `docker-compose logs redis`

### Frontend Not Loading

1. Check frontend container: `docker-compose ps`
2. Check frontend logs: `docker-compose logs frontend`
3. Verify CORS settings in backend

### Migration Issues

```bash
# Check current migration status
alembic current

# Rollback last migration
alembic downgrade -1

# Reset database (CAUTION: deletes all data)
alembic downgrade base
alembic upgrade head
```

## Docker Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Rebuild containers
docker-compose up -d --build

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Execute command in container
docker-compose exec backend bash
docker-compose exec mysql mysql -u root -p
```

## Production Deployment

1. Update `.env` with production values
2. Change `JWT_SECRET_KEY` to a strong random value
3. Set `DEBUG=false` and `APP_ENV=production`
4. Configure SSL/TLS certificates
5. Use proper database backups
6. Set up log rotation

## Architecture Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Browser   │────>│   Frontend  │────>│   Backend   │
│   (Vue 3)   │     │   (Nginx)   │     │  (FastAPI)  │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
                              ┌───────────────┼───────────────┐
                              ▼               ▼               ▼
                        ┌──────────┐   ┌──────────┐   ┌──────────┐
                        │  MySQL   │   │  Redis   │   │  Files   │
                        │    8     │   │    7     │   │ (Local)  │
                        └──────────┘   └──────────┘   └──────────┘
```

## Next Steps

1. Review API documentation at `/docs`
2. Create additional roles and users
3. Configure department structure
4. Set up menu permissions
5. Customize frontend branding