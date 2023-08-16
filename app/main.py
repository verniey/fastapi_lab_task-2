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
from app.models import core as models



app = FastAPI()

app.include_router(menu_router)
app.include_router(dish_router)
app.include_router(submenu_router)

def reset_database():
    try:
        with Session(engine) as db:
            db.query(models.Submenu).delete()
            db.query(models.Menu).delete()
            db.query(models.Dish).delete()
            db.commit()
    except Exception as e:
        print(f"An exception occurred while resetting the database: {e}")

# Clear and reset the database on app startup
reset_database()
