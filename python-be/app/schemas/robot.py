# Defines Pydantic schemas for robots.
# # These schemas are used for validating and serializing data in the API.
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from uuid import UUID, uuid4

class RobotType(str, Enum):
  FOOBOT = "foo-bot"
  BARBOT = "bar-bot"

class RobotStatus(str, Enum):
  IDLE   = "IDLE"
  ACTIVE = "ACTIVE"
  ERROR  = "ERROR"

# Defines the base schema for robots. Fields, types and default values.
class RobotBase(BaseModel):
  id: UUID = Field(default_factory=uuid4) # Auto-generate a new UUID for each robot.
  name: str
  type: RobotType = RobotType.FOOBOT
  status: RobotStatus = RobotStatus.IDLE
  description: Optional[str] = None

# Schema to validate user input data when creating a new robot.
# This class defines what fields a user can use when creating a new robot ex. with the with POST request.
class RobotCreate(BaseModel):
  name: str
  type: RobotType
  status: RobotStatus
  description: Optional[str] = None

# Schema to validate user input data when update existing robots. All fields are optional, allowing partial updates.
class RobotUpdate(BaseModel):  # Used for validating data when creating a new robot.
  name: Optional[str] = None
  type: Optional[RobotType] = None
  status: Optional[RobotStatus] = None
  description: Optional[str] = None

# The Robot schema extends the base schema and is used for returning robot data.
class Robot(RobotBase):
  model_config = {
    "from_attributes": True  # ORM mode, allows to use attributes from the ORM model directly.
  }
