from sqlalchemy.orm import Session
from app.models import core as models
from app.models import schemas
from uuid import UUID, uuid4
from sqlalchemy import func


def get_menus(db: Session):
    return db.query(models.Menu).all()

def get_menu(db: Session, menu_id: UUID):
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not menu: return None

    submenus_count = db.query(func.count(models.Submenu.id)).filter(models.Submenu.menu_id == menu_id).scalar()

    dishes_count = db.query(func.count(models.Dish.id)).join(models.Submenu).filter(models.Submenu.menu_id == menu_id).scalar()

    menu.submenus_count = submenus_count
    menu.dishes_count = dishes_count

    return menu


def create_menu(db: Session, menu: schemas.MenuCreate):
    db_menu = models.Menu(
        title=menu.title,
        description=menu.description,
    )
    db.add(db_menu)
    db.commit()
    db.flush()  
    db.refresh(db_menu)

    return db_menu


def update_menu(db: Session, menu_id: UUID, menu_update: schemas.MenuUpdate):
    db_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if db_menu:
        db_menu.title = menu_update.title
        db_menu.description = menu_update.description
        db.commit()
        db.refresh(db_menu)
        return db_menu
    return None

def delete_menu(db: Session, menu_id: UUID):
    db_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if db_menu:
        db.delete(db_menu)
        db.commit()
        return True
    else:
        return False