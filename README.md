# Password Manager Backend

### Environment Setup

Copy the `.env.example` file to `.env` and update the values as needed:

```
cp .env.example .env
```

Key environment variables:
- `DATABASE_URL`: PostgreSQL connection string
- `MIN_DB_CONNECTIONS`: Minimum number of database connections in the pool (default: 5)
- `MAX_DB_CONNECTIONS`: Maximum number of database connections in the pool (default: 20)

### Database Connection Pool

The application uses a connection pool for efficient database access:
- Automatically manages concurrent database connections
- Handles connection acquisition and release
- Configurable pool size via environment variables
- Graceful startup and shutdown

### How to modify schema locally

Install the golang-migrations tool : [Installation commands](https://github.com/golang-migrate/migrate/tree/master/cmd/migrate#download-pre-built-binary-windows-macos-or-linux)

Create a new migration:
```
migrate create -ext sql -dir migrate/db_migrations {title of update}
```

This will create empty up/down files.

Populate these files with idempotent schema modifications, UP will contain changes while
DOWN will undo them


apply new changes to your local/test DB: 
```
migrate -database 'postgres://sean_b:postgres@localhost:5432/passwordmanager?sslmode=disable' -path db/migrations up
```
test if changes can be reversed:
```
migrate -database 'postgres://sean_b:postgres@localhost:5432/passwordmanager?sslmode=disable' -path db/migrations down
```

### Running the Application

Start the application:

```
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000