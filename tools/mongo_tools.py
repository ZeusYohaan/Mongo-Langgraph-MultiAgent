from langchain_core.tools import tool
from config import db

@tool
def find_client(keyword: str) -> dict:
    """Find a client by name, email, or phone."""
    result = db.clients.find_one({
        "$or": [
            {"name": {"$regex": keyword, "$options": "i"}},
            {"email": {"$regex": keyword, "$options": "i"}},
            {"phone": {"$regex": keyword, "$options": "i"}}
        ]
    })
    return result or {}


@tool
def get_orders(client_email: str = "", order_id: str = "", status: str = "") -> list:
    """Retrieve orders by client email, order ID, or status."""
    query = {}
    if client_email:
        query["client_id"] = client_email
    if order_id:
        query["order_id"] = order_id
    if status:
        query["status"] = status
    return list(db.orders.find(query, {"_id": 0}))


@tool
def get_payments(order_id: str) -> list:
    """Get payment details for a specific order ID."""
    return list(db.payments.find({"order_id": order_id}, {"_id": 0}))


@tool
def get_pending_dues(client_email: str) -> float:
    """Calculate total pending dues for a client."""
    orders = db.orders.find({"client_id": client_email, "status": "pending"})
    return sum(order["amount"] for order in orders)


@tool
def list_upcoming_classes(instructor: str = "") -> list:
    """List upcoming classes, optionally filtered by instructor."""
    query = {}
    if instructor:
        query["instructor"] = instructor
    return list(db.classes.find(query, {"_id": 0}))


@tool
def total_revenue() -> float:
    """Calculate total revenue from all payments."""
    pipeline = [{"$group": {"_id": None, "total": {"$sum": "$amount_paid"}}}]
    result = list(db.payments.aggregate(pipeline))
    return result[0]["total"] if result else 0.0


@tool
def outstanding_revenue() -> float:
    """Calculate total outstanding (pending) payment amount."""
    pipeline = [{"$match": {"status": "pending"}}, {"$group": {"_id": None, "total": {"$sum": "$amount"}}}]
    result = list(db.orders.aggregate(pipeline))
    return result[0]["total"] if result else 0.0


@tool
def active_inactive_clients() -> dict:
    """Return count of active and inactive clients."""
    pipeline = [{"$group": {"_id": "$status", "count": {"$sum": 1}}}]
    result = list(db.clients.aggregate(pipeline))
    return {doc["_id"]: doc["count"] for doc in result}


@tool
def birthday_reminders(month: int) -> list:
    """List clients whose birthdays are in a given month (1-12)."""
    query = {
        "$expr": {
            "$eq": [{"$month": {"$dateFromString": {"dateString": "$dob"}}}, month]
        }
    }
    return list(db.clients.find(query, {"_id": 0}))


@tool
def top_courses(limit: int = 3) -> list:
    """List top N courses by enrollment count."""
    pipeline = [
        {"$unwind": "$enrolled_services"},
        {"$group": {"_id": "$enrolled_services.course_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]
    return list(db.clients.aggregate(pipeline))


@tool
def attendance_percentage() -> list:
    """Get attendance percentage by class."""
    pipeline = [
        {"$group": {
            "_id": "$class_id",
            "present": {"$sum": {"$cond": [{"$eq": ["$status", "present"]}, 1, 0]}},
            "total": {"$sum": 1}
        }},
        {"$project": {
            "class_id": "$_id",
            "attendance_percentage": {"$multiply": [{"$divide": ["$present", "$total"]}, 100]}
        }}
    ]
    return list(db.attendance.aggregate(pipeline))
