from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

# -------------------
# USER SCHEMAS
# -------------------
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: Optional[datetime] = None  # if you add this in model

    # Pydantic v2: enable ORM objects -> Pydantic
    model_config = ConfigDict(from_attributes=True)

# Returned by /auth/login
class Token(BaseModel):
    access_token: str
    token_type: str

# Internal use when decoding JWT
class TokenData(BaseModel):
    email: Optional[EmailStr] = None


# -------------------
# TASK SCHEMAS
# -------------------
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskOut(TaskBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

#weather schema
class WeatherOut(BaseModel):
    city: str
    temperature: float
    description: str