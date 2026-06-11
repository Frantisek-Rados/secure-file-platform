# Secure File Platform API

A backend service built with FastAPI providing authentication, file management, and secure JWT-based access control with PostgreSQL and Alembic migrations.

## Features

- User registration and login
- JWT access and refresh tokens
- Password hashing with bcrypt
- File upload per authenticated user
- Secure file download with ownership checks
- List user files
- PostgreSQL integration
- Alembic database migrations
- Dockerized setup (API + database)

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- PyJWT
- Passlib (bcrypt)
- Docker / Docker Compose

## Project Structure

app/
├── core/
│   ├── database.py
│   ├── security.py
│   ├── dependencies.py
│   └── alembic_metadata.py
│
├── models/
│   ├── user.py
│   ├── file.py
│   └── __init__.py
│
├── routes/
│   ├── auth.py
│   └── files.py
│
├── schemas/
│   ├── user.py
│   └── file.py
│
├── main.py

alembic/
├── env.py
├── versions/

## Environment Variables

Create a `.env` file:

DATABASE_URL=postgresql://postgres:postgres@postgres:5432/securefiles  
SECRET_KEY=your-secret-key

## Run the Project

docker compose up --build

API will be available at:
http://localhost:8000

## API Endpoints

Auth:
- POST /register
- POST /login

User:
- GET /me

Files:
- POST /upload
- GET /files
- GET /download/{file_id}

## Authentication

All protected routes require:

Authorization: Bearer <access_token>

## Alembic Commands

docker compose exec api alembic upgrade head  
docker compose exec api alembic revision --autogenerate -m "init"

## Notes

- Uploaded files are stored in /app/uploads
- Each file belongs to a user
- Access is restricted per user
