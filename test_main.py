from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_lead():
    response = client.post(
        "/leads/",
        json={
            "name": "Juan",
            "surname": "Martinez",
            "address": "135 Oky St",
            "email": "juan@test.com",
            "phone": 1143012943,
            "inscription": "2022-03-01"
        }
    )
    if response.status_code == 400:
        assert response.json() == {'detail': 'Email already registered'}
    elif response.status_code == 200:
        assert response.json() == {
            "name": "Juan",
            "surname": "Martinez",
            "address": "135 Oky St",
            "email": "juan@test.com",
            "phone": 1143012943,
            "inscription": "2022-03-01",
            "id": 2,
            "projection_by_degree": []
        }


def test_read_lead():
    response = client.get("/leads/2")
    assert response.status_code == 200
    assert response.json() == {
        "name": "Juan",
        "surname": "Martinez",
        "address": "135 Oky St",
        "email": "juan@test.com",
        "phone": 1143012943,
        "inscription": "2022-03-01",
        'id': 2,
        'projection_by_degree': []
    }


def test_read_lead_not_found():
    response = client.get("/leads/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Lead not found"}
