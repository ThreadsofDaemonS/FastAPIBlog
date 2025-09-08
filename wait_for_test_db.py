import asyncio
import asyncpg
from decouple import config


async def wait_for_db():
    """Асинхронна перевірка доступності бази даних."""
    db_host = config("POSTGRES_HOST", default="localhost")
    db_port = config("POSTGRES_PORT", default="5432")
    db_user = config("POSTGRES_USER", default="postgres")
    db_password = config("POSTGRES_PASSWORD", default="password")
    db_name = config("POSTGRES_DB", default="test_db")

    while True:
        try:
            conn = await asyncpg.connect(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_password,
                database=db_name,
            )
            await conn.close()
            print("✅ Database is ready!")
            break
        except Exception as e:
            print(f"⏳ Waiting for database... Error: {e}")
            await asyncio.sleep(3)


if __name__ == "__main__":
    asyncio.run(wait_for_db())