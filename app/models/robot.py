# Defines database models for robots.
# Represents your database table structure and ORM mapping.
# The model is used to interract with the database using SQLAlchemy.
from sqlalchemy import Column, Integer, String
from app.database import Base

class RobotModel(Base):
  __tablename__ = "robots"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(31), index=True)
  type = Column(String(31))
  status = Column(String(15))
  description = Column(String(255))
