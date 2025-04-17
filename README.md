# FastAPI CRUD with JWT Authentication

This is a FastAPI backend project that provides full CRUD operations along with secure authentication and authorization using JWT tokens.

## Features

- ✅ User Registration, Login, Logout
- 🔐 JWT-based Authentication
- 🔒 Role-based Authorization
- 🧾 CRUD operations for products (or other models)
- 🛠️ SQLAlchemy for ORM, Pydantic for validation
- 🔍 Swagger UI & Postman support for API testing

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/fastapi-crud-auth.git
cd fastapi-crud-auth

## Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

## Install Dependencies
pip install -r requirements.txt

#Run the server
uvicorn app.main:app --reload
