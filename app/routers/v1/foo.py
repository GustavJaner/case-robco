from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/foo",
    tags=["Foo"],
    responses={404: {"description": "Not found"}},
)

@router.get("", description="Foo stuff")
async def root():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "ok:)"})
