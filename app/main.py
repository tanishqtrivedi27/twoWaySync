from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models import Customer
from app.database import SessionLocal
from app.kafka_queue import send_to_queue

class CustomerCreate(BaseModel):
    name: str
    email: str
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/customers/")
def add_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    new_customer = Customer(name=customer.name, email=customer.email)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    send_to_queue("customer_updates", f"{new_customer.id},{new_customer.name},{new_customer.email}")

    return new_customer
