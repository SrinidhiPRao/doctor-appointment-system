# 🏥 Hospital Appointment Booking System API

## 📌 Project Overview

This project is a backend system built using **FastAPI** that enables patients to search for doctors, view availability, and book appointments. It simulates a real-world hospital appointment management system with a modular and scalable architecture.

---

## 🚀 Features

### 🔐 Authentication

- User Registration
- User Login

### 👨‍⚕️ Doctor Management

- Create Doctor
- View All Doctors
- Update Doctor
- Delete Doctor

### 📅 Upcoming Features

- Doctor Schedule Management
- Search Doctors by Specialization
- Appointment Booking & Cancellation
- Patient Appointment History

### ✅ Additional Capabilities

- Input Validation
- Error Handling
- Scalable API Design

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
│
├── tests/
├── requirements.txt
├── Dockerfile
├── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-link>
cd hospital_appointment_api
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

- **Windows:**

```bash
venv\Scripts\activate
```

- **Mac/Linux:**

```bash
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application

```bash
uvicorn app.main:app --reload
```

👉 Open API Docs in your browser:
http://127.0.0.1:8000/docs

---

## 📌 API Endpoints

### 🔐 Authentication

- `POST /auth/register` → Register a new user
- `POST /auth/login` → Login user

### 👨‍⚕️ Doctors

- `POST /doctors/` → Create doctor
- `GET /doctors/` → Get all doctors
- `PUT /doctors/{id}` → Update doctor
- `DELETE /doctors/{id}` → Delete doctor

---

## 🧪 Testing

- APIs tested using **Postman**
- Automated tests written using **Pytest**
- Test cases available in the `tests/` folder

---

## 🐳 Docker Setup (Optional)

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
- ✔ SQLite Database (`test.db`)
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

## 📌 Future Enhancements

- Implement JWT Authentication
- Add Role-Based Access Control
- Pagination & Filtering
- Migrate to PostgreSQL
- Cloud Deployment (AWS / Azure)

---

## ✅ Current Status

- ✔ Core Backend Completed (Authentication + Doctor Management)
- ⏳ Remaining Modules Under Development

---

## 📞 Notes

- Ensure all dependencies are installed before running the project
- Refer to API documentation at `/docs` for endpoint testing

---
