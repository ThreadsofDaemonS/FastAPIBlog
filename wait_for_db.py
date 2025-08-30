import asyncio
import asyncpg
import os

async def wait_for_db():
    for i in range(20):
        try:
            conn = await asyncpg.connect(
                user=os.getenv("POSTGRES_USER", "postgres"),
                password=os.getenv("POSTGRES_PASSWORD", "password"),
                database=os.getenv("POSTGRES_DB", "blogdb"),
                host="db",
            )
            await conn.close()
            print("✅ DB is ready!")
            return
        except Exception as e:
            print(f"⏳ Waiting for DB... ({i+1}/20)")
            await asyncio.sleep(1)
    print("❌ Could not connect to the database.")
    exit(1)

if __name__ == "__main__":
    asyncio.run(wait_for_db())
