import logging

from fastapi import APIRouter

from app.api.v1.endpoints import file_router, user_router, scope_router, auth_router, \
    configuration_router, items_router

logger = logging.getLogger(__name__)

tags_metadata = [
    {
        "items": "items",
        "description": "Manage items.",
    },
]

v1_router = APIRouter()
v1_router.include_router(scope_router.router, prefix="/scopes", tags=["scopes"])
v1_router.include_router(user_router.router, prefix="/users", tags=["users"])
v1_router.include_router(auth_router.router, prefix="/auth", tags=["auth"])
v1_router.include_router(configuration_router.router, prefix="/configuratios", tags=["configurations"])
v1_router.include_router(items_router.router, prefix="/items", tags=["items"])
v1_router.include_router(file_router.router, prefix="/file", tags=["items"])


