import random
import string

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# --- Helper for unique usernames ---
def get_random_username():
    return "user_" + "".join(
        random.choices(string.ascii_lowercase + string.digits, k=8)
    )


# =========================
# AUTH TESTS
# =========================


def test_register_user():
    username = get_random_username()

    payload = {"username": username, "password": "testpassword", "role": "patient"}

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["username"] == username
    assert data["role"] == "patient"


def test_register_duplicate_user():
    username = get_random_username()

    payload = {"username": username, "password": "testpassword"}

    # First registration
    client.post("/auth/register", json=payload)

    # Second registration (should fail)
    response = client.post("/auth/register", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"


def test_login_success():
    username = get_random_username()

    payload = {"username": username, "password": "securepass"}

    # Register first
    client.post("/auth/register", json=payload)

    # Login
    response = client.post("/auth/login", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user_id"] is not None


def test_login_wrong_password():
    username = get_random_username()

    # Register
    client.post(
        "/auth/register", json={"username": username, "password": "correctpass"}
    )

    # Try wrong password
    response = client.post(
        "/auth/login", json={"username": username, "password": "wrongpass"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_login_user_not_found():
    username = get_random_username()

    response = client.post(
        "/auth/login", json={"username": username, "password": "doesntmatter"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"
