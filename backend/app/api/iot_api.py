from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from schemas.sensor import (
    SensorCreate,
    SensorUpdate,
    SensorResponse
)

from services.iot_service import (
    get_sensors,
    get_sensor,
    create_sensor,
    update_sensor,
    delete_sensor
)

router = APIRouter(
    prefix="/iot",
    tags=["IoT"]
)


@router.get("/", response_model=list[SensorResponse])
def read_sensors(
    db: Session = Depends(get_db)
):
    return get_sensors(db)


@router.get("/{sensor_id}", response_model=SensorResponse)
def read_sensor(
    sensor_id: int,
    db: Session = Depends(get_db)
):
    sensor = get_sensor(db, sensor_id)

    if not sensor:
        raise HTTPException(
            status_code=404,
            detail="Sensor not found"
        )

    return sensor


@router.post("/", response_model=SensorResponse)
def create(
    sensor: SensorCreate,
    db: Session = Depends(get_db)
):
    return create_sensor(db, sensor)


@router.put("/{sensor_id}", response_model=SensorResponse)
def update(
    sensor_id: int,
    sensor: SensorUpdate,
    db: Session = Depends(get_db)
):
    result = update_sensor(
        db,
        sensor_id,
        sensor
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Sensor not found"
        )

    return result


@router.delete("/{sensor_id}")
def delete(
    sensor_id: int,
    db: Session = Depends(get_db)
):
    result = delete_sensor(
        db,
        sensor_id
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Sensor not found"
        )

    return {
        "message": "Sensor deleted successfully"
      }
