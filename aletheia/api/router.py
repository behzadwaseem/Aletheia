from fastapi import APIRouter
from aletheia.api.routes import health, recommend, upload


api_v1_router = APIRouter()

api_v1_router.include_router(health.router, tags=["health"])
api_v1_router.include_router(recommend.router, prefix="/recommend", tags=["recommend"])