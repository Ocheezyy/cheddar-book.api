from uuid import UUID
from fastapi import APIRouter, Depends
from sqlmodel import Session as SQLSession
from app.db.session import get_session
from app.db.models import Staff

router = APIRouter()


# Create a new staff member
@router.post("/", response_model=Staff)
def create_staff(staff: Staff, db: SQLSession = Depends(get_session)):
    db.add(staff)
    db.commit()
    db.refresh(staff)
    return staff


# Get all staff for a business
@router.get("/{business_id}", response_model=list[Staff])
def get_staff(business_id: UUID, db: SQLSession = Depends(get_session)):
    return db.query(Staff).filter(Staff.business_id == business_id).all()


# Get a specific staff member by ID
@router.get("/{business_id}/{staff_id}", response_model=Staff)
def get_staff_by_id(business_id: UUID, staff_id: UUID, db: SQLSession = Depends(get_session)):
    return db.query(Staff).filter(Staff.business_id == business_id, Staff.id == staff_id).first()


# Update a staff member's details
@router.put("/{business_id}/{staff_id}", response_model=Staff)
def update_staff(business_id: UUID, staff_id: UUID, staff: Staff, db: SQLSession = Depends(get_session)):
    db_staff = db.query(Staff).filter(Staff.business_id == business_id, Staff.id == staff_id).first()
    if db_staff:
        db_staff.name = staff.name
        db_staff.position = staff.position
        db.commit()
        db.refresh(db_staff)
        return db_staff
    return None


# Delete a staff member by ID
@router.delete("/{business_id}/{staff_id}")
def delete_staff(business_id: UUID, staff_id: UUID, db: SQLSession = Depends(get_db)):
    db_staff = db.query(Staff).filter(Staff.business_id == business_id, Staff.id == staff_id).first()
    if db_staff:
        db.delete(db_staff)
        db.commit()
        return {"message": "Staff member deleted successfully"}
    return {"message": "Staff member not found"}
