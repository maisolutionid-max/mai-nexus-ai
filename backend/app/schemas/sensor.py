from pydantic import BaseModel


class SensorCreate(BaseModel):
    sensor_name: str
    sensor_type: str
    location: str
    value: float
    unit: str


class SensorUpdate(BaseModel):
    value: float | None = None
    status: str | None = None


class SensorResponse(BaseModel):
    id: int
    sensor_name: str
    sensor_type: str
    location: str
    value: float
    unit: str
    status: str

    class Config:
        from_attributes = True
