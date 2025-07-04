
# Multi-Agent Backend System for Support & Analytics

A multi-agent backend system designed to handle natural language queries related to **client services** and **business analytics** using LangGraph and ChatGroq, with data stored in **MongoDB** and real-time interactivity via **Streamlit** and **FastAPI**.

---

## Project Overview

This system simulates an AI-powered backend for an education-tech business. It features:

- **Support Agent**: Handles client service, order creation, payment checks, and class info.
- **Dashboard Agent**: Provides business metrics like revenue, attendance, and client stats.
- **Supervisor Agent**: Routes user queries to the appropriate sub-agent intelligently.

Agents use LangGraph to maintain state and ChatGroq (`deepseek-r1-distill-llama-70b`) for reasoning and generation.

---

## Agent Responsibilities

### 1. Support Agent
Handles operational queries via:
- Client lookup (by name, email, or phone)
- Viewing order/payment details
- Creating new enquiries and orders
- Fetching upcoming classes and due amounts

**Tools Used**:
- MongoDB read access (`mongo_tools`)
- External API via FastAPI (`external_api_tool`)

### 2. Dashboard Agent
Handles analytics:
- Total and pending revenue
- Top courses and enrollments
- Attendance percentage
- Active vs inactive clients
- Birthday reminders

**Tools Used**:
- MongoDB aggregations via `mongo_tools`

### 3. Supervisor Agent
Routes user queries to the correct agent using intent-aware prompting and conversation memory.

---

## Tech Stack

| Component      | Technology                        |
|----------------|------------------------------------|
| LLM            | ChatGroq (`deepseek-r1-distill-llama-70b`) |
| Agent Runtime  | LangGraph (with Redis checkpointing) |
| Database       | MongoDB                           |
| Backend API    | FastAPI (external agent API)       |
| UI             | Streamlit (chat interface)         |
| State Storage  | Redis (via LangGraph RedisSaver)   |

---

## Setup Instructions

### 1. Clone and Install
```bash
git clone <repo_url>
cd <folder_name>
pip install -r requirements.txt
```

### 2. Setup Environment
Create a `.env` file:
```env
REDIS_URL=redis://<username>:<password>@<host>:<port>
GROQ_API_KEY=<your_groq_api_key>
```

### 3. Seed Mock Data
```bash
python mock_data.py
```

### 4. Start FastAPI (External API)
```bash
uvicorn api:app --reload
```

### 5. Launch Streamlit App
```bash
streamlit run inference.py
```

---

## Sample Queries (For UI)

- "What classes are coming up this week?"
- "Create a new enquiry for Riya Das, riya@example.com, 9876543210"
- "Generate an order for Data Science Bootcamp for Amit Singh"
- "How much revenue did we make this month?"
- "Show me top 3 enrolled courses"

---

## Project Structure

```
.
├── agents/
│   ├── support_agent.py
│   ├── dashboard_agent.py
│   └── supervisor.py
├── tools/
│   ├── mongo_tools.py
│   └── external_api_tool.py
├── api/
│   ├──app.py              # FastAPI external endpoint
├── inference.py           # Streamlit UI
├── config.py              # LLM, Redis & Mongo setup
├── seed_mock_data.py      # Mock MongoDB seeder
├── prompt_templates.py    # Agent prompt templates
└── README.md
```

---

## 🔌 FastAPI Endpoints

| Endpoint        | Method | Description               |
|-----------------|--------|---------------------------|
| `/enquiry`      | POST   | Creates a new client enquiry |
| `/order`        | POST   | Creates a new order          |

**Example Payloads:**

```json
POST /enquiry
{
  "name": "Riya Das",
  "email": "riya@example.com",
  "phone": "9876543210"
}
```

```json
POST /order
{
  "client_email": "riya@example.com",
  "course_id": "tech_1",
  "amount": 4999
}
```

---

## Testing & Extensibility

- Add multilingual support via translation wrappers
- Devops deployment using Docker, Graffna logging....etc

---

## Credits

Built for the **Multi-Agent Backend Assignment** using LangGraph, ChatGroq, FastAPI, and MongoDB.  
Developed by: Aakarsh Ravi (ZeusYohaan)

---
