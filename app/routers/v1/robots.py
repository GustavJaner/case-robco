# REST API:
# ○ GET /robots – returnsrobotswithsomemockrobotstatus.
# ○ POST /robots – addsanewrobot.
# ○ PATCH /robot – updatesarobotdata.

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schemas.robot import Robot
from app.models.robot import RobotModel
from app.database import SessionLocal

robots = [] # Temporary robots list.

router = APIRouter(
  prefix="", # This prefix is used to group the endpoints under /robots. @router.get("/bar") would become /robots/bar.
  tags=["Robot Service"], # This tag is used to group the endpoints in the OpenAPI documentation.
  responses={404: {"description": "Not found"}},
)

# Dependency to get DB session
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@router.post("/robots", description="Create new robot.")
async def create_robot(robot: Robot, db: Session = Depends(get_db)):
  # robots.append(robot)
  db_robot = RobotModel(**robot.dict())
  db.add(db_robot)
  db.commit()
  db.refresh(db_robot)
  return JSONResponse(
    status_code=status.HTTP_200_OK,
    content={"status": "ok", "new robot": robot.model_dump()},
  )

@router.get("/robots", description="Get robots.")
def read_robots(db: Session = Depends(get_db)):
  # db.query(Robot).filter(Robot.id == robot_id).first()
  robots = db.query(Robot).filter(Robot.id == robot_id).first()

  return JSONResponse(
    status_code=status.HTTP_200_OK,
    content={"status": "ok", "robots": [r.model_dump() for r in robots]},
  )

@router.put("/robot/{robot_id}", description="Update existing robot.")
async def update_robot(robot_id: int, updated_robot: Robot):
  for index, robot in enumerate(robots):
    if robot.id == robot_id:
      robots[index] = updated_robot
      return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "ok", "updated robot": updated_robot.model_dump()},
      )
  return JSONResponse(
    status_code=status.HTTP_404_NOT_FOUND,
    content={"error": "Robot with id {robot_id} not found"},
  )
