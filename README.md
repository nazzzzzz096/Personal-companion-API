# Personal Companion API 🚀

A **FastAPI-based backend project** that provides:
- **User Authentication** (JWT)
- **Task Management** (CRUD)
- **Weather Information** (via OpenWeather API)
- **Email Reports** (manual trigger)
- **Rate Limiting & Logging**

---

## ✨ Features
- 🔑 **Authentication**
  - Signup & Login with JWT authentication
  - Secure password hashing with bcrypt
- 👥 **User Management**
  - User registration via `/auth/signup`
  - Get current authenticated user via `/users/me`
- ✅ **Task Management**
  - Create, Read, Update, Delete tasks
  - Tasks linked to user account
- 📧 **Reports**
  - On-demand daily task summary email
  - Triggered via `/reports/daily`
- 🌦 **Weather**
  - Get real-time weather by city (`/weather/{city}`)
- ⚡ **Security**
  - JWT-based auth with expiry
  - Rate limiting (5 requests/min per endpoint)
- 📝 **Logging**
  - Centralized rotating log file (`logs/app.log`)

---

## 🛠 Tech Stack
- [FastAPI](https://fastapi.tiangolo.com/) – API framework
- [SQLAlchemy](https://www.sqlalchemy.org/) – ORM for database
- [PostgreSQL (AWS RDS)](https://aws.amazon.com/rds/) – database
- [Passlib (bcrypt)](https://passlib.readthedocs.io/en/stable/) – password hashing
- [python-jose](https://python-jose.readthedocs.io/) – JWT handling
- [FastAPI-Mail](https://sabuhish.github.io/fastapi-mail/) – email service
- [SlowAPI](https://pypi.org/project/slowapi/) – rate limiting
- Logging via Python `logging` module with rotation

---

## 📂 Project Structure
app/
│── main.py # FastAPI entrypoint
│── models.py # SQLAlchemy models (User, Task)
│── database.py # DB connection (Postgres RDS)
│── schemas.py # Pydantic schemas
│── utils.py # Password hashing/verification
│── auth.py # Auth routes (signup, login)
│── users.py # User management routes
│── tasks.py # Task CRUD routes
│── weather.py # Weather API route
│── reports.py # Email report route
│── mail_utils.py # Email config & helper
│── auth_utils.py # JWT token & current_user helper
│── logger.py # Centralized logging
│── rate_limit.py # Global rate limiter setup

📬 API Endpoints

🔑 Auth

POST /v1/auth/signup → Register new user

POST /v1/auth/login → Login & get JWT

👤 Users

GET /v1/users/me → Get current user profile

✅ Tasks

POST /v1/tasks/ → Create task

GET /v1/tasks/ → List tasks

GET /v1/tasks/{task_id} → Get task

PUT /v1/tasks/{task_id} → Update task

DELETE /v1/tasks/{task_id} → Delete task

🌦 Weather

GET /v1/weather/{city} → Get weather data

📧 Reports

POST /v1/reports/daily → Send daily email report


