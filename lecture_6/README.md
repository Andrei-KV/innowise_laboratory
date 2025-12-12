# Book API

## Description

This is a simple Book API built with FastAPI and SQLAlchemy.

## Endpoints

### Add a new book

```http
POST /books/
```

### Get all books with pagination

```http
GET /books/
```

### Search books

```http
GET /books/search/
```

### Delete a book by ID

```http
DELETE /books/{book_id}
```

### Update a book by ID

```http
PUT /books/{book_id}
```

## Running with Docker

### Prerequisites

```Docker installed on your machine
```

### Quick Start

#### Build the Docker image

```Build the Docker image:
   docker build . -t app:latest
```

#### Run the container

```docker run -p 8000:8000 app:latest
```

#### Open in browser

```http://localhost:8000/e
```
