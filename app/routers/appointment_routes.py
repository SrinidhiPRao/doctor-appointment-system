from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas
from datetime import datetime
from typing import List

router = APIRouter(prefix="/appointments", tags=["Appointments"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.AppointmentResponse)
def book_appointment(req: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    # --- 1. Basic Existence Check ---
    doctor = db.query(models.Doctor).filter(models.Doctor.id == req.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # --- 2. Schedule Logic (Is the doctor working?) ---
    requested_day = req.appointment_time.strftime("%A")  # Converts date to "Monday"
    requested_time = req.appointment_time.strftime("%H:%M")  # Converts time to "10:30"

    # Search for the doctor's schedule for that specific day
    schedule = (
        db.query(models.DoctorSchedule)
        .filter(
            models.DoctorSchedule.doctor_id == req.doctor_id,
            models.DoctorSchedule.day_of_week == requested_day,
        )
        .first()
    )

    if not schedule:
        raise HTTPException(
            status_code=400, detail=f"Doctor does not work on {requested_day}s"
        )

    # Check if the time falls within start and end hours
    if not (schedule.start_time <= requested_time <= schedule.end_time):
        raise HTTPException(
            status_code=400,
            detail=f"Doctor is only available between {schedule.start_time} and {schedule.end_time}",
        )

    # --- 3. Double Booking Logic (Is the slot free?) ---
    existing_appointment = (
        db.query(models.Appointment)
        .filter(
            models.Appointment.doctor_id == req.doctor_id,
            models.Appointment.appointment_time == req.appointment_time,
            models.Appointment.status == "booked",
        )
        .first()
    )

    if existing_appointment:
        raise HTTPException(status_code=400, detail="This time slot is already booked")

    # --- 5. Final Action: Save to Database ---
    new_appointment = models.Appointment(
        doctor_id=req.doctor_id,
        patient_id=1,  # Temporary: We will link this to the logged-in user later
        appointment_time=req.appointment_time,
        status="booked",
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment


# --- 6. GET PATIENT APPOINTMENT HISTORY ---
@router.get("/patient/{patient_id}", response_model=List[schemas.AppointmentResponse])
def get_patient_history(patient_id: int, db: Session = Depends(get_db)):
    # This looks into the database and finds every row where the patient_id matches
    history = (
        db.query(models.Appointment)
        .filter(models.Appointment.patient_id == patient_id)
        .all()
    )

    if not history:
        raise HTTPException(
            status_code=404, detail="No appointment history found for this patient"
        )

    return history


# --- 7. DELETE APPOINTMENT (Hard Delete) ---
@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    # 1. Find the appointment
    appt = (
        db.query(models.Appointment)
        .filter(models.Appointment.id == appointment_id)
        .first()
    )

    # 2. If it doesn't exist, tell the user
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    # 3. Physically remove it from the database
    db.delete(appt)
    db.commit()

    return {"message": f"Appointment {appointment_id} has been permanently deleted"}
