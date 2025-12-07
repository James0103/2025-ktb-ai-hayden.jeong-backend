"""
API routers for the application
Handles all route definitions and endpoint organization
"""

from .user import router as user_router
from .post import router as post_router
from .relay_story import router as relay_story_router

__all__ = [
    "user_router",
    "post_router",
    "relay_story_router",
]
