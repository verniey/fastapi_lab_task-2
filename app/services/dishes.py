from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from app.models import core as models
from fastapi.responses import JSONResponse

from app.models import schemas

from uuid import UUID

from app.models.database import get_db
from app.models import schemas
from app.services import menus as menu_service


def get_dishes(db: Session, submenu_id: UUID):
    dishes = db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).all()
    return dishes


def get_dish(db: Session, submenu_id: UUID, dish_id: UUID):
    dish = db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id, models.Dish.id == dish_id).first()

    return dish

def create_dish(db: Session, dish: schemas.DishCreate, submenu_id: UUID):
    db_dish = models.Dish(
        title=dish.title,
        description=dish.description,
        price=dish.price,
        submenu_id=submenu_id
    )
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish


def update_dish(db: Session, dish_id: UUID, dish_update: schemas.DishUpdate):
    db_dish = db.query(models.Dish).filter(models.Dish.id == dish_id).first()
    if not db_dish:
        return JSONResponse(status_code=404, detail="dish not found")

    # Check if the Dish is linked to a Submenu
    if db_dish.submenu_id is None:
        return JSONResponse(status_code=400, detail="Dish cannot be linked directly to a Menu")

    for key, value in dish_update.dict(exclude_unset=True).items():
        setattr(db_dish, key, value)

    # Check if the Dish is already linked to another Submenu
    if 'submenu_id' in dish_update and dish_update.submenu_id != db_dish.submenu_id:
        existing_dish = db.query(models.Dish).filter(models.Dish.submenu_id == dish_update.submenu_id).first()
        if existing_dish:
            return JSONResponse(status_code=400, detail="Dish already exists in another Submenu")

    db.commit()
    db.refresh(db_dish)
    return db_dish



def delete_dish(db: Session, dish_id: UUID):
    db_dish = db.query(models.Dish).filter(models.Dish.id == dish_id).first()
    if db_dish:
        db.delete(db_dish)
        db.commit()    
        return {"status": true, "mesage": "The dish has been deleted"}

    
    raise HTTPException(status_code=404, detail="dish not found")