from faker import Faker
import random
import datetime
import uuid
from config import db

fake = Faker("en_IN")


# Reset all collections
for col in ["clients", "courses", "classes", "orders", "payments", "attendance"]:
    db[col].delete_many({})

# 1. Tech Courses
course_names = [
    "Python Programming",
    "Data Science Bootcamp",
    "Machine Learning with Python",
    "Web Development with React",
    "Full Stack Java Development",
    "Cloud Computing (AWS)",
    "DevOps with Docker & Kubernetes"
]

instructors = [
    "Rohan Menon",
    "Sneha Pillai",
    "Arjun Deshmukh",
    "Divya Natarajan",
    "Karthik Rao",
    "Meera Iyer"
]

courses = []
for i, course in enumerate(course_names):
    course_id = f"tech_{i+1}"
    instructor = random.choice(instructors)
    status = random.choice(["ongoing", "upcoming"])
    duration = random.choice([4, 6, 8])
    courses.append({
        "course_id": course_id,
        "name": course,
        "instructor": instructor,
        "duration_weeks": duration,
        "status": status
    })

db.courses.insert_many(courses)

# 2. Classes
tech_locations = ["Koramangala", "Whitefield", "Hitech City", "T-Nagar", "Hadapsar"]
classes = []
for course in courses:
    for j in range(1, 4):  # 3 classes per course
        class_id = f"{course['course_id']}_class_{j}"
        date = (datetime.datetime.now() + datetime.timedelta(days=j*3)).strftime('%Y-%m-%d')
        classes.append({
            "class_id": class_id,
            "course_id": course["course_id"],
            "date": date,
            "time": "18:30",
            "location": random.choice(tech_locations),
            "instructor": course["instructor"]
        })

db.classes.insert_many(classes)

# 3. Clients (Tech learners)
clients = []
for _ in range(10):
    name = fake.name()
    email = fake.email()
    phone = fake.phone_number()
    dob = fake.date_of_birth(minimum_age=20, maximum_age=35)
    status = random.choice(["active", "inactive"])
    enrolled_course = random.choice(courses)
    clients.append({
        "name": name,
        "email": email,
        "phone": phone,
        "dob": dob.isoformat(),
        "status": status,
        "enrolled_services": [{
            "course_id": enrolled_course["course_id"],
            "status": "active" if status == "active" else "completed"
        }],
        "created_at": datetime.datetime.now().isoformat()
    })

db.clients.insert_many(clients)

# 4. Orders & Payments
orders = []
payments = []

for client in clients:
    course = client["enrolled_services"][0]
    course_id = course["course_id"]
    order_id = f"ORD_{uuid.uuid4().hex[:6].upper()}"
    amount = random.choice([4999, 5999, 7499])
    status = random.choice(["paid", "pending"])
    order = {
        "order_id": order_id,
        "client_id": client["email"],
        "course_id": course_id,
        "amount": amount,
        "status": status,
        "date": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    orders.append(order)

    if status == "paid":
        payment_id = f"PAY_{uuid.uuid4().hex[:6].upper()}"
        payments.append({
            "payment_id": payment_id,
            "order_id": order_id,
            "amount_paid": amount,
            "method": random.choice(["UPI", "Card", "NetBanking"]),
            "date": datetime.datetime.now().strftime("%Y-%m-%d")
        })

db.orders.insert_many(orders)
db.payments.insert_many(payments)

# 5. Attendance
attendance = []
for client in clients:
    course_id = client["enrolled_services"][0]["course_id"]
    related_classes = [c for c in classes if c["course_id"] == course_id]
    for cl in related_classes:
        attendance.append({
            "client_id": client["email"],
            "class_id": cl["class_id"],
            "status": random.choice(["present", "absent"])
        })

db.attendance.insert_many(attendance)

print(" Tech course data inserted into MongoDB.")
