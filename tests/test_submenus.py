from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.models.database import get_db
from app.models import schemas
from app.models.core import Base
from app.models.core import Submenu
from app.models.database import engine

import pytest
from uuid import uuid4


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

def test_get_submenus_empty(db: Session):
    # Create a menu to use its ID
    menu_data = {
        "title": "Test Menu",
        "description": "Test menu description"
    }
    response = client.post("/api/v1/menus", json=menu_data)
    assert response.status_code == 201
    menu_id = response.json()["id"]

    # Fetch submenus for the created menu
    response = client.get(f"/api/v1/menus/{menu_id}/submenus")

    assert response.status_code == 200
    assert response.json() == []


def test_get_submenus_not_empty(db: Session):
    # Create a menu
    menu_data = {
        "title": "Test Menu",
        "description": "Test menu description"
    }
    response = client.post("/api/v1/menus", json=menu_data)
    assert response.status_code == 201
    menu_id = response.json()["id"]

    # Create multiple submenus associated with the created menu
    submenu_data_list = [
        {
            "title": "Submenu 1",
            "description": "Submenu 1 description"
        },
        {
            "title": "Submenu 2",
            "description": "Submenu 2 description"
        },
        {
            "title": "Submenu 3",
            "description": "Submenu 3 description"
        }
    ]
    
    for submenu_data in submenu_data_list:
        response = client.post(f"/api/v1/menus/{menu_id}/submenus", json=submenu_data)
        assert response.status_code == 201

    # Fetch submenus for the created menu
    response = client.get(f"/api/v1/menus/{menu_id}/submenus")

    assert response.status_code == 200
    assert len(response.json()) == len(submenu_data_list)

def test_get_submenu_by_id(db: Session):
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

    # Fetch the created submenu by its ID
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")

    assert response.status_code == 200
    assert response.json()["id"] == submenu_id
    assert response.json()["title"] == submenu_data["title"]
    assert response.json()["description"] == submenu_data["description"]


def test_update_submenu(db: Session):
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

    # Update the submenu
    updated_data = {
        "title": "Updated Submenu Title",
        "description": "Updated submenu description"
    }
    response = client.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}", json=updated_data)
    assert response.status_code == 200

    # Fetch the updated submenu and verify its attributes
    updated_submenu = response.json()
    assert updated_submenu["title"] == updated_data["title"]
    assert updated_submenu["description"] == updated_data["description"]


def test_create_submenu(db: Session):
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

    # Fetch the created submenu and verify its attributes
    created_submenu = response.json()
    assert "id" in created_submenu
    assert created_submenu["title"] == submenu_data["title"]
    assert created_submenu["description"] == submenu_data["description"]
    assert created_submenu["dishes_count"] == 0  # Assuming no dishes are added yet

def test_delete_submenu_not_found(db: Session):
    # Create a menu
    menu_data = {
        "title": "Test Menu",
        "description": "Test menu description"
    }
    response = client.post("/api/v1/menus", json=menu_data)
    assert response.status_code == 201
    menu_id = response.json()["id"]

    # Attempt to delete a submenu that doesn't exist
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{uuid4()}")
    assert response.status_code == 404

def test_delete_submenu_found(db: Session):
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

    # Delete the created submenu
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200

    # Fetch the deleted submenu and verify it's not found
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 404

def test_delete_submenu_cascading(db: Session):
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

    # Delete the submenu
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200

    # Attempt to fetch the deleted submenu and dish and ensure they're not found
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 404

    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 404


def test_submenu_when_all_dishes_deleted(db: Session):
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

    # Create dishes associated with the submenu
    num_dishes = 3
    dish_ids = []  # Store created dish IDs
    for i in range(num_dishes):
        dish_data = {
            "title": f"Test Dish {i}",
            "description": "My test dish description",
            "price": '9.99',
            "submenu_id": submenu_id

        }
        response = client.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json=dish_data)
        assert response.status_code == 201
        dish_ids.append(response.json()["id"])  # Store the created dish ID

    # Delete all dishes from the submenu
    for dish_id in dish_ids:
        response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
        assert response.status_code == 200

    # Fetch the submenu again
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200

    # Assert that there are no dishes left
    assert response.json()["dishes_count"] == 0


def test_submenu_when_one_of_three_dishes_deleted(db: Session):
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

    # Create dishes associated with the submenu
    num_dishes = 3
    dish_ids = []  # Store created dish IDs
    for i in range(num_dishes):
        dish_data = {
            "title": f"Test Dish {i}",
            "description": "My test dish description",
            "price": '9.99',
            "submenu_id": submenu_id
        }
        response = client.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json=dish_data)
        assert response.status_code == 201
        dish_ids.append(response.json()["id"])  # Store the created dish ID

    dish_id = dish_ids[0]
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200

    # Fetch the submenu again
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200

    # Assert that there are no dishes left
    assert response.json()["dishes_count"] == 2


def test_submenu_when_two_of_three_dishes_deleted(db: Session):
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

    # Create dishes associated with the submenu
    num_dishes = 3
    dish_ids = []  # Store created dish IDs
    for i in range(num_dishes):
        dish_data = {
            "title": f"Test Dish {i}",
            "description": "My test dish description",
            "price": '9.99',
            "submenu_id": submenu_id
        }
        response = client.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json=dish_data)
        assert response.status_code == 201
        dish_ids.append(response.json()["id"])  # Store the created dish ID

    dish_id = dish_ids[0]
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200
    dish_id = dish_ids[1]
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200

    # Fetch the submenu again
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200

    # Assert that there are no dishes left
    assert response.json()["dishes_count"] == 1
