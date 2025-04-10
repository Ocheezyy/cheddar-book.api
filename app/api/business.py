from uuid import UUID
from fastapi import APIRouter, Depends
from sqlmodel import Session as SQLSession
from app.auth.dependencies import require_role
from app.auth.models import User
from app.db.session import get_session
from app.db.models import Business

router = APIRouter()


# Create a new business
@router.post("/", response_model=Business)
def create_business(
        business: Business,
        db: SQLSession = Depends(get_session),
        user: User = Depends(require_role("owner"))
):
    db.add(business)
    db.commit()
    db.refresh(business)
    return business


# Get all businesses
@router.get("/", response_model=list[Business])
def get_businesses(db: SQLSession = Depends(get_session)):
    return db.query(Business).all()


# Get a business by ID
@router.get("/{business_id}", response_model=Business)
def get_business(business_id: UUID, db: SQLSession = Depends(get_session)):
    return db.query(Business).filter(Business.id == business_id).first()


# Update a business by ID
@router.put("/{business_id}", response_model=Business)
def update_business(business_id: UUID, business: Business, db: SQLSession = Depends(get_session)):
    db_business = db.query(Business).filter(Business.id == business_id).first()
    if db_business:
        db_business.name = business.name
        db_business.location = business.location
        db.commit()
        db.refresh(db_business)
        return db_business
    return None


# Delete a business by ID
@router.delete("/{business_id}")
def delete_business(business_id: UUID, db: SQLSession = Depends(get_session), user: User = Depends(require_role("owner"))):
    db_business = db.query(Business).filter(Business.id == business_id).first()
    if db_business:
        db.delete(db_business)
        db.commit()
        return {"message": "Business deleted successfully"}
    return {"message": "Business not found"}
