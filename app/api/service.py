from uuid import UUID
from fastapi import APIRouter, Depends
from sqlmodel import Session as SQLSession
from app.db.session import get_session
from app.db.models import Service

router = APIRouter()


# Create a new service
@router.post("/", response_model=Service)
def create_service(service: Service, db: SQLSession = Depends(get_session)):
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


# Get all services for a business
@router.get("/{business_id}", response_model=list[Service])
def get_services(business_id: UUID, db: SQLSession = Depends(get_session)):
    return db.query(Service).filter(Service.business_id == business_id).all()


# Get a service by ID
@router.get("/{business_id}/{service_id}", response_model=Service)
def get_service(business_id: UUID, service_id: UUID, db: SQLSession = Depends(get_session)):
    return db.query(Service).filter(Service.business_id == business_id, Service.id == service_id).first()


# Update a service by ID
@router.put("/{business_id}/{service_id}", response_model=Service)
def update_service(business_id: UUID, service_id: UUID, service: Service, db: SQLSession = Depends(get_session)):
    db_service = db.query(Service).filter(Service.business_id == business_id, Service.id == service_id).first()
    if db_service:
        db_service.name = service.name
        db_service.description = service.description
        db.commit()
        db.refresh(db_service)
        return db_service
    return None


# Delete a service by ID
@router.delete("/{business_id}/{service_id}")
def delete_service(business_id: UUID, service_id: UUID, db: SQLSession = Depends(get_session)):
    db_service = db.query(Service).filter(Service.business_id == business_id, Service.id == service_id).first()
    if db_service:
        db.delete(db_service)
        db.commit()
        return {"message": "Service deleted successfully"}
    return {"message": "Service not found"}
