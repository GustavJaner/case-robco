import asyncio
import sys
from app.database import Base, engine

# Initializes the database by creating all tables defined in app/models.
async def init_db():
  try:
    print(f"🔎 [database] Initializing DB")
    async with engine.begin() as conn: # Connection to the DB engine to manage schema changes.
      await conn.run_sync(Base.metadata.create_all) # Apply the ORM schema models to the DB.
    print("✅ [database] DB initialized successfully")

  except Exception as e:
    print(f"Error initializing database: {e}", file=sys.stderr)
    sys.exit(1)

# To enable running this script directly to init the DB (Run: python app/init_db.py). This won't run if imported as a module.
if __name__ == "__main__":
  asyncio.run(init_db())
