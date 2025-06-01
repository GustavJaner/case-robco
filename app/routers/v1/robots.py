# REST API:
# ○ GET /robots – returnsrobotswithsomemockrobotstatus.
# ○ POST /robots – addsanewrobot.
# ○ PATCH /robot – updatesarobotdata.

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.schemas.robot import Robot, RobotCreate
# from app.models import RobotModel
# from app.database import SessionLocal

# Temporary robot list.
robots = [
    Robot(
        id="295091f5-7c9c-40d8-9578-5fc7ac75fac8",
        name="R2D2",
        type="foo-bot",
        status="ACTIVE",
        description=""
    ),
    Robot.model_validate(RobotCreate(
        name="C3PO",
        type="bar-bot",
        status="IDLE",
        description="Lorem ipsum"
    ))
]

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

@router.post("/robots", description="Create new robot.")
def create_robot(robot_new: RobotCreate):
  robot = Robot.model_validate(robot_new) # Validate and convert the RobotCreate object to a Robot object (Adding the ID field).
  robots.append(robot)
  return JSONResponse(
    status_code=status.HTTP_200_OK,
    content={"status": "ok", "new robot": robot.model_dump()},
  )

@router.get("/robots", description="Get robots.")
def read_robots():
  return JSONResponse(
    status_code=status.HTTP_200_OK,
    content={"status": "ok", "robots": [r.model_dump() for r in robots]},
  )

@router.put("/robot/{robot_id}", description="Update existing robot.")
async def update_robot(robot_id: int, robot_updated: RobotCreate):
  for index, robot in enumerate(robots):
    if robot.id == robot_id:
      robot_og = robots[index]
      # Update only the editable fields, keeping the original id.
      robot.name = robot_updated.name
      robot.type = robot_updated.type
      robot.status = robot_updated.status
      robot.description = robot_updated.description
      return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "ok", "original robot": robot_og.model_dump(), "updated robot": robots[robot_id].model_dump()},
      )
  return JSONResponse(
    status_code=status.HTTP_404_NOT_FOUND,
    content={"error": f"Robot with id {robot_id} not found"},
  )
