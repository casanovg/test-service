"""
Test API endpoints
"""
import pytest


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "version" in data
    assert "status" in data
    assert data["status"] == "running"


def test_api_root(client):
    """Test API root endpoint"""
    response = client.get("/api/v1/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_test_endpoint(client):
    """Test the /api/v1/test endpoint"""
    response = client.get("/api/v1/test")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "message" in data
    assert "service" in data


def test_echo_endpoint(client):
    """Test the /api/v1/echo endpoint"""
    test_data = {
        "message": "Hello, World!",
        "number": 42,
        "array": [1, 2, 3]
    }
    response = client.post("/api/v1/echo", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert "echo" in data
    assert data["echo"] == test_data
    assert "message" in data


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "service" in data
    assert "version" in data
    assert "database" in data


def test_get_examples(client):
    """Test getting list of examples"""
    response = client.get("/api/v1/examples")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_create_and_get_example(client):
    """Test creating and retrieving an example"""
    # Create example
    new_example = {
        "name": "Test Example",
        "description": "This is a test",
        "value": 123
    }
    create_response = client.post("/api/v1/examples", json=new_example)
    assert create_response.status_code == 201
    created_data = create_response.json()
    assert "id" in created_data
    example_id = created_data["id"]
    
    # Get example by ID
    get_response = client.get(f"/api/v1/examples/{example_id}")
    assert get_response.status_code == 200
    get_data = get_response.json()
    assert get_data["name"] == new_example["name"]
    assert get_data["description"] == new_example["description"]
    assert get_data["value"] == new_example["value"]


def test_update_example(client):
    """Test updating an example"""
    # Create example first
    new_example = {
        "name": "Original Name",
        "description": "Original Description",
        "value": 100
    }
    create_response = client.post("/api/v1/examples", json=new_example)
    example_id = create_response.json()["id"]
    
    # Update example
    update_data = {
        "name": "Updated Name",
        "value": 200
    }
    update_response = client.put(f"/api/v1/examples/{example_id}", json=update_data)
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["name"] == update_data["name"]
    assert updated_data["value"] == update_data["value"]
    assert updated_data["description"] == new_example["description"]


def test_delete_example(client):
    """Test deleting an example"""
    # Create example first
    new_example = {
        "name": "To Be Deleted",
        "description": "This will be deleted",
        "value": 999
    }
    create_response = client.post("/api/v1/examples", json=new_example)
    example_id = create_response.json()["id"]
    
    # Delete example
    delete_response = client.delete(f"/api/v1/examples/{example_id}")
    assert delete_response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/examples/{example_id}")
    assert get_response.status_code == 404


def test_get_nonexistent_example(client):
    """Test getting an example that doesn't exist"""
    response = client.get("/api/v1/examples/99999")
    assert response.status_code == 404


def test_update_nonexistent_example(client):
    """Test updating an example that doesn't exist"""
    update_data = {"name": "Test"}
    response = client.put("/api/v1/examples/99999", json=update_data)
    assert response.status_code == 404


def test_delete_nonexistent_example(client):
    """Test deleting an example that doesn't exist"""
    response = client.delete("/api/v1/examples/99999")
    assert response.status_code == 404
