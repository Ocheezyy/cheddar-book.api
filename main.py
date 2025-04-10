from fastapi import FastAPI
from app.api import booking, business, staff, service
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CheddarBook")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(business.router, prefix="/business", tags=["business"])
app.include_router(staff.router, prefix="/staff", tags=["staff"])
app.include_router(service.router, prefix="/service", tags=["service"])
app.include_router(booking.router, prefix="/booking", tags=["booking"])


@app.get("/")
def root():
    return {"message": "Welcome to CheddarBook 🧀"}
