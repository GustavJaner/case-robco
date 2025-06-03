"""
REST API:
   - GET /robots returns robots with some mock robot status.
   - POST /robots adds a new robot.
   - PATCH /robot updates a robot data.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import SessionLocal
from app.models.robot import RobotORM
from app.schemas.robot import Robot, RobotCreate, RobotUpdate

async def get_db():
  async with SessionLocal() as session:
    yield session

router = APIRouter(
  prefix="", # This prefix is used to group the endpoints under /robots. @router.get("/bar") would become /robots/bar.
  tags=["Robot Service"], # This tag is used to group the endpoints in the OpenAPI documentation.
  responses={404: {"description": "Not found"}},
)

@router.post("/robots", description="Create new robot")
async def create_robot(robot_new: RobotCreate, db: AsyncSession = Depends(get_db)):
  robot = Robot.model_validate(robot_new) # Validate and convert the RobotCreate object to a Robot object (Implicitly generating and adding the ID field).
  robot_orm = RobotORM(
    id=robot.id,
    name=robot.name,
    type=robot.type.value,
    status=robot.status.value,
    description=robot.description,
  )
  db.add(robot_orm)
  try:
    await db.commit() # Commit the transaction to save the new robot to the database.
    await db.refresh(robot_orm) # Refresh the robot_orm object to get the updated state from the database.
  except IntegrityError:
    await db.rollback() # Undo any changes made during the transaction if an integrity error occurs (e.g., duplicate ID).
    return {
      "status": "error",
      "error": "Robot with this ID already exists",
    }, 400
  return {
    "status": "ok",
    "message": f"Robot with ID={robot.id} created successfully",
    "data": {"robot_new": Robot.model_validate(robot_orm, from_attributes=True).model_dump()},
  }

@router.get("/robots", description="Get robots")
async def read_robots(db: AsyncSession = Depends(get_db)):
  result = await db.execute(select(RobotORM)) # Fetch all rows of robots from the database table.
  robots = result.scalars().all() # Convert the result to a list of RobotORM objects.
  return {
    "status": "ok",
    "message": "Robots retrieved successfully",
    "data": {
      "robots": [Robot.model_validate(r, from_attributes=True).model_dump() for r in robots],
    },
  }

@router.patch("/robot/{robot_id}", description="Update existing robot")
async def update_robot(robot_id: str, robot_updated_config: RobotUpdate, db: AsyncSession = Depends(get_db)):
  result = await db.execute(select(RobotORM).where(RobotORM.id == robot_id))
  robot_orm = result.scalar_one_or_none()
  if robot_orm is None:
    return {
      "status": "error",
      "error": f"Robot with ID={robot_id} not found",
    }, 404
  # Save original config for response.
  robot_original = Robot.model_validate(robot_orm, from_attributes=True)
  update_data = robot_updated_config.model_dump(exclude_unset=True)
  for field, value in update_data.items():
    if field in ["type", "status"] and value is not None:
      value = value.value  # Convert Enum to string.
    setattr(robot_orm, field, value)
  try:
    await db.commit()
    await db.refresh(robot_orm)
  except Exception as e:
    await db.rollback()
    return {
      "status": "error",
      "error": str(e),
    }, 400
  return {
    "status": "ok",
    "message": f"Robot with ID={robot_id} updated successfully",
    "data": {
      "robot_original_config": robot_original.model_dump(),
      "robot_updated": Robot.model_validate(robot_orm, from_attributes=True).model_dump(),
    },
  }
