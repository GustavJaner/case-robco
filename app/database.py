# Request: User sends JSON data → FastAPI uses Pydantic schema to validate.
# Processing: You convert the Pydantic object to a SQLAlchemy model instance and save it to the database.
# Response: You fetch SQLAlchemy model instances from the database, convert them to Pydantic schemas, and return as JSON.

# Pydantic schema: Validates and serializes data.
# SQLAlchemy model: Maps to the database table.
# Database: Stores the data.

# On the database side, SQLAlchemy is one of the most mature and flexible ORMs (Object Relational Mappers) for Python. It allows you to interact with databases using Python objects rather than writing raw SQL.

#     ORM Abstraction: Maps database tables to Python classes and records to Python objects.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/dbname"

engine = create_engine(DATABASE_URL) # MySQL dialect (mysql+pymysql) with the pymysql driver.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # The SQLAlchemy session that manages database transactions.
Base = declarative_base() # Models will inherit from this base.
