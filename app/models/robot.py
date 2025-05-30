# Defines database models for robots.
# Represents your database table structure and ORM mapping.
# The model is used to interract with the database using SQLAlchemy.
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RobotModel(Base):
  __tablename__ = "robots"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, index=True)
  type = Column(String)
  status = Column(String)
  description = Column(String)
