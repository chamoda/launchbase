from fastapi.routing import APIRouter

from .routers import meta, users

router = APIRouter()

router.include_router(meta.router)
router.include_router(users.router)
