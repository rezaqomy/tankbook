# tankbook

## Overview

Tankbook is a FastAPI project that provides a comprehensive system for managing books, authors, and customers. The project includes features like user authentication, book management, and reservation systems. This README will guide you through the structure of the project and how to use it.

## Project Structure

The project is organized into various directories and files, each serving a specific purpose:

- `Dockerfile`: Defines the Docker image for the project.
- `docker-compose.yml`: Defines the services for Docker Compose.
- `alembic.ini`: Configuration file for Alembic, the database migration tool.
- `requirements.txt`: Lists the dependencies required for the project.
- `start.sh`: Shell script to start the application.
- `.env.example`: Example environment variables file.
- `src/`: Contains the main application code.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Setup

1. **Clone the repository:**

    ```sh
    git clone <repository_url>
    cd tankbook
    ```

2. **Copy the example environment file and configure the environment variables:**

    ```sh
    cp .env.example .env
    ```

3. **Build and start the application using Docker Compose:**

    ```sh
    docker-compose up --build
    ```

4. **Access the application:**

    The application will be available at `http://localhost:8000`.

### Database Migrations

The project uses Alembic for database migrations. To apply migrations, use the following command:

```sh
docker-compose exec tankbook alembic upgrade head
```

## Usage

### API Endpoints

The application exposes several API endpoints for managing users, books, and reservations.

#### User Endpoints

- **Create User:** `POST /user/`
- **Get User:** `GET /user/{user_id}`
- **Update User:** `PATCH /user/{user_id}`
- **Delete User:** `DELETE /user/{user_id}`
- **Login:** `POST /auth/login`
- **Get Current User:** `GET /auth/me`

#### Book Endpoints

- **Create Book:** `POST /book/`
- **Get Book:** `GET /book/{id}`
- **Get All Books:** `GET /book/`
- **Update Book:** `PUT /book/{id}`
- **Delete Book:** `DELETE /book/{id}`

#### Reservation Endpoints

- **Create Reservation:** `POST /reserves/`
- **Get Reservation:** `GET /reserves/{reserve_id}`
- **Update Reservation:** `PUT /reserves/{reserve_id}`
- **Delete Reservation:** `DELETE /reserves/{reserve_id}`


## Directory Structure

- `alembic/`: Contains Alembic configuration and migrations.
- `src/`: Contains the main application code.
  - `auth/`: Contains authentication and authorization logic.
  - `book/`: Contains book management logic.
  - `profile/`: Contains user profile management logic.
  - `reserve/`: Contains reservation management logic.
  - `config.py`: Configuration settings for the application.
  - `database/`: Contains database connection and setup code.
  - `main.py`: The entry point for the FastAPI application.
  - `schemas.py`: Defines Pydantic models for request and response validation.


