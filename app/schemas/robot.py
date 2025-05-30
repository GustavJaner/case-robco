# # Defines Pydantic schemas for robots.
from pydantic import BaseModel
from typing import Optional

class RobotBase(BaseModel):
  id: int
  name: str
  type: str = "foobar"
  status: str = "idle"
  description: Optional[str] = None

class RobotCreate(RobotBase): # Used for validating data when creating a new robot.
  pass

class Robot(RobotBase):
  # id: int

  class Config:
    from_attributes = True
