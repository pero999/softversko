"""API rute."""

from app.routes.auth import router as auth_router
from app.routes.menu import router as menu_router
from app.routes.orders import router as orders_router

__all__ = ["auth_router", "menu_router", "orders_router"]
