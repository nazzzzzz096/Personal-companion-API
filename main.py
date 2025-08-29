
from fastapi import FastAPI

from app.routes.v1 import auth, users, weather,reports
from app.routes.v1 import tasks
from . import models, database
from app.rate_limit import limiter, rate_limit_handler, RateLimitExceeded


# Create tables in RDS
models.Base.metadata.create_all(bind=database.engine)



app = FastAPI(title="Personal Companion API",version="1.0.0")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)


# Include auth routes
app.include_router(auth.router,prefix="/v1")
app.include_router(users.router,prefix="/v1")
app.include_router(tasks.router,prefix="/v1")
app.include_router(weather.router,prefix="/v1")
app.include_router(reports.router,prefix="/v")
@app.get("/")
def root():
    return {"message": "Welcome to Personal Companion API 🚀"}


