from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum


# -------------------- ENUMS --------------------

class CarStatusEnum(enum.Enum):
    available = "available"
    rented = "rented"
    maintenance = "maintenance"


class RentalStatusEnum(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    finished = "finished"
    cancelled = "cancelled"


# -------------------- ADMIN --------------------

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    cars = relationship("Car", back_populates="admin")
    rentals = relationship("Rental", back_populates="admin")


# -------------------- RENTER (Customer) --------------------

class Renter(Base):
    __tablename__ = "renters"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    address = Column(String)
    phone = Column(String)
    email = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    cars = relationship("Car", back_populates="renter")
    rentals = relationship("Rental", back_populates="renter")


# -------------------- CAR --------------------

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String, unique=True, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    mileage = Column(Integer)
    status = Column(Enum(CarStatusEnum), nullable=False, default=CarStatusEnum.available)
    rental_price_per_day = Column(Float, nullable=False)

    renter_id = Column(Integer, ForeignKey("renters.id"))
    admin_id = Column(Integer, ForeignKey("admins.id"))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    renter = relationship("Renter", back_populates="cars")
    rentals = relationship("Rental", back_populates="car")
    admin = relationship("Admin", back_populates="cars")


# -------------------- RENTAL --------------------

class Rental(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True, index=True)

    car_id = Column(Integer, ForeignKey("cars.id"))
    renter_id = Column(Integer, ForeignKey("renters.id"))
    admin_id = Column(Integer, ForeignKey("admins.id"))

    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    price_per_day = Column(Float)
    total_price = Column(Float)
    status = Column(Enum(RentalStatusEnum), default=RentalStatusEnum.pending)

    # Relationships
    car = relationship("Car", back_populates="rentals")
    renter = relationship("Renter", back_populates="rentals")
    admin = relationship("Admin", back_populates="rentals")
