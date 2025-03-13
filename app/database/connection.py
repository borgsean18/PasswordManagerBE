import os
import asyncpg
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Hardcoded connection string for testing
POSTGRES_URI = "postgresql://postgres:postgres@localhost:5432/postgres"
logger.info(f"Using database connection string: {POSTGRES_URI}")

MIN_CONNECTIONS = int(os.getenv("MIN_DB_CONNECTIONS", "5"))
MAX_CONNECTIONS = int(os.getenv("MAX_DB_CONNECTIONS", "20"))

# Global connection pool
_pool: Optional[asyncpg.Pool] = None

async def initialize_connection_pool():
    """Initialize the database connection pool."""
    global _pool
    
    if _pool is not None:
        logger.warning("Connection pool already initialized")
        return
    
    try:
        logger.info("Initializing database connection pool")
        _pool = await asyncpg.create_pool(
            POSTGRES_URI,
            min_size=MIN_CONNECTIONS,
            max_size=MAX_CONNECTIONS,
            command_timeout=60,
            max_inactive_connection_lifetime=300.0,  # 5 minutes
        )
        logger.info(f"Connection pool initialized with min={MIN_CONNECTIONS}, max={MAX_CONNECTIONS} connections")
        
        # Test the connection
        async with _pool.acquire() as conn:
            version = await conn.fetchval("SELECT version();")
            logger.info(f"Connected to PostgreSQL: {version}")
    except Exception as e:
        logger.error(f"Failed to initialize connection pool: {str(e)}")
        raise

async def get_connection():
    """Get a connection from the pool."""
    if _pool is None:
        logger.info("Connection pool not initialized, initializing now")
        await initialize_connection_pool()
    
    try:
        return await _pool.acquire()
    except Exception as e:
        logger.error(f"Failed to acquire connection from pool: {str(e)}")
        raise

async def release_connection(connection):
    """Release a connection back to the pool."""
    if _pool is not None:
        try:
            await _pool.release(connection)
        except Exception as e:
            logger.error(f"Failed to release connection: {str(e)}")
            raise

async def close_connection_pool():
    """Close the connection pool."""
    global _pool
    
    if _pool is not None:
        logger.info("Closing database connection pool")
        await _pool.close()
        _pool = None
        logger.info("Database connection pool closed")

class DatabaseConnection:
    """Context manager for database connections."""
    
    def __init__(self):
        self.conn = None
    
    async def __aenter__(self):
        try:
            self.conn = await get_connection()
            return self.conn
        except Exception as e:
            logger.error(f"Error in DatabaseConnection.__aenter__: {str(e)}")
            raise
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.conn is not None:
            try:
                await release_connection(self.conn)
            except Exception as e:
                logger.error(f"Error in DatabaseConnection.__aexit__: {str(e)}")
                raise
