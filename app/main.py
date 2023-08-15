from fastapi import FastAPI, APIRouter

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from typing import List, Dict

import app.models.core
from app.models.database import engine

app.models.core.Base.metadata.create_all(bind=engine)

from app.routers.menus import menu_router
from app.routers.dishes import dish_router
from app.routers.submenus import submenu_router



app = FastAPI()

app.include_router(menu_router)
app.include_router(dish_router)
app.include_router(submenu_router)