from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from api.models import Car, CarStatusEnum
from api.deps import db_dependency

from pydantic import BaseModel


router = APIRouter(
    prefix="/cars",
    tags=["cars"]
)

# ============================
#       Pydantic Schemas
# ============================

class CarCreate(BaseModel):
    plate_number: str
    brand: str
    model: str
    mileage: int | None = None
    status: CarStatusEnum = CarStatusEnum.available
    rental_price_per_day: float


class CarUpdate(BaseModel):
    plate_number: str | None = None
    brand: str | None = None
    model: str | None = None
    mileage: int | None = None
    status: CarStatusEnum | None = None
    rental_price_per_day: float | None = None


class CarResponse(BaseModel):
    id: int
    plate_number: str
    brand: str
    model: str
    mileage: int | None
    status: CarStatusEnum
    rental_price_per_day: float

    class Config:
        from_attributes = True


# ============================
#        ROUTES CRUD
# ============================

# ---- Create Car ----
@router.post("/", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
def create_car(car: CarCreate, db: db_dependency):
    new_car = Car(
        plate_number=car.plate_number,
        brand=car.brand,
        model=car.model,
        mileage=car.mileage,
        status=car.status,
        rental_price_per_day=car.rental_price_per_day
    )
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car


# ---- Get All Cars ----
@router.get("/", response_model=List[CarResponse])
def get_cars(db: db_dependency):
    cars = db.query(Car).all()
    return cars


# ---- Get Car by ID ----
@router.get("/{car_id}", response_model=CarResponse)
def get_car(car_id: int, db: db_dependency):
    car = db.query(Car).filter(Car.id == car_id).first()

    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    return car


# ---- Update Car ----
@router.put("/{car_id}", response_model=CarResponse)
def update_car(car_id: int, update_data: CarUpdate, db: db_dependency):
    car = db.query(Car).filter(Car.id == car_id).first()

    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    update_dict = update_data.dict(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(car, key, value)

    db.commit()
    db.refresh(car)

    return car


# ---- Delete Car ----
@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_car(car_id: int, db: db_dependency):
    car = db.query(Car).filter(Car.id == car_id).first()

    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    db.delete(car)
    db.commit()

    return {"message": "Car deleted successfully"}
