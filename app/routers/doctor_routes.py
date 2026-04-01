from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas
from typing import List

router = APIRouter(prefix="/doctors", tags=["Doctors"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 1. ADD NEW DOCTOR ---
@router.post("/", response_model=schemas.DoctorResponse)
def create_doctor(doc: schemas.DoctorCreate, db: Session = Depends(get_db)):
    new_doc = models.Doctor(name=doc.name, specialization=doc.specialization)
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc

# --- 2. SET DOCTOR SCHEDULE (The "24/7 Fix") ---
@router.post("/{doctor_id}/schedule", response_model=schemas.ScheduleResponse)
def set_doctor_schedule(doctor_id: int, schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    # Guard: Ensure doctor exists before setting a schedule
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
        
    new_schedule = models.DoctorSchedule(
        doctor_id=doctor_id,
        day_of_week=schedule.day_of_week,
        start_time=schedule.start_time,
        end_time=schedule.end_time
    )
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return new_schedule

# --- 3. SEARCH DOCTORS BY SPECIALIZATION ---
@router.get("/search", response_model=List[schemas.DoctorResponse])
def search_doctors(specialization: str, db: Session = Depends(get_db)):
    # .ilike makes it case-insensitive (e.g., 'dentist' matches 'Dentist')
    doctors = db.query(models.Doctor).filter(
        models.Doctor.specialization.ilike(f"%{specialization}%")
    ).all()
    
    if not doctors:
        raise HTTPException(status_code=404, detail="No doctors found with this specialization")
    return doctors

# --- 4. GET ALL DOCTORS ---
@router.get("/", response_model=List[schemas.DoctorResponse])
def list_all_doctors(db: Session = Depends(get_db)):
    return db.query(models.Doctor).all()

# --- 5. UPDATE DOCTOR ---
@router.put("/{doctor_id}", response_model=schemas.DoctorResponse)
def update_doctor(doctor_id: int, doc_update: schemas.DoctorCreate, db: Session = Depends(get_db)):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    db_doctor.name = doc_update.name
    db_doctor.specialization = doc_update.specialization
    
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

# --- 6. DELETE DOCTOR ---
@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    db.delete(db_doctor)
    db.commit()
    return {"message": f"Doctor {doctor_id} has been removed from the system"}