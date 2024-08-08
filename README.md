# FastAPI Practice Project

This repository is a practice project to learn and demonstrate how to create APIs using FastAPI.

## Features

- RESTful API creation with FastAPI
- Database integration using SQLAlchemy
- Asynchronous request handling
- User authentication and authorization
- CRUD operations with PostgreSQL
- Alembic for database migrations
- JWT (JSON Web Tokens) for secure authentication
- Error handling and password management

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/crystalvisio/FastAPI.git
   cd FastAPI
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install the necessary packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file with your database information:**

   ```env
   DB_NAME=<your_dbName>
   DB_USER=<your_dbUSer>
   DB_PASSWORD=<your_dbPassword>
   DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME}
   SECRET_KEY=<your_secret_key>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINS=30 # specify the timeframe you want
   ```

5. **Set up the database:**

   ```bash
   alembic upgrade head
   ```

## Running the Application

1. **Start the FastAPI server:**

   ```bash
   uvicorn app.main:app --reload
   ```

## Project Structure

```
FastAPI/
├── alembic/                     # Alembic configuration and migration scripts
│   ├── versions/                # Migration versions
│   ├── env.py                   # Environment-specific configuration for Alembic (if used)
│   └── README.md                # Instructions or notes for Alembic usage (optional)
│
├── app/                         # Application source code
│   ├── routers/                 # API route definitions
│   │   ├── auth.py              # Authentication routes
│   │   ├── post.py              # Post-related routes
│   │   ├── user.py              # Post-related routes
│   │   └── vote.py              # vote-related routes
│   │
│   ├── __init__.py              # Initializes the `app` package
│   ├── config.py                # Pydantic Basic Settings (Import env variables)
│   ├── database.py              # Database connection setup
│   ├── main.py                  # FastAPI application instance
│   ├── models.py                # SQLAlchemy models
│   ├── oauth2.py                # Authentication (JWT) handling
│   ├── schemas.py               # Pydantic models (schemas)
│   ├── utils.py                 # Utility functions (error handling, password management)
│
├── .env                         # Environment variables
├── .gitignore                   # Git ignore file to exclude files and directories from version control
├── alembic.ini                  # Alembic configuration file
├── Procfile                     # For deploying with platforms like Heroku
├── gunicorn.service             # Systemd service file for Gunicorn (if used for deployment)
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Dockerfile for containerizing the application
├── docker-compose.yml           # Docker Compose configuration for multi-container setup
├── .dockerignore                # Specifies files and directories to ignore in Docker builds
└── README.md                    # Project README file
```

## Usage

### Authentication

The API uses JWT for authentication. Obtain a token by logging in, and include the token in the `Authorization` header as `Bearer <token>` for subsequent requests.

### Endpoints

- **User Registration and Login:**

  - `POST /user` - Register a new user
  - `GET /user/{id}` - GET a specific user

- **Post Operations:**

  - `POST /post` - Create a new post
  - `GET /post` - Retrieve all posts
  - `GET /post` - Retrieve all posts with filters
  - `GET /post/{id}` - Retrieve a specific post by ID
  - `PUT /post/{id}` - Update a post by ID
  - `DELETE /post/{id}` - Delete a post by ID

- **Login Operations:**

  - `POST /login` - Login and getting auth token

- **Voting (Likes and Dislike):**
  - `POST /vote` - Upvote or Downvote post

## Utility Functions

- **Password Management:**

  - Hashing and verification of passwords are handled in `utils.py`.

- **Error Handling:**
  - Centralized error handling is managed in `utils.py` for consistent API responses.
