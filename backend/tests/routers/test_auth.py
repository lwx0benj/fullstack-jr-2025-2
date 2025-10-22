from http import HTTPStatus


def test_register(client):
    response = client.post(
        '/api/auth/register',
        json={
            'name': 'Alana Raysa',
            'email': 'alana.raysa@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'name': 'Alana Raysa',
        'email': 'alana.raysa@example.com',
    }
