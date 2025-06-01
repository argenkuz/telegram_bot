# handlers/user/__init__.py
from .start import router as start_router
from .status import router as status_router
from .help import router as help_router
from .subscribe import router as subscribe_router

from aiogram import Router

routers = Router()
routers.include_router(start_router)
routers.include_router(status_router)
routers.include_router(help_router)
routers.include_router(subscribe_router)
