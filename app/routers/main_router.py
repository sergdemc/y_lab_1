from fastapi import APIRouter

from routers.menu_router import menu_router
from routers.submenu_router import submenu_router
from routers.dish_router import dish_router

# main_router = APIRouter()
# main_router.include_router(menu_router, prefix='/menus')
# main_router.include_router(submenu_router, prefix='/submenus')
# main_router.include_router(dish_router, prefix='/dishes')
