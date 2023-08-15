from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.models.database import get_db
from app.models import schemas
import pytest
from app.models.database import engine
from app.models.core import Base
client = TestClient(app)

# Create the tables before tests
@pytest.fixture(scope="module", autouse=True)
def create_tables():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db():
    with Session(engine) as session:
        yield session
        session.rollback()


def test_get_dishes_empty(db: Session):
    # Create a menu
    menu_data = {
        "title": "Test Menu",
        "description": "Test menu description"
    }
    response = client.post("/api/v1/menus", json=menu_data)
    assert response.status_code == 201
    menu_id = response.json()["id"]

    # Create a submenu associated with the created menu
    submenu_data = {
        "title": "Test Submenu",
        "description": "My test submenu description"
    }
    response = client.post(f"/api/v1/menus/{menu_id}/submenus", json=submenu_data)
    assert response.status_code == 201
    submenu_id = response.json()["id"]

    # Fetch dishes for the created submenu
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")

    assert response.status_code == 200
    assert len(response.json()) == 0



def test_get_dishes_not_empty(db: Session):
    # Create a menu
    menu_data = {
        "title": "Test Menu",
        "description": "Test menu description"
    }
    response = client.post("/api/v1/menus", json=menu_data)
    assert response.status_code == 201
    menu_id = response.json()["id"]

    # Create a submenu associated with the created menu
    submenu_data = {
        "title": "Test Submenu",
        "description": "My test submenu description"
    }
    response = client.post(f"/api/v1/menus/{menu_id}/submenus", json=submenu_data)
    assert response.status_code == 201
    submenu_id = response.json()["id"]

    # Create a dish associated with the created submenu
    dish_data = {
        "title": "Test Dish",
        "description": "My test dish description",
        "price": 9.99
    }
    response = client.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json=dish_data)
    assert response.status_code == 201

    # Fetch dishes for the created submenu
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")

    assert response.status_code == 200
    assert len(response.json()) == 1

def test_create_dish(db: Session):
    # Create a menu
    menu_data = {
        "title": "Test Menu",
        "description": "Test menu description"
    }
    response = client.post("/api/v1/menus", json=menu_data)
    assert response.status_code == 201
    menu_id = response.json()["id"]

    # Create a submenu associated with the created menu
    submenu_data = {
        "title": "Test Submenu",
        "description": "My test submenu description"
    }
    response = client.post(f"/api/v1/menus/{menu_id}/submenus", json=submenu_data)
    assert response.status_code == 201
    submenu_id = response.json()["id"]

    # Create a dish associated with the created submenu
    dish_data = {
        "title": "Test Dish",
        "description": "My test dish description",
        "price": '9.99'
    }
    response = client.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json=dish_data)

    assert response.status_code == 201
    assert response.json()["title"] == dish_data["title"]
    assert response.json()["description"] == dish_data["description"]
    assert response.json()["price"] == dish_data["price"]


def test_get_dish_by_id(db: Session):
    # Create a menu
    menu_data = {
        "title": "Test Menu",
        "description": "Test menu description"
    }
    response = client.post("/api/v1/menus", json=menu_data)
    assert response.status_code == 201
    menu_id = response.json()["id"]

    # Create a submenu associated with the created menu
    submenu_data = {
        "title": "Test Submenu",
        "description": "My test submenu description"
    }
    response = client.post(f"/api/v1/menus/{menu_id}/submenus", json=submenu_data)
    assert response.status_code == 201
    submenu_id = response.json()["id"]

    # Create a dish associated with the created submenu
    dish_data = {
        "title": "Test Dish",
        "description": "My test dish description",
        "price": '9.99'
    }
    response = client.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json=dish_data)
    assert response.status_code == 201
    dish_id = response.json()["id"]

    # Fetch the created dish by its ID
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200
    assert response.json()["title"] == dish_data["title"]
    assert response.json()["description"] == dish_data["description"]
    assert response.json()["price"] == dish_data["price"]


def test_update_dish(db: Session):
    # Create a menu
    menu_data = {
        "title": "Test Menu",
        "description": "Test menu description"
    }
    response = client.post("/api/v1/menus", json=menu_data)
    assert response.status_code == 201
    menu_id = response.json()["id"]

    # Create a submenu associated with the created menu
    submenu_data = {
        "title": "Test Submenu",
        "description": "My test submenu description"
    }
    response = client.post(f"/api/v1/menus/{menu_id}/submenus", json=submenu_data)
    assert response.status_code == 201
    submenu_id = response.json()["id"]

    # Create a dish associated with the created submenu
    dish_data = {
        "title": "Test Dish",
        "description": "My test dish description",
        "price": 9.99
    }
    response = client.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json=dish_data)
    assert response.status_code == 201
    dish_id = response.json()["id"]

    # Update the dish's information
    updated_dish_data = {
        "title": "Updated Dish Title",
        "description": "Updated dish description",
        "price": '12.99'
    }
    response = client.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", json=updated_dish_data)
    assert response.status_code == 200

    # Fetch the updated dish and verify the changes
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200
    assert response.json()["title"] == updated_dish_data["title"]
    assert response.json()["description"] == updated_dish_data["description"]
    assert response.json()["price"] == updated_dish_data["price"]

def test_delete_dish(db: Session):
    # Create a menu
    menu_data = {
        "title": "Test Menu",
        "description": "Test menu description"
    }
    response = client.post("/api/v1/menus", json=menu_data)
    assert response.status_code == 201
    menu_id = response.json()["id"]

    # Create a submenu associated with the created menu
    submenu_data = {
        "title": "Test Submenu",
        "description": "My test submenu description"
    }
    response = client.post(f"/api/v1/menus/{menu_id}/submenus", json=submenu_data)
    assert response.status_code == 201
    submenu_id = response.json()["id"]

    # Create a dish associated with the created submenu
    dish_data = {
        "title": "Test Dish",
        "description": "My test dish description",
        "price": '9.99'
    }
    response = client.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json=dish_data)
    assert response.status_code == 201
    dish_id = response.json()["id"]

    # Delete the created dish
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200

    # Try to fetch the deleted dish and ensure it's not found
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 404

