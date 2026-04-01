from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas, auth
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Auth"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 1. REGISTER ---
@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if username is taken
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hash the password
    hashed_password = auth.hash_password(user.password)

    # Create user (Default role is 'patient')
    new_user = models.User(
        username=user.username, 
        password=hashed_password,
        role=user.role if hasattr(user, 'role') else "patient"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# --- 2. LOGIN (The "Proper" Way) ---
@router.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. Find the user
    db_user = db.query(models.User).filter(models.User.username == user.username).first()

    # 2. Verify password
    if not db_user or not auth.verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password"
        )

    # 3. Create a JWT Access Token (The ID Badge)
    access_token = auth.create_access_token(data={"sub": db_user.username, "id": db_user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": db_user.id,
        "role": db_user.role
    }