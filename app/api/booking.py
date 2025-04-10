from uuid import UUID
from fastapi import APIRouter, Depends
from sqlmodel import Session as SQLSession
from app.db.session import get_session
from app.db.models import Booking

router = APIRouter()


# Create a new booking
@router.post("/", response_model=Booking)
def create_booking(booking: Booking, db: SQLSession = Depends(get_session)):
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


# Get all bookings for a business
@router.get("/{business_id}", response_model=list[Booking])
def get_bookings(business_id: UUID, db: SQLSession = Depends(get_session)):
    return db.query(Booking).filter(Booking.business_id == business_id).all()


# Get a specific booking by ID
@router.get("/{business_id}/{booking_id}", response_model=Booking)
def get_booking(business_id: UUID, booking_id: UUID, db: SQLSession = Depends(get_session)):
    return db.query(Booking).filter(Booking.business_id == business_id, Booking.id == booking_id).first()


# Update a booking by ID
@router.put("/{business_id}/{booking_id}", response_model=Booking)
def update_booking(business_id: UUID, booking_id: UUID, booking: Booking, db: SQLSession = Depends(get_session)):
    db_booking = db.query(Booking).filter(Booking.business_id == business_id, Booking.id == booking_id).first()
    if db_booking:
        db_booking.customer_name = booking.customer_name
        db_booking.booking_time = booking.booking_time
        db.commit()
        db.refresh(db_booking)
        return db_booking
    return None


# Delete a booking by ID
@router.delete("/{business_id}/{booking_id}")
def delete_booking(business_id: UUID, booking_id: UUID, db: SQLSession = Depends(get_db)):
    db_booking = db.query(Booking).filter(Booking.business_id == business_id, Booking.id == booking_id).first()
    if db_booking:
        db.delete(db_booking)
        db.commit()
        return {"message": "Booking deleted successfully"}
    return {"message": "Booking not found"}
