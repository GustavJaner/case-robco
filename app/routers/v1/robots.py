# REST API:
# ○ GET /robots – returnsrobotswithsomemockrobotstatus.
# ○ POST /robots – addsanewrobot.
# ○ PATCH /robot – updatesarobotdata.

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.schemas.robot import Robot, RobotCreate
# from app.models import RobotModel
# from app.database import SessionLocal

# Temporary robot dict.
robots = {}

router = APIRouter(
  prefix="", # This prefix is used to group the endpoints under /robots. @router.get("/bar") would become /robots/bar.
  tags=["Robot Service"], # This tag is used to group the endpoints in the OpenAPI documentation.
  responses={404: {"description": "Not found"}},
)

# def get_db():
#   db = SessionLocal()
#   try:
#     yield db
#   finally:
#     db.close()

@router.post("/robots", description="Create new robot")
def create_robot(robot_new: RobotCreate):
  robot = Robot.model_validate(robot_new) # Validate and convert the RobotCreate object to a Robot object (Adding the ID field).
  robots[robot.id] = robot
  return JSONResponse(
    status_code=status.HTTP_200_OK,
    content={"status": "ok", "robot_new": robot.model_dump()},
  )

@router.get("/robots", description="Get robots")
def read_robots():
  return JSONResponse(
    status_code=status.HTTP_200_OK,
    content={"status": "ok", "robots": [r.model_dump() for r in robots.values()]},
  )

@router.put("/robot/{robot_id}", description="Update existing robot")
async def update_robot(robot_id: str, robot_updated_config: RobotCreate):
  if robot_id in robots:
    robot_to_update = robots[robot_id]
    robot_original_config = Robot(**robot_to_update.model_dump())

    # Update only the editable fields, keeping the original id.
    robot_to_update.name = robot_updated_config.name
    robot_to_update.type = robot_updated_config.type
    robot_to_update.status = robot_updated_config.status
    robot_to_update.description = robot_updated_config.description
    return JSONResponse(
      status_code=status.HTTP_200_OK,
      content={"status": "ok", "robot_original_config": robot_original_config.model_dump(), "robot_updated": robots[robot_id].model_dump()},
    )

  # If the robot with the given ID does not exist, return a 404 error.
  else:
    return JSONResponse(
      status_code=status.HTTP_404_NOT_FOUND,
      content={"error": f"Robot with id {robot_id} not found"},
    )
