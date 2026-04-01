from fastapi import FastAPI
from app.database import Base, engine
import app.models

# 1. Import all your routers here
from .routers import auth_routes, doctor_routes, appointment_routes

app = FastAPI(title="Doctor Appointment System")

# 2. This line tells SQLAlchemy to look at models.py and create
# any missing tables (like Appointments and DoctorSchedules)
Base.metadata.create_all(bind=engine)

# 3. Connect the Routers to the App
app.include_router(auth_routes.router)
app.include_router(doctor_routes.router)
app.include_router(appointment_routes.router)  # This connects your booking logic!


@app.get("/")
def home():
    return {"message": "API is running successfully"}


if __name__ == "__main__":
    from uvicorn import run

    run(app=app, host="0.0.0.0", port=8000)
