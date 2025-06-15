from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from enum import Enum

class Units(str, Enum):
    standard = "standard"
    metric = "metric"
    imperial = "imperial"

class WeatherReportParams(BaseModel):
    lat: Annotated[float, Field(ge=-90, le=90)]
    lon: Annotated[float, Field(ge=-180, le=180)]
    appid: str
    units: Units
    exclude: Optional[str] = None

class WeatherDescription(BaseModel):
    id: int
    main: str
    description: str

class WeatherCurrent(BaseModel):
    sunrise: int
    sunset: int
    temp: float
    feels_like: float
    humidity: float
    weather: List[WeatherDescription]

class WeatherForecastDailyTemp(BaseModel):
    morn: float
    day: float
    eve: float
    night: float

class WeatherForecastDaily(BaseModel):
    dt: int
    summary: str
    temp: WeatherForecastDailyTemp

class WeatherReport(BaseModel):
    lat: float
    lon: float
    timezone: str
    current: WeatherCurrent
    daily: List[WeatherForecastDaily]


