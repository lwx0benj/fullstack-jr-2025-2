from fastapi.testclient import TestClient

from backend.app import app

client = TestClient(app)


def test_hello_world():
    OK = 200
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == OK
    assert response.json() == {'message': 'Hello, World!'}
