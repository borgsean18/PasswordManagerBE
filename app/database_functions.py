import os
import asyncpg
from uuid import UUID
from models.user import User
from models.records import Record
from .exceptions import RecordNotFoundException
from app.encryption import deterministic_encrypt_data, deterministic_decrypt_data
from app.database.connection import DatabaseConnection
import logging

env = os.getenv("ENVIRONMENT", "local")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def psql_search_user(user_email):
    try:
        async with DatabaseConnection() as conn:
            sql = "SELECT * FROM users WHERE email = $1"

            encrypted_email = deterministic_encrypt_data(user_email)
            
            result = await conn.fetchrow(sql, encrypted_email)

            if result:
                # Decrypt the email in the result
                result = dict(result)
                result['email'] = deterministic_decrypt_data(result['email'])
                result['password'] = deterministic_decrypt_data(result['password'])

            return result

    except Exception as e:
        logger.error(f"Error searching user: {str(e)}")
        return "Error", "User doesn't exist"


async def psql_create_user(user: User):
    try:
        async with DatabaseConnection() as conn:
            sql = "INSERT INTO users (name, email, password) VALUES ($1, $2, $3);"

            encrypted_email = deterministic_encrypt_data(user.email)
            encrypted_password = deterministic_encrypt_data(user.password)
            
            result = await conn.execute(sql, user.name, encrypted_email, encrypted_password)

            return result

    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return e


async def psql_create_record(record: Record, user_id: str):
    try:
        async with DatabaseConnection() as conn:
            sql = "INSERT INTO record (name, description, username, password, is_weak, user_id, group_id) VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING id;"

            # Encrypt sensitive data
            encrypted_username = deterministic_encrypt_data(record.username)
            encrypted_password = deterministic_encrypt_data(record.password)

            # Handle group_id: if it's not a valid UUID, set it to None
            group_id = None
            if record.group_id:
                try:
                    group_id = UUID(str(record.group_id))
                except ValueError:
                    logger.warning(f"Invalid group_id provided: {record.group_id}. Setting to None.")

            result = await conn.fetchval(sql, record.name, record.description, encrypted_username, encrypted_password, record.is_weak, user_id, group_id)

            return result
    
    except Exception as e:
        logger.error(f"Error creating record: {str(e)}")
        raise Exception(f"Error creating record: {str(e)}")


async def psql_get_record(
        user_id: str,
        record_id: str
    ):
    '''
    Get a record by ID.
    '''
    try:
        async with DatabaseConnection() as conn:
            sql = "SELECT * FROM record WHERE user_id = $1 AND id = $2;"

            result = await conn.fetchrow(sql, user_id, record_id)

            if result is None:
                raise RecordNotFoundException("Record was not found")

            # Convert result to a dictionary
            result_dict = dict(result)

            # Convert UUID fields to strings
            for key, value in result_dict.items():
                if isinstance(value, UUID):
                    result_dict[key] = str(value)

            # Decrypt username and password
            try:
                result_dict['username'] = deterministic_decrypt_data(result_dict['username'])
                result_dict['password'] = deterministic_decrypt_data(result_dict['password'])
            except Exception as e:
                logger.error(f"Failed to decrypt username or password for record {record_id}: {str(e)}")
                result_dict['decryption_failed'] = True

            return result_dict
    
    except RecordNotFoundException as e:
        raise e
    except asyncpg.PostgresError as e:
        logger.error(f"Database error: {str(e)}")
        raise Exception(f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise Exception(f"Unexpected error: {str(e)}")


async def psql_get_all_records(user_id: str):
    try:
        async with DatabaseConnection() as conn:
            sql = "SELECT id, name, group_id FROM record WHERE user_id = $1;"

            results = await conn.fetch(sql, user_id)

            # Convert UUIDs to strings
            serializable_results = [
                {key: str(value) if isinstance(value, UUID) else value for key, value in record.items()}
                for record in results
            ]

            return serializable_results
    
    except Exception as e:
        logger.error(f"Error retrieving user records: {str(e)}")
        raise Exception("Error retrieving user records")


async def psql_update_record(record_id: str, user_id: str, record_data: Record):
    try:
        async with DatabaseConnection() as conn:
            sql = """
            UPDATE record 
            SET name = $1, description = $2, username = $3, password = $4, is_weak = $5, group_id = $6 
            WHERE id = $7 AND user_id = $8;
            """

            # Encrypt sensitive data
            encrypted_username = deterministic_encrypt_data(record_data.username)
            encrypted_password = deterministic_encrypt_data(record_data.password)

            # Handle group_id: if it's not a valid UUID, set it to None
            group_id = None
            if record_data.group_id:
                try:
                    group_id = UUID(str(record_data.group_id))
                except ValueError:
                    logger.warning(f"Invalid group_id provided: {record_data.group_id}. Setting to None.")

            result = await conn.execute(sql, record_data.name, record_data.description, 
                                        encrypted_username, encrypted_password, 
                                        record_data.is_weak, group_id, 
                                        record_id, user_id)

            if result == "UPDATE 0":
                raise Exception("No record found to update")

            return {"status": "success", "message": "Record updated successfully"}
    except Exception as e:
        logger.error(f"Failed to update record: {str(e)}")
        raise Exception(f"Failed to update record: {str(e)}")


async def psql_delete_record(record_id: str, user_id: str):
    try:
        async with DatabaseConnection() as conn:
            sql = "DELETE FROM record WHERE id = $1 AND user_id = $2"

            result = await conn.execute(sql, record_id, user_id)

            return result
    except Exception as e:
        logger.error(f"Error deleting record: {str(e)}")
        raise Exception("Error deleting record") 