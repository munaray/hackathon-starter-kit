from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import User, APIKey
from ..schemas import UserCreate, UserOut, Token, APIKeyCreate, APIKeyOut
from .utils import hash_password, verify_password, create_access_token, generate_api_key
from .deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=user_in.email, hashed_password=hash_password(user_in.password), role="user")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token(user.email)
    return Token(access_token=token)


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/api-keys", response_model=APIKeyOut)
def create_api_key(
    payload: APIKeyCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    key = APIKey(name=payload.name, key=generate_api_key(), user_id=current_user.id)
    db.add(key)
    db.commit()
    db.refresh(key)
    return key