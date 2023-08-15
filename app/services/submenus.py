
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST
from sqlalchemy import func  
from fastapi.responses import JSONResponse

from app.models import core as models
from typing import List, Optional

from app.models import schemas
from uuid import UUID

from app.services import menus as menu_service


def get_submenus(db: Session, menu_id: UUID):
    submenus = db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).all()
    for submenu in submenus:
        submenu.dishes_count = len(submenu.dishes)
    return submenus



def get_submenu(db: Session, submenu_id: UUID):
    db_submenu = db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()

    if db_submenu is None:
        return JSONResponse(content={"detail":"submenu not found"}, status_code=404)
    else:
        dishes_count = len(db_submenu.dishes)  
    
        submenu_response = {
            "id": db_submenu.id,
            "title": db_submenu.title,
            "description": db_submenu.description,
            "dishes_count": dishes_count
        }
        return submenu_response

    
def create_submenu(db: Session, submenu: schemas.SubmenuCreate, menu_id: UUID):
    db_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    db_submenu = models.Submenu(title=submenu.title, description=submenu.description, menu_id=menu_id)
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu


def update_submenu(db: Session, submenu_id: UUID, submenu_update: schemas.SubmenuUpdate):
    db_submenu = db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()
    if not db_submenu:
        raise HTTPException(status_code=404, detail="Submenu not found")

    for key, value in submenu_update.dict(exclude_unset=True).items():
        setattr(db_submenu, key, value)

    db.commit()
    db.refresh(db_submenu)
    return db_submenu



def delete_submenu(db: Session, submenu_id: UUID):
    db_submenu = db.query(models.Submenu).filter(models.Submenu.id == submenu_id).first()
    if db_submenu:
        db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).delete()
        db.delete(db_submenu)
        db.commit()
        return True
    return False