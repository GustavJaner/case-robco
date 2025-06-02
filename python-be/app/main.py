# import secrets
# from typing import Annotated

from fastapi import FastAPI #, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

# from fastapi.responses import JSONResponse
# from fastapi.security import HTTPBasic, HTTPBasicCredentials
# from starlette.requests import Request

# My own modules
from app import Config
from app.routers.v1 import health, robots

app = FastAPI(debug=Config.DEBUG_MODE)
# security = HTTPBasic()

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

app.include_router(health.router, prefix="/health")  # Prefix is used to group the endpoints under /health. @router.get("/bar") would become /health/bar.
app.include_router(robots.router, prefix="/api/v1") # Prefix is used to group the endpoints under /api/v1. @router.get("/bar") would become /api/v1/bar.

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.error")

@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code} for {request.method} {request.url}")
    return response


# def is_valid_credentials(
#     credentials: Annotated[HTTPBasicCredentials, Depends(security)],
# ):
#     current_username_bytes = credentials.username.encode("utf8")
#     correct_username_bytes = Config.BASIC_AUTH_USERNAME.encode("utf8")
#     is_correct_username = secrets.compare_digest(current_username_bytes, correct_username_bytes)
#     current_password_bytes = credentials.password.encode("utf8")
#     correct_password_bytes = Config.BASIC_AUTH_PASSWORD.encode("utf8")
#     is_correct_password = secrets.compare_digest(current_password_bytes, correct_password_bytes)
#     if not (is_correct_username and is_correct_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Basic"},
#         )


# @app.middleware("http")
# async def auth_middleware(request: Request, call_next):
#     try:
#         credentials: HTTPBasicCredentials | None = await security(request)
#         if credentials:
#             is_valid_credentials(credentials)
#         else:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Incorrect username or password",
#                 headers={"WWW-Authenticate": "Basic"},
#             )
#     except HTTPException as e:
#         return JSONResponse(
#             status_code=e.status_code,
#             content={"message": e.detail},
#             headers={"WWW-Authenticate": "Basic"},
#         )
#     response = await call_next(request)
#     return response