from pydantic import BaseModel, EmailStr
from typing import Any, Optional, List
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class APIKeyCreate(BaseModel):
    name: str


class APIKeyOut(BaseModel):
    id: int
    name: str
    key: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class EventIn(BaseModel):
    type: str
    payload: Any


class EventOut(BaseModel):
    id: int
    type: str
    payload: Any
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationCreate(BaseModel):
    user_id: Optional[int]
    title: str
    message: str


class NotificationOut(BaseModel):
    id: int
    user_id: Optional[int]
    title: str
    message: str
    read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class SentimentRequest(BaseModel):
    text: str


class SentimentResponse(BaseModel):
    label: str
    score: float


class AnomalyRequest(BaseModel):
    values: List[float]


class AnomalyResponse(BaseModel):
    is_anomaly: List[bool]
    scores: List[float]


class ScoreRequest(BaseModel):
    features: dict


class ScoreResponse(BaseModel):
    score: float