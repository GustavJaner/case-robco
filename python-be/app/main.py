from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from app.config import settings
from app.routers.v1 import health, robots
from app.init_db import init_db
import asyncio

app = FastAPI(debug=settings.DEBUG_MODE)

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger("uvicorn.error")

# CORS middleware to allow requests from the React FE.
origins = [
  os.environ.get("FRONTEND_ORIGIN", "http://localhost:3000") # Reads the frontend origin from env variable at runtime.
]
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

@app.on_event("startup") # FastAPI will run this function when app starts.
async def on_startup():
  await init_db() # Initialize the database. This creates the tables defined in app/models.

# @app.middleware("http")
# async def log_requests(request, call_next):
#   logger.info(f"Incoming request: {request.method} {request.url}")
#   response = await call_next(request)
#   logger.info(f"Response status: {response.status_code} for {request.method} {request.url}")
#   return response

# Backend API endpoints.
app.include_router(health.router, prefix="/health")
app.include_router(robots.router, prefix="/api/v1") # Prefix is used to group the endpoints under /api/v1. @router.get("/bar") would become /api/v1/bar.
