from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="",
    tags=["Health"],
    responses={404: {"description": "Not found"}},
)

@router.get("", description="Health check API availability")
async def root():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "ok"})
