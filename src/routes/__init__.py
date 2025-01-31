from fastapi import APIRouter

# Import all route modules
from .users import router as users_router
from .buddy import router as buddy_router
from .dashboard import router as dashboard_router

# Create the main API router
api_router = APIRouter()

# Include all routers with their prefixes
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(buddy_router, prefix="/buddy", tags=["buddy"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"]) 