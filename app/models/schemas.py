from typing import List, Optional
from pydantic import BaseModel, validator
from decimal import Decimal

from uuid import UUID
from pydantic import Field

class DishBase(BaseModel):
    title: str
    description: str

class DishCreate(DishBase):
    price: Decimal

class Dish(DishBase):
    id:  UUID
    price: Decimal  # Custom field to represent price as a formatted string

    class Config:
        orm_mode = True
        from_attributes = True

class DishUpdate(DishBase):
    price: Decimal  # Assuming that the price is stored as a Decimal type



class SubmenuBase(BaseModel):
    title: str
    description: Optional[str] = None

class SubmenuCreate(SubmenuBase):
    pass

class Submenu(SubmenuBase):
    id: UUID   
    dishes_count: int = 0
    
    class Config:
        orm_mode = True
        #exclude = ("dishes",)  # Exclude the 'dishes' field from the response


class SubmenuUpdate(BaseModel):
    title: str
    description: str


class MenuBase(BaseModel):
    title: str
    description: Optional[str] = None

class MenuCreate(MenuBase):
    pass


class MenuUpdate(BaseModel):
    title: str
    description: str

class Menu(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    submenus_count: int
    dishes_count: int


class MenuResponse(Menu):
    id: Optional[int]  # The id is optional in the response
