# ORM (Object-Relational Mapping) models are defined using the base class.
# ORM models represent the database tables and their relationships.
from sqlalchemy import Column, String, Enum as SqlEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from app.schemas.robot import RobotType, RobotStatus
# import uuid

# Each instance of the RobotORM class represents a table row in the database.
class RobotORM(Base):
  __tablename__ = "robots"

  id = Column(UUID(as_uuid=True), primary_key=True, index=True) #, default=uuid.uuid4)
  name = Column(String(31), index=True)
  type = Column(SqlEnum(RobotType, name="robottype_enum"), nullable=False)
  status = Column(SqlEnum(RobotStatus, name="robotstatus_enum"), nullable=False)
  description = Column(String(255), nullable=True)
