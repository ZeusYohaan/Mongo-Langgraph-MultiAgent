from langchain_core.tools import tool
from datetime import datetime
import uuid


@tool
def create_client_enquiry(name: str, email: str, phone: str) -> str:
    """Create a new client enquiry with name, email, and phone."""
    client = {
        "name": name,
        "email": email,
        "phone": phone,
        "dob": "1995-01-01",
        "status": "active",
        "enrolled_services": [],
        "created_at": datetime.now().isoformat()
    }
    from pymongo import MongoClient
    db = MongoClient("mongodb://localhost:27017")["Quest_Demo"]
    db.clients.insert_one(client)
    return f"Client enquiry for {name} added."


@tool
def create_order(client_email: str, course_id: str, amount: float) -> str:
    """Create a new order for a client for a specific course."""
    order_id = f"ORD_{uuid.uuid4().hex[:6].upper()}"
    order = {
        "order_id": order_id,
        "client_id": client_email,
        "course_id": course_id,
        "amount": amount,
        "status": "pending",
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    from pymongo import MongoClient
    db = MongoClient("mongodb://localhost:27017")["Quest_Demo"]
    db.orders.insert_one(order)
    return f"Order {order_id} created for {client_email}."
