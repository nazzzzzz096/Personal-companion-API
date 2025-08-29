from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app import database, schemas, utils
from app.auth_utils import get_current_user
from app.models import User as UserModel
from app.logger import logger
from typing import List
from app.rate_limit import limiter

router = APIRouter(prefix="/users", tags=["Users"])




# ---------------- Get Current User ----------------
@router.get("/me", response_model=schemas.UserOut)
@limiter.limit("5/minute")
def read_me(request:Request,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(database.get_db),
):
    logger.info(f'accessing current user info{current_user}')
    return current_user


@router.get("/", response_model=List[schemas.UserOut])
@limiter.limit("5/minute")
def list_users(request:Request,db: Session = Depends(database.get_db)):
    logger.info(f'acceesing the information about the users')
    return db.query(UserModel).all()
