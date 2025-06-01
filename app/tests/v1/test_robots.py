import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# robots = [
#   Robot(
#     id="295091f5-7c9c-40d8-9578-5fc7ac75fac8",
#     name="R2D2",
#     type="foo-bot",
#     status="ACTIVE",
#     description=""
#   ),
#   Robot.model_validate(RobotCreate(
#     name="C3PO",
#     type="bar-bot",
#     status="IDLE",
#     description="Lorem ipsum"
#   ))
# ]

def test_create_robot_endpoint():
  robot_new = {
    "name": "TestBot01",
    "type": "foo-bot",
    "status": "IDLE",
    "description": "Test robot"
  }
  response = client.post("/api/v1/robots", json=robot_new)
  assert response.status_code == 200
  data = response.json()
  assert data["status"] == "ok"
  assert data["data"]["robot_new"]["name"] == robot_new["name"]

def test_read_robots_endpoint():
  response = client.get("/api/v1/robots")
  assert response.status_code == 200
  data = response.json()
  assert data["status"] == "ok"
  assert len(data["data"]["robots"]) == 1  # Assuming we have one robot created in the previous test.

def test_update_robot_endpoint():
  data = client.get("/api/v1/robots").json()
  robot_id = data["data"]["robots"][0]["id"]  # Get the ID of the first robot (To update it).
  assert robot_id is not None

  robot_updated_config = {
    "name": "UpdatedBot",
    "type": "bar-bot",
    "status": "ACTIVE",
    "description": "Updated description"
  }

  response = client.put(f"/api/v1/robot/{robot_id}", json=robot_updated_config)
  assert response.status_code == 200
  data = response.json()
  assert data["status"] == "ok"
  assert data["data"]["robot_updated"]["id"] == robot_id, "Robot ID should not change"
  assert data["data"]["robot_updated"]["name"] == robot_updated_config["name"]
