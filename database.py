import os
import asyncpg
from asyncpg.exceptions import UniqueViolationError

env = os.getenv("ENVIRONMENT", "local")

if (os.getenv("ENVIRONMENT", "local") == "local"):
    postgres_uri = "postgres://sean_b:postgres@localhost:5432/passwordmanager?sslmode=disable"
else: 
    postgres_uri = ""


async def psql_search_user(*params):
    try:
        conn = await asyncpg.connect(postgres_uri)

        sql = "SELECT * FROM users WHERE email = $1"
        
        result = await conn.fetchrow(sql, *params)

        return result

    except UniqueViolationError as e :
        return "Error", "User doesnt exist"
    finally:
        await conn.close()


async def psql_create_user(*params):
    try:
        conn = await asyncpg.connect(postgres_uri)

        sql = "INSERT INTO users (name, email, password) VALUES ($1, $2, $3);"
        
        result = await conn.execute(sql, *params)

        return result

    except UniqueViolationError as e :
        return "Error", "Email Address already in use"
    finally:
        await conn.close()