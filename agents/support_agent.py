from tools.mongo_tools import (
    find_client,
    get_orders,
    get_payments,
    get_pending_dues,
    list_upcoming_classes
)
from tools.external_api_tool import create_order, create_client_enquiry
from config import llm, redis_checkpoint
from langgraph.prebuilt import create_react_agent
from prompt_templates import support_agent_prompt

support_agent = create_react_agent(
    tools=[
        find_client,
        get_orders,
        get_payments,
        get_pending_dues,
        list_upcoming_classes,
        create_order,
        create_client_enquiry
    ],
    model = llm,
    prompt=support_agent_prompt,
    name = "support_agent",
    checkpointer=redis_checkpoint,
)

