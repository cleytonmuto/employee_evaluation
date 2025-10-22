from fastapi import APIRouter
from app.api.v1 import auth, users, sectors, evaluations

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(sectors.router, prefix="/sectors", tags=["sectors"])
api_router.include_router(evaluations.router, prefix="/evaluations", tags=["evaluations"])
