from fastapi import APIRouter,Request
import httpx
from pydantic import BaseModel
from app.rate_limit import limiter

router = APIRouter(prefix="/weather", tags=["Weather"])

class WeatherOut(BaseModel):
    city: str
    temperature: float
    description: str

@router.get("/{city}", response_model=WeatherOut)
@limiter.limit("5/minute")
async def get_weather(request:Request,city: str):
    """getting weather of the city"""
    api_key = "apikeyyy###"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        data = resp.json()

    return {
        "city": city,
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"]
    }

