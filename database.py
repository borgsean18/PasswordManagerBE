import os
import asyncpg

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

    except Exception :
        return "Error", "User doesnt exist"
    finally:
        await conn.close()


async def psql_create_user(*params):
    try:
        conn = await asyncpg.connect(postgres_uri)

        sql = "INSERT INTO users (name, email, password) VALUES ($1, $2, $3);"
        
        result = await conn.execute(sql, *params)

        return result

    except Exception as e :
        return e
    finally:
        await conn.close()


async def psql_create_password(*params):
    try:
        conn = await asyncpg.connect(postgres_uri)

        sql = "INSERT INTO passwords (name, description, username, password, folder_id, user_id) VALUES ($1, $2, $3, $4, $5, $6);"

        result = await conn.execute(sql, *params)

        return result
    
    except Exception as e:
        return e
    finally:
        await conn.close()