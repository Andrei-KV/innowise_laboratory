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
