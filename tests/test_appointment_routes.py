from fastapi import Depends
from fastapi.testclient import TestClient
from app.main import app
from app import models
from app.database import get_db
from sqlalchemy.orm import Session
from random import randint

client = TestClient(app)


def seed_doctor_and_schedule(db=next(get_db())):
    d_id = randint(0, 100_000_000)
    doctor = models.Doctor(id=d_id, name="Test Doctor", specialization="Opthalmology")
    db.add(doctor)

    schedule = models.DoctorSchedule(
        doctor_id=d_id,
        day_of_week="Monday",
        start_time="09:00",
        end_time="17:00",
    )
    db.add(schedule)

    db.commit()
    return d_id


def test_book_appointment():
    d_id = seed_doctor_and_schedule()
    payload = {"doctor_id": d_id, "appointment_time": "2026-04-06T10:30:00"}

    response = client.post("/appointments/", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["doctor_id"] == d_id
    assert data["status"] == "booked"


def test_get_patient_history():
    d_id = seed_doctor_and_schedule()

    # Create an appointment first
    payload = {"doctor_id": "d_id", "appointment_time": "2026-04-06T14:43:46.246Z"}
    client.post("/appointments/", json=payload)

    # Fetch patient history
    response = client.get("/appointments/patient/1")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["patient_id"] == 1


def test_delete_appointment():
    d_id = seed_doctor_and_schedule()

    # Create appointment
    payload = {"doctor_id": d_id, "appointment_time": "2026-04-06T10:30:00"}
    create_response = client.post("/appointments/", json=payload)

    assert create_response.status_code == 200
    appointment_id = create_response.json()["id"]

    # Delete appointment
    response = client.delete(f"/appointments/{appointment_id}")

    assert response.status_code == 200
