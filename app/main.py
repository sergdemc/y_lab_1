import uvicorn
from config import PORT
from database.db import Base, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRouter
from routers.dish_router import dish_router
from routers.menu_router import menu_router
from routers.submenu_router import submenu_router

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title='Restaurant API',
    description='API for restaurant menu',
    version='1.0.0',
    openapi_url='/api/v1/openapi.json',
    redoc_url=None
)


class CustomAPIRouter(APIRouter):

    def reverse(self, route_name: str, **path_params) -> str:
        for route in self.routes:
            if route.name == route_name:
                return route.path_format.format_map(path_params)
        raise ValueError(f"No route found with name '{route_name}'")


origins = [
    'http://localhost',
    'http://localhost:8000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
    allow_headers=['*'],
)

app.router = CustomAPIRouter()
app.include_router(menu_router, prefix='/api/v1')
app.include_router(submenu_router, prefix='/api/v1')
app.include_router(dish_router, prefix='/api/v1')

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=PORT or 8080, reload=True, workers=3)
