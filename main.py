from fastapi import FastAPI
from app.api import booking, business, staff, service

app = FastAPI(title="CheddarBook")

app.include_router(business.router, prefix="/business", tags=["business"])
app.include_router(staff.router, prefix="/staff", tags=["staff"])
app.include_router(service.router, prefix="/service", tags=["service"])
app.include_router(booking.router, prefix="/booking", tags=["booking"])


@app.get("/")
def root():
    return {"message": "Welcome to CheddarBook 🧀"}
