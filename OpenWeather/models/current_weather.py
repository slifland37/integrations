from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from enum import Enum

class Units(str, Enum):
    metric = "m"
    scientific = "s"
    fahrenheit = "f"

class WeatherstackRequest(BaseModel):
    type: str
    query: str
    language: str
    unit: str

class WeatherstackLocation(BaseModel):
    name: str
    country: str
    region: str
    lat: str
    lon: str
    timezone_id: str
    localtime: str
    localtime_epoch: int
    utc_offset: str

class WeatherstackAstro(BaseModel):
    sunrise: str
    sunset: str
    moonrise: str
    moonset: str
    moon_phase: str
    moon_illumination: int

class WeatherstackAirQuality(BaseModel):
    co: str
    no2: str
    o3: str
    so2: str
    pm2_5: str
    pm10: str
    us_epa_index: str = Field(alias="us-epa-index")
    gb_defra_index: str = Field(alias="gb-defra-index")

class WeatherstackCurrent(BaseModel):
    observation_time: str
    temperature: int
    weather_code: int
    weather_icons: List[str]
    weather_descriptions: List[str]
    wind_speed: int
    wind_degree: int
    wind_dir: str
    pressure: int
    precip: float
    humidity: int
    cloudcover: int
    feelslike: int
    uv_index: int
    visibility: int
    astro: Optional[WeatherstackAstro] = None
    air_quality: Optional[WeatherstackAirQuality] = None

class WeatherstackResponse(BaseModel):
    request: WeatherstackRequest
    location: WeatherstackLocation
    current: WeatherstackCurrent

class WeatherstackError(BaseModel):
    code: int
    type: str
    info: str

class WeatherstackErrorResponse(BaseModel):
    success: bool = False
    error: WeatherstackError


