from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="patient")

    appointments = relationship("Appointment", back_populates="patient")


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    specialization = Column(String, index=True)

    # Relationships
    appointments = relationship("Appointment", back_populates="doctor")
    schedules = relationship("DoctorSchedule", back_populates="doctor")


class DoctorSchedule(Base):
    __tablename__ = "doctor_schedules"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    day_of_week = Column(String)  # "Monday", "Tuesday", etc.
    start_time = Column(String)  # "09:00"
    end_time = Column(String)  # "17:00"

    doctor = relationship("Doctor", back_populates="schedules")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    patient_id = Column(Integer, ForeignKey("users.id"))
    appointment_time = Column(DateTime, index=True)
    status = Column(String, default="booked")

    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("User", back_populates="appointments")
