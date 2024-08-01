import os
import asyncpg
from models.user.models import User
from models.records.models import Password

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


async def psql_create_user(user: User):
    try:
        conn = await asyncpg.connect(postgres_uri)

        sql = "INSERT INTO users (name, email, password) VALUES ($1, $2, $3);"
        
        result = await conn.execute(sql, user.name, user.email, user.password)

        return result

    except Exception as e :
        return e
    finally:
        await conn.close()


async def psql_create_record(password: Password):
    try:
        conn = await asyncpg.connect(postgres_uri)

        sql = "INSERT INTO passwords (name, description, username, password, folder_id, user_id) VALUES ($1, $2, $3, $4, $5, $6);"

        result = await conn.execute(sql, password.name, password.description, password.username, password.password, password.folder_id, password.user_id)

        return result
    
    except Exception:
        raise Exception("Error with sql creating password")
    finally:
        await conn.close()


async def psql_get_record(
        user_email:str,
        record_name:str = "%"
    ):
    try:
        conn = await asyncpg.connect(postgres_uri)

        sql = "SELECT * FROM passwords WHERE user_id LIKE $1 AND name LIKE $2;"

        result = await conn.execute(sql, user_email, record_name)

        return result
    
    except Exception:
        return Exception("Error with sql creating password")
    finally:
        await conn.close()