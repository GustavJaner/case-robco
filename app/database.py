# Request: User sends JSON data → FastAPI uses Pydantic schema to validate.
# Processing: You convert the Pydantic object to a SQLAlchemy model instance and save it to the database.
# Response: You fetch SQLAlchemy model instances from the database, convert them to Pydantic schemas, and return as JSON.

# Pydantic schema: Validates and serializes data.
# SQLAlchemy model: Maps to the database table.
# Database: Stores the data.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./robots.db"  # You can change this to your preferred database URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
