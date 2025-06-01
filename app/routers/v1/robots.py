# REST API:
# ○ GET /robots – returns robots with some mock robot status.
# ○ POST /robots – adds a new robot.
# ○ PATCH /robot – updates a robot data.

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.schemas.robot import Robot, RobotCreate, RobotUpdate
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
    status_code = status.HTTP_200_OK,
    content = {
      "status": "ok",
      "message": f"Robot with ID={robot.id} created successfully",
      "data": {
        "robot_new": robot.model_dump(),
      },
    },
  )

@router.get("/robots", description="Get robots")
def read_robots():
  return JSONResponse(
    status_code = status.HTTP_200_OK,
    content = {
      "status": "ok",
      "message": "Robots retrieved successfully",
      "data": {
        "robots": [r.model_dump() for r in robots.values()],
      },
    },
  )

@router.patch("/robot/{robot_id}", description="Update existing robot")
async def update_robot(robot_id: str, robot_updated_config: RobotUpdate):
  if robot_id in robots:
    robot_to_update = robots[robot_id]
    robot_original_config = Robot(**robot_to_update.model_dump())

    # Update only fields provided in the PATCH request
    update_data = robot_updated_config.model_dump(exclude_unset=True)
    for field, value in update_data.items():
      setattr(robot_to_update, field, value)

    return JSONResponse(
      status_code = status.HTTP_200_OK,
      content = {
        "status": "ok",
        "message": f"Robot with ID={robot_id} updated successfully",
        "data": {
          "robot_original_config": robot_original_config.model_dump(),
          "robot_updated": robots[robot_id].model_dump(),
        },
      },
    )

  else:
    return JSONResponse(
      status_code = status.HTTP_404_NOT_FOUND,
      content = {
        "status": "error",
        "error": f"Robot with ID={robot_id} not found",
      },
    )
