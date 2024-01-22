import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.db import Base, engine
from config import PORT
from routers.menu_router import menu_router
from routers.submenu_router import submenu_router
from routers.dish_router import dish_router

Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)


app.include_router(menu_router, prefix='/api/v1')
app.include_router(submenu_router, prefix='/api/v1')
app.include_router(dish_router, prefix='/api/v1')

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=PORT or 8080, reload=True, workers=3)
