# # Defines Pydantic schemas for robots.
from pydantic import BaseModel
from typing import Optional
from enum import Enum

class RobotStatus(str, Enum):
  IDLE = "IDLE"
  ACTIVE = "ACTIVE"

class RobotBase(BaseModel):
  id: int
  name: str
  type: str = "foobar"
  status: RobotStatus = RobotStatus.IDLE
  description: Optional[str] = None

class RobotCreate(RobotBase): # Used for validating data when creating a new robot.
  pass

class Robot(RobotBase):
  # id: int

  class Config:
    from_attributes = True
