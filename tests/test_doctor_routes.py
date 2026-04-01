import random
from fastapi.testclient import TestClient
from app.main import app
from app import models
from app.database import get_db

client = TestClient(app)


client = TestClient(app)


# --- Helper ---
def get_random_id():
    return random.randint(1000, 999999)


def seed_doctor(db, doctor_id):
    doctor = models.Doctor(
        id=doctor_id, name=f"Doctor_{doctor_id}", specialization="Cardiology"
    )
    db.add(doctor)
    db.commit()
    return doctor


# =========================
# DOCTOR TESTS
# =========================


def test_create_doctor():
    payload = {"name": "Dr. No", "specialization": "Neurology"}

    response = client.post("/doctors/", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "Dr. No"
    assert data["specialization"] == "Neurology"


def test_set_doctor_schedule():
    db = next(get_db())
    doctor_id = get_random_id()
    seed_doctor(db, doctor_id)

    payload = {"day_of_week": "Monday", "start_time": "09:00", "end_time": "17:00"}

    response = client.post(f"/doctors/{doctor_id}/schedule", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["doctor_id"] == doctor_id
    assert data["day_of_week"] == "Monday"


def test_set_schedule_doctor_not_found():
    doctor_id = get_random_id()

    payload = {"day_of_week": "Monday", "start_time": "09:00", "end_time": "17:00"}

    response = client.post(f"/doctors/{doctor_id}/schedule", json=payload)

    assert response.status_code == 404


def test_search_doctors():
    db = next(get_db())

    db.add(models.Doctor(name="A", specialization="Cardiology"))
    db.add(models.Doctor(name="B", specialization="Cardiologist"))
    db.commit()

    response = client.get("/doctors/search?specialization=cardio")

    assert response.status_code == 200
    data = response.json()

    assert len(data) >= 1


def test_search_no_results():
    response = client.get("/doctors/search?specialization=unknown_xyz")

    assert response.status_code == 404


def test_list_all_doctors():
    db = next(get_db())
    doctor_id = get_random_id()
    seed_doctor(db, doctor_id)

    response = client.get("/doctors")

    assert response.status_code == 200
    print(response)
    # data = response.json()

    # assert isinstance(data, list)
    # assert len(data) >= 1


def test_update_doctor():
    db = next(get_db())
    doctor_id = get_random_id()
    seed_doctor(db, doctor_id)

    payload = {"name": "Updated Name", "specialization": "Dermatology"}

    response = client.put(f"/doctors/{doctor_id}", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "Updated Name"
    assert data["specialization"] == "Dermatology"


def test_update_doctor_not_found():
    doctor_id = get_random_id()

    payload = {"name": "X", "specialization": "Y"}

    response = client.put(f"/doctors/{doctor_id}", json=payload)

    assert response.status_code == 404


def test_delete_doctor():
    db = next(get_db())
    doctor_id = get_random_id()
    seed_doctor(db, doctor_id)

    response = client.delete(f"/doctors/{doctor_id}")

    assert response.status_code == 200
    assert "removed" in response.json()["message"]


def test_delete_doctor_not_found():
    doctor_id = get_random_id()

    response = client.delete(f"/doctors/{doctor_id}")

    assert response.status_code == 404


# =========================
# APPOINTMENT TESTS
# =========================


def seed_schedule(db, doctor_id):
    schedule = models.DoctorSchedule(
        doctor_id=doctor_id,
        day_of_week="Monday",
        start_time="09:00",
        end_time="17:00",
    )
    db.add(schedule)
    db.commit()


def test_book_appointment():
    db = next(get_db())
    doctor_id = get_random_id()

    seed_doctor(db, doctor_id)
    seed_schedule(db, doctor_id)

    payload = {"doctor_id": doctor_id, "appointment_time": "2026-04-06T10:30:00"}

    response = client.post("/appointments/", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["doctor_id"] == doctor_id
    assert data["status"] == "booked"


def test_delete_appointment():
    db = next(get_db())
    doctor_id = get_random_id()

    seed_doctor(db, doctor_id)
    seed_schedule(db, doctor_id)

    payload = {"doctor_id": doctor_id, "appointment_time": "2026-04-06T10:30:00"}

    create_response = client.post("/appointments/", json=payload)
    appointment_id = create_response.json()["id"]

    response = client.delete(f"/appointments/{appointment_id}")

    assert response.status_code == 200
