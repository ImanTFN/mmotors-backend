import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_success():
    response = client.post("/auth/register", json={
        "nom": "Test",
        "prenom": "User",
        "email": "testunit_new@test.com",
        "password": "Test2024!"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "testunit_new@test.com"

def test_register_duplicate_email():
    client.post("/auth/register", json={
        "nom": "Test",
        "prenom": "User",
        "email": "duplicate_new@test.com",
        "password": "Test2024!"
    })
    response = client.post("/auth/register", json={
        "nom": "Test",
        "prenom": "User",
        "email": "duplicate_new@test.com",
        "password": "Test2024!"
    })
    assert response.status_code == 400

def test_login_success():
    client.post("/auth/register", json={
        "nom": "Login",
        "prenom": "Test",
        "email": "login@test.com",
        "password": "Test2024!"
    })
    response = client.post("/auth/login", json={
        "email": "login@test.com",
        "password": "Test2024!"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password():
    response = client.post("/auth/login", json={
        "email": "login@test.com",
        "password": "WrongPassword!"
    })
    assert response.status_code == 401

def test_login_wrong_email():
    response = client.post("/auth/login", json={
        "email": "notexist@test.com",
        "password": "Test2024!"
    })
    assert response.status_code == 401

def test_get_me_without_token():
    response = client.get("/auth/me")
    assert response.status_code == 401

def test_get_me_with_token():
    client.post("/auth/register", json={
        "nom": "Me",
        "prenom": "Test",
        "email": "me@test.com",
        "password": "Test2024!"
    })
    login_res = client.post("/auth/login", json={
        "email": "me@test.com",
        "password": "Test2024!"
    })
    token = login_res.json()["access_token"]
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "me@test.com"