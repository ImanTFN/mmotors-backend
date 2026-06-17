import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_admin_token():
    client.post("/auth/register", json={
        "nom": "Admin",
        "prenom": "Test",
        "email": "adminvehicle@test.com",
        "password": "Test2024!"
    })
    from app.database import SessionLocal
    from app.models.user import User
    db = SessionLocal()
    user = db.query(User).filter(User.email == "adminvehicle@test.com").first()
    user.is_admin = True
    db.commit()
    db.close()
    res = client.post("/auth/login", json={
        "email": "adminvehicle@test.com",
        "password": "Test2024!"
    })
    return res.json()["access_token"]

def test_get_vehicles_empty():
    response = client.get("/vehicles/?type=achat")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_vehicle_without_auth():
    response = client.post("/vehicles/", json={
        "marque": "Renault",
        "modele": "Clio",
        "annee": 2020,
        "kilometrage": 45000,
        "prix": 12000,
        "motorisation": "Essence",
        "disponible_achat": True,
        "disponible_location": False
    })
    assert response.status_code == 401

def test_create_vehicle_as_admin():
    token = get_admin_token()
    response = client.post("/vehicles/", json={
        "marque": "Peugeot",
        "modele": "308",
        "annee": 2021,
        "kilometrage": 30000,
        "prix": 15000,
        "motorisation": "Diesel",
        "disponible_achat": True,
        "disponible_location": False
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert response.json()["marque"] == "Peugeot"

def test_get_vehicle_by_id():
    token = get_admin_token()
    create_res = client.post("/vehicles/", json={
        "marque": "Toyota",
        "modele": "Yaris",
        "annee": 2019,
        "kilometrage": 60000,
        "prix": 10000,
        "motorisation": "Hybride",
        "disponible_achat": True,
        "disponible_location": False
    }, headers={"Authorization": f"Bearer {token}"})
    vehicle_id = create_res.json()["id"]
    response = client.get(f"/vehicles/{vehicle_id}")
    assert response.status_code == 200
    assert response.json()["modele"] == "Yaris"

def test_get_vehicle_not_found():
    response = client.get("/vehicles/99999")
    assert response.status_code == 404

def test_basculer_vehicle():
    token = get_admin_token()
    create_res = client.post("/vehicles/", json={
        "marque": "BMW",
        "modele": "Serie 3",
        "annee": 2022,
        "kilometrage": 20000,
        "prix": 25000,
        "motorisation": "Essence",
        "disponible_achat": True,
        "disponible_location": False
    }, headers={"Authorization": f"Bearer {token}"})
    vehicle_id = create_res.json()["id"]
    response = client.patch(f"/vehicles/{vehicle_id}/basculer", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["disponible_achat"] == False
    assert response.json()["disponible_location"] == True