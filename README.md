# 🏥 Hospital Appointment Booking System API

## 📌 Project Overview

This project is a backend system built using **FastAPI** that enables patients to search for doctors, view availability, and book appointments. It simulates a real-world hospital appointment management system with a modular and scalable architecture.

---

## ✅ Implemented Features

## 🔐 Authentication

* User Registration
* User Login

## 👨‍⚕️ Doctor Management (CRUD Operations)

* Create Doctor
* View All Doctors
* Update Doctor
* Delete Doctor

## 🗓️ Doctor Schedule Management

* Manage doctor availability and schedules

## 🔍 Doctor Search

* Search doctors by specialization

## 📅 Appointment Management

* Book Appointments
* Cancel Appointments

## 📜 Patient Features

* View Appointment History


## ⚙️ **Additional Capabilities**

* Input Validation
* Error Handling
* Scalable API Design

---
## 🛠️ Tech Stack

- **Backend:** FastAPI
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Authentication:** Passlib (Password Hashing)
- **Testing:** Pytest
- **API Testing:** Postman
- **Containerization:** Docker

---

## 📁 Project Structure

```
hospital_appointment_api/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   │
│   └── routers/
│       ├── auth_routes.py
│       ├── doctor_routes.py
│       └── appointment_routes.py
│
├── tests/
│   ├── auth_routes.py
│   ├── doctor_routes.py
│   └── appointment_routes.py
│   
├── requirements.txt
├── Dockerfile
├── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/SrinidhiPRao/doctor-appointment-system
cd doctor-appointment-system
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

Activate the environment:

- **Windows:**

```bash
.venv\Scripts\activate
```

- **Mac/Linux:**

```bash
source .venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application

```bash
python -m app.main
```

👉 Open API in your browser:
http://127.0.0.1:8000

---

### 📌 **API Endpoints**

#### 🔐 Authentication

* **POST /auth/register** → Register a new user
* **POST /auth/login** → Login user


#### 👨‍⚕️ Doctors

* **POST /doctors/** → Create doctor
* **GET /doctors/** → Get all doctors
* **PUT /doctors/{id}** → Update doctor
* **DELETE /doctors/{id}** → Delete doctor


#### 🗓️ Doctor Schedule

* **POST /doctors/{doctor_id}/schedule** → Add schedule for a doctor
* **POST /schedules** → Create schedule entry


#### 🔍 Search

* **GET /doctors/search** → Search doctors by specialization


#### 📅 Appointments

* **POST /appointments** → Book appointment
* **DELETE /appointments/{id}** → Cancel appointment
* **GET /appointments/patient/{id}** → Get patient appointment history

---


## 🧪 Testing

- APIs tested using **Postman**
- Automated tests written using **Pytest**
- Test cases available in the `tests/` folder

---

## 🐳 Docker Setup

### Build Docker Image

```bash
docker build -t hospital-api .
```

### Run Docker Container

```bash
docker run -p 8000:8000 hospital-api
```

---

## 📂 Submission Contents

- ✔ Source Code (GitHub Repository)
- ✔ Postman Collection
- ✔ Pytest Test Cases
- ✔ Dockerfile
- ✔ README Documentation

---

## 👥 Team Members

- Raj Kaudinya
- Khushi Sharma
- Srinidhi Rao

---

## 💬 Project Description

This project demonstrates strong backend development skills including:

- RESTful API design
- Database integration
- Authentication systems
- Modular architecture

It follows real-world development practices and is designed for future scalability.

---

