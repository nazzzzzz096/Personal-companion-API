from fastapi import APIRouter, Depends,Request
from sqlalchemy.orm import Session
from app import database, models
from app.mail_utils import send_report_email
from app.auth_utils import get_current_user
from app.logger import logger
from app.rate_limit import limiter

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.post("/daily")
@limiter.limit("5/minute")
async def send_daily_report(request:Request,db: Session = Depends(database.get_db),
                            current_user: models.User = Depends(get_current_user)):
    tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()
    
    task_list = "".join([f"<li>{t.title} - {' Done' if t.completed else ' Pending'}</li>" for t in tasks])
    
    body = f"""
    <h3>Hello {current_user.username}, here is your daily task report:</h3>
    <ul>{task_list}</ul>
    """
    
    await send_report_email(
        subject="Your Daily Task Report",
        recipients=[current_user.email],
        body=body
    )
    logger.info(f'report send succcessfully to {current_user.email}')
    return {"message": f"Daily report sent to {current_user.email}"}
