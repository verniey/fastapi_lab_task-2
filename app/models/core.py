from sqlalchemy import Column, Integer, String, Float, ForeignKey, Numeric, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from app.models.database import get_db as db

Base = declarative_base()



class Menu(Base):
    __tablename__ = "menus"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, index=True, unique=False)
    description = Column(String, index=True)
    submenus_count = Column(Integer, default=0)
    dishes_count = Column(Integer, default=0)
    submenus = relationship("Submenu", back_populates="menu", cascade="all, delete")


    def get_submenus_and_dishes_count(self, session):
    
        submenus_count = (
            session.query(Submenu)
            .filter(Submenu.menu_id == self.id)
            .count()
        )
        dishes_count = (
            session.query(Dish)
            .join(Submenu, Dish.submenu_id == Submenu.id)
            .filter(Submenu.menu_id == self.id)
            .count()
        )
        return submenus_count, dishes_count


class Submenu(Base):
    __tablename__ = "submenus"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, index=True, unique=False)
    description = Column(String, nullable=True, unique=False)
    dishes_count = Column(Integer, default=0)
    menu_id = Column(UUID(as_uuid=True), ForeignKey("menus.id"))
    
    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dish", back_populates="submenu", cascade="all, delete")

    

class Dish(Base):
    __tablename__ = "dishes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    
    submenu_id = Column(UUID(as_uuid=True), ForeignKey("submenus.id"))
    submenu = relationship("Submenu", back_populates="dishes")
