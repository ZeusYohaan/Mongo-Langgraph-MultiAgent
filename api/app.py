from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from datetime import datetime
from config import db
import uuid

app = FastAPI(title="Support Agent External API")


# Request Models
class EnquiryRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str

class OrderRequest(BaseModel):
    client_email: EmailStr
    course_id: str
    amount: float

# Routes
@app.post("/enquiry")
def create_client_enquiry(payload: EnquiryRequest):
    enquiry = {
        "name": payload.name,
        "email": payload.email,
        "phone": payload.phone,
        "dob": "1995-01-01",
        "status": "active",
        "enrolled_services": [],
        "created_at": datetime.now().isoformat()
    }
    db.clients.insert_one(enquiry)
    return {"message": f"Client enquiry for {payload.name} added."}


@app.post("/order")
def create_order(payload: OrderRequest):
    order_id = f"ORD_{uuid.uuid4().hex[:6].upper()}"
    order = {
        "order_id": order_id,
        "client_id": payload.client_email,
        "course_id": payload.course_id,
        "amount": payload.amount,
        "status": "pending",
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    db.orders.insert_one(order)
    return {"message": f"Order {order_id} created for {payload.client_email}."}
