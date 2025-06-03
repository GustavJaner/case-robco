from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
# from app.config import settings

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+asyncpg://robotuser:password@localhost:5432/robotdb")

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False) # The SQLAlchemy ORM session that manages the database transactions(write/read from tables).
Base = declarative_base() # The ORM models should inherit from this base.
