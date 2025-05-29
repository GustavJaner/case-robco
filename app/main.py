# import secrets
# from typing import Annotated

from fastapi import FastAPI #, Depends, HTTPException, status
# from fastapi.responses import JSONResponse
# from fastapi.security import HTTPBasic, HTTPBasicCredentials
# from starlette.requests import Request

from app import Config
from app.routers.v1 import health, foo

app = FastAPI(debug=Config.DEBUG_MODE)
# security = HTTPBasic()

app.include_router(health.router, prefix="/health")
app.include_router(foo.router, prefix="/api/v1")


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