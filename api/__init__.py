from fastapi import APIRouter
from .services.views import router as task_router

router = APIRouter()
router.include_router(router=task_router)