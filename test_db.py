import asyncio
import asyncpg
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Hardcoded connection string for testing
POSTGRES_URI = "postgresql://postgres:postgres@localhost:5432/postgres"
logger.info(f"Database URL: {POSTGRES_URI}")

async def test_connection():
    try:
        logger.info(f"Connecting to database: {POSTGRES_URI}")
        conn = await asyncpg.connect(POSTGRES_URI)
        logger.info("Connection successful!")
        
        # Test a simple query
        version = await conn.fetchval("SELECT version();")
        logger.info(f"PostgreSQL version: {version}")
        
        await conn.close()
        logger.info("Connection closed")
    except Exception as e:
        logger.error(f"Error connecting to database: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(test_connection()) 