from tools.mongo_tools import (
    total_revenue,
    outstanding_revenue,
    active_inactive_clients,
    birthday_reminders,
    top_courses,
    attendance_percentage,
)

from config import llm, redis_checkpoint
from langgraph.prebuilt import create_react_agent
from prompt_templates import support_agent_prompt

dashboard_agent = create_react_agent(
    tools=[
        total_revenue,
        outstanding_revenue,
        active_inactive_clients,
        birthday_reminders,
        top_courses,
        attendance_percentage,
    ],
    model = llm,
    prompt=support_agent_prompt,
    name = "dashboard_agent",
    checkpointer=redis_checkpoint,
)
