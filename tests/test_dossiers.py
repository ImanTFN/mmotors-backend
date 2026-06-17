from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_user_token():
    client.post("/auth/register", json={
        "nom": "Dossier",
        "prenom": "User",
        "email": "dossieruser@test.com",
        "password": "Test2024!"
    })
    res = client.post("/auth/login", json={
        "email": "dossieruser@test.com",
        "password": "Test2024!"
    })
    return res.json()["access_token"]

def get_admin_token():
    client.post("/auth/register", json={
        "nom": "Dossier",
        "prenom": "Admin",
        "email": "dossieradmin@test.com",
        "password": "Test2024!"
    })
    from app.database import SessionLocal
    from app.models.user import User
    db = SessionLocal()
    user = db.query(User).filter(User.email == "dossieradmin@test.com").first()
    user.is_admin = True
    db.commit()
    db.close()
    res = client.post("/auth/login", json={
        "email": "dossieradmin@test.com",
        "password": "Test2024!"
    })
    return res.json()["access_token"]

def create_test_vehicle():
    token = get_admin_token()
    res = client.post("/vehicles/", json={
        "marque": "Test",
        "modele": "Car",
        "annee": 2020,
        "kilometrage": 10000,
        "prix": 8000,
        "motorisation": "Essence",
        "disponible_achat": True,
        "disponible_location": True,
        "prix_location_mois": 300
    }, headers={"Authorization": f"Bearer {token}"})
    return res.json()["id"]

def test_create_dossier_without_auth():
    response = client.post("/dossiers/", json={
        "vehicle_id": 1,
        "type_dossier": "achat"
    })
    assert response.status_code == 401

def test_create_dossier_as_user():
    token = get_user_token()
    vehicle_id = create_test_vehicle()
    response = client.post("/dossiers/", json={
        "vehicle_id": vehicle_id,
        "type_dossier": "achat"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert response.json()["type_dossier"] == "achat"

def test_get_mes_dossiers():
    token = get_user_token()
    response = client.get("/dossiers/mes-dossiers", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_all_dossiers_as_admin():
    token = get_admin_token()
    response = client.get("/dossiers/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_get_all_dossiers_as_user():
    token = get_user_token()
    response = client.get("/dossiers/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

def test_update_dossier_statut():
    admin_token = get_admin_token()
    user_token = get_user_token()
    vehicle_id = create_test_vehicle()
    dossier_res = client.post("/dossiers/", json={
        "vehicle_id": vehicle_id,
        "type_dossier": "location"
    }, headers={"Authorization": f"Bearer {user_token}"})
    dossier_id = dossier_res.json()["id"]
    response = client.patch(f"/dossiers/{dossier_id}", json={
        "statut": "valide",
        "commentaire": "Dossier complet"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["statut"] == "valide"