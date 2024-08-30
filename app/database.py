import os
import asyncpg
from uuid import UUID
from models.user import User
from models.records import Record
from .exceptions import RecordNotFoundException
from app.encryption import encrypt_data, decrypt_data

env = os.getenv("ENVIRONMENT", "local")

if (os.getenv("ENVIRONMENT", "local") == "local"):
    postgres_uri = "postgres://sean_b:postgres@localhost:5432/passwordmanager?sslmode=disable"
else: 
    postgres_uri = ""


async def psql_search_user(user_email):
    try:
        conn = await asyncpg.connect(postgres_uri)

        sql = "SELECT * FROM users WHERE email = $1"
        
        result = await conn.fetchrow(sql, user_email)

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


async def psql_create_record(record: Record, user_id: str):
    try:
        conn = await asyncpg.connect(postgres_uri)

        sql = "INSERT INTO record (id, name, description, username, password, is_weak, user_id, group_id) VALUES (gen_random_uuid(), $1, $2, $3, $4, $5, $6, $7) RETURNING id;"

        # Encrypt sensitive data
        encrypted_username = encrypt_data(record.username)
        encrypted_password = encrypt_data(record.password)

        # Convert UUID to string
        user_id_str = str(user_id)

        result = await conn.fetchval(sql, record.name, record.description, encrypted_username, encrypted_password, record.is_weak, user_id_str, record.group_id)

        return result
    
    except Exception as e:
        raise Exception(f"Error creating record: {str(e)}")
    finally:
        await conn.close()


async def psql_get_record(
        user_id:int,
        record_name:str = None
    ):
    '''
    Get a record by name or by ID.
    - Used as a search feature for users to get records by name
    - Used to search for records by ID internally.
    '''
    try:
        conn = await asyncpg.connect(postgres_uri)

        sql = "SELECT * FROM record WHERE user_id = $1 AND name LIKE $2;"

        result = await conn.fetchrow(sql, user_id, record_name)

        if result is None:
            raise RecordNotFoundException

        # Decrypt sensitive data
        result['username'] = decrypt_data(result['username'])
        result['password'] = decrypt_data(result['password'])

        return result
    
    except RecordNotFoundException:
        raise RecordNotFoundException("Record was not found")
    except Exception:
        raise Exception("Error with sql getting record")
    finally:
        if conn:
            await conn.close()


async def psql_get_all_records(user_id: int):
    try:
        conn = await asyncpg.connect(postgres_uri)

        sql = "SELECT name, folder_id FROM record WHERE user_id = $1;"

        results = await conn.fetch(sql, user_id)

        return results
    
    except Exception:
        raise Exception("Error retrieving user records")
    finally:
        if conn:
            await conn.close()


async def psql_update_record(record_id: int, user_id: int, record_data: Record):
    try:
        conn = await asyncpg.connect(postgres_uri)

        sql = "UPDATE record SET name = $1, description = $2, username = $3, password = $4, folder_id = $5 WHERE id = $6 AND user_id = $7;"

        # Encrypt sensitive data
        encrypted_username = encrypt_data(record_data.username)
        encrypted_password = encrypt_data(record_data.password)

        await conn.execute(sql, record_data.name, record_data.description, encrypted_username, encrypted_password, record_data.folder_id, record_id, user_id)

        return {
            "status":200,
            "message": "success"
            }
    except Exception:
        raise Exception("Failed to update record")


async def psql_delete_record(record_id: int, user_id: int):
    try:
        conn = await asyncpg.connect(postgres_uri)

        sql = "DELETE FROM record WHERE id = $1 AND user_id = $2"

        result = await conn.execute(sql, record_id, user_id)

        return result
    except Exception:
        raise Exception("Error deleting row")