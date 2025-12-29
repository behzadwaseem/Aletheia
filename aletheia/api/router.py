from fastapi import APIRouter
from aletheia.api.routes import health, recommend


api_v1_router = APIRouter()

api_v1_router.include_router(health.router, tags=["health"])
api_v1_router.include_router(recommend.router, prefix="/recommendations", tags=["recommendations"])