#Libraries Import
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate

def get_users(db: Session, skip=0, limit=10):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user_data: UserCreate):
    new_user = User(name=user_data.name, email=user_data.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user