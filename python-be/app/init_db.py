import asyncio
from app.database import engine
from app.models.robot import Base

# Initializes the database by creating all tables defined in the models.
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# To enable running this script directly to init the DB.
if __name__ == "__main__":
    asyncio.run(init_db())
