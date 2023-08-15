from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.models.database import get_db
from app.models import schemas
import pytest
from app.models.database import engine
from app.models.core import Base
from app.models.core import Base, Menu 
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

def test_get_menus_empty(db: Session):
    response = client.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json() == []

def test_create_menu(db: Session):
    # Prepare payload for creating a menu
    menu_create_payload = {
        "title": "New Menu",
        "description": "A new menu"
    }
    
    # Send a POST request to create a menu
    response = client.post("/api/v1/menus/", json=menu_create_payload)
    
    # Verify the response status code and JSON data
    assert response.status_code == 201
    created_menu = response.json()
    assert created_menu["title"] == menu_create_payload["title"]
    assert created_menu["description"] == menu_create_payload["description"]
    assert created_menu["submenus_count"] == 0
    assert created_menu["dishes_count"] == 0

def test_get_menu_by_id(db: Session):
    # Create a menu in the database
    menu_create_payload = {
        "title": "Test Menu",
        "description": "Test menu description"
    }
    response = client.post("/api/v1/menus/", json=menu_create_payload)
    created_menu = response.json()
    
    # Send a GET request to retrieve the created menu
    response = client.get(f"/api/v1/menus/{created_menu['id']}")
    
    # Verify the response status code and JSON data
    assert response.status_code == 200
    retrieved_menu = response.json()
    assert retrieved_menu["id"] == created_menu["id"]
    assert retrieved_menu["title"] == created_menu["title"]
    assert retrieved_menu["description"] == created_menu["description"]
    assert retrieved_menu["submenus_count"] == created_menu["submenus_count"]
    assert retrieved_menu["dishes_count"] == created_menu["dishes_count"]


def test_delete_menu_not_found(db: Session):
    # Generate a random UUID that is not present in the database
    non_existent_menu_id = uuid4()

    # Send a DELETE request to delete the non-existent menu
    response = client.delete(f"/api/v1/menus/{non_existent_menu_id}")

    # Verify the response status code and the detail message
    assert response.status_code == 404
    assert response.json()["detail"] == "menu not found"

def test_delete_menu_found(db: Session):
    # Create a new menu for testing
    menu_create_payload = {
        "title": "Test Menu",
        "description": "Test menu description"
    }
    response = client.post("/api/v1/menus/", json=menu_create_payload)

    # Verify that the menu was created successfully
    assert response.status_code == 201
    menu_id = response.json()["id"]

    # Send a DELETE request to delete the created menu
    delete_response = client.delete(f"/api/v1/menus/{menu_id}")

    # Verify the response status code and the response message
    assert delete_response.status_code == 200
    assert delete_response.json() == {"status": True, "message": "The menu has been deleted"}

    # Verify that the menu is no longer present in the database
    get_response = client.get(f"/api/v1/menus/{menu_id}")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "menu not found"

def test_update_menu_found(db: Session):
    # Create a menu first
    menu_create_payload = {
        "title": "Test Menu",
        "description": "Test menu description"
    }
    
    create_response = client.post("/api/v1/menus/", json=menu_create_payload)
    assert create_response.status_code == 201
    created_menu_id = create_response.json()["id"]
    
    # Update the menu
    updated_menu_data = {
        "title": "Updated Menu Title",
        "description": "Updated menu description"
    }
    
    update_response = client.patch(f"/api/v1/menus/{created_menu_id}", json=updated_menu_data)
    assert update_response.status_code == 200
    assert update_response.json()["title"] == updated_menu_data["title"]
    assert update_response.json()["description"] == updated_menu_data["description"]

def test_update_menu_not_found(db: Session):
    # Menu ID that does not exist
    non_existent_menu_id = uuid4()
    
    updated_menu_data = {
        "title": "Updated Menu Title",
        "description": "Updated menu description"
    }
    
    update_response = client.patch(f"/api/v1/menus/{non_existent_menu_id}", json=updated_menu_data)
    assert update_response.status_code == 404


def test_menu_when_all_submenus_deleted(db: Session):
    # Create a menu
    menu_data = {
        "title": "Test Menu",
        "description": "Test menu description"
    }
    response = client.post("/api/v1/menus", json=menu_data)
    assert response.status_code == 201
    menu_id = response.json()["id"]

    # Create submenus
    num_submenus = 3
    submenu_ids = []  # Store created submenu IDs
    for i in range(num_submenus):
        submenu_data = {
            "title": f"Test Submenu {i}",
            "description": "My test submenu description"
        }
        response = client.post(f"/api/v1/menus/{menu_id}/submenus", json=submenu_data)
        assert response.status_code == 201
        submenu_ids.append(response.json()["id"])  # Store the created submenu ID

    # Delete all submenus
    for submenu_id in submenu_ids:
        response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
        assert response.status_code == 200

    # Fetch the menu again
    response = client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200

    # Assert that there are no submenus left
    assert response.json()["submenus_count"] == 0
    assert response.json()["dishes_count"] == 0

