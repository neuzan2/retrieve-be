from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()


class Health(BaseModel):
    status: str


@router.get("/health", response_model=Health, tags=["health"])
async def health():
    """
    Health check endpoint.
    """
    return Health(status="ok")
