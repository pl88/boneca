# API Example Requests

This document contains example requests for all API endpoints. You can use these examples with `curl` or import them into Postman.

## Health Check

### GET /api/v1/ping

Check if the API is running:

```bash
curl http://localhost:8000/api/v1/ping
```

Expected response:
```json
{
    "status": "ok",
    "version": "1.0.0"
}
```

## Users API

### GET /api/v1/users

List all users:

```bash
curl http://localhost:8000/api/v1/users
```

Expected response:
```json
{
    "users": [
        {
            "id": "1",
            "username": "john_doe",
            "email": "john@example.com",
            "created_at": "2025-09-12T10:00:00Z",
            "updated_at": "2025-09-12T10:00:00Z"
        }
    ],
    "total": 1
}
```

### GET /api/v1/users/{user_id}

Get a specific user:

```bash
curl http://localhost:8000/api/v1/users/1
```

Expected response:
```json
{
    "id": "1",
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": "2025-09-12T10:00:00Z",
    "updated_at": "2025-09-12T10:00:00Z"
}
```

### POST /api/v1/users

Create a new user:

```bash
curl -X POST http://localhost:8000/api/v1/users \
    -H "Content-Type: application/json" \
    -d '{
        "username": "jane_doe",
        "email": "jane@example.com",
        "password": "securepassword123"
    }'
```

Expected response:
```json
{
    "id": "2",
    "username": "jane_doe",
    "email": "jane@example.com",
    "created_at": "2025-09-12T10:30:00Z",
    "updated_at": "2025-09-12T10:30:00Z"
}
```

### PUT /api/v1/users/{user_id}

Update an existing user:

```bash
curl -X PUT http://localhost:8000/api/v1/users/2 \
    -H "Content-Type: application/json" \
    -d '{
        "username": "jane_smith",
        "email": "jane.smith@example.com"
    }'
```

Expected response:
```json
{
    "id": "2",
    "username": "jane_smith",
    "email": "jane.smith@example.com",
    "created_at": "2025-09-12T10:30:00Z",
    "updated_at": "2025-09-12T11:00:00Z"
}
```

### DELETE /api/v1/users/{user_id}

Delete a user:

```bash
curl -X DELETE http://localhost:8000/api/v1/users/2
```

Expected response:
```json
{
    "status": "success",
    "message": "User deleted successfully"
}
```

## Using with Postman

1. Download and install [Postman](https://www.postman.com/downloads/)
2. Import the collection:
   - Click "Import" in Postman
   - Select "Raw text"
   - Copy and paste the following:

```json
{
    "info": {
        "name": "Boneca API",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "item": [
        {
            "name": "Health Check",
            "request": {
                "method": "GET",
                "url": "http://localhost:8000/api/v1/ping"
            }
        },
        {
            "name": "List Users",
            "request": {
                "method": "GET",
                "url": "http://localhost:8000/api/v1/users"
            }
        },
        {
            "name": "Get User",
            "request": {
                "method": "GET",
                "url": "http://localhost:8000/api/v1/users/1"
            }
        },
        {
            "name": "Create User",
            "request": {
                "method": "POST",
                "url": "http://localhost:8000/api/v1/users",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json"
                    }
                ],
                "body": {
                    "mode": "raw",
                    "raw": "{\n    \"username\": \"jane_doe\",\n    \"email\": \"jane@example.com\",\n    \"password\": \"securepassword123\"\n}"
                }
            }
        },
        {
            "name": "Update User",
            "request": {
                "method": "PUT",
                "url": "http://localhost:8000/api/v1/users/1",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json"
                    }
                ],
                "body": {
                    "mode": "raw",
                    "raw": "{\n    \"username\": \"jane_smith\",\n    \"email\": \"jane.smith@example.com\"\n}"
                }
            }
        },
        {
            "name": "Delete User",
            "request": {
                "method": "DELETE",
                "url": "http://localhost:8000/api/v1/users/1"
            }
        }
    ]
}
