from langgraph_supervisor import create_supervisor
from agents.support_agent import support_agent
from agents.dashboard_agent import dashboard_agent
from config import llm
from prompt_templates import supervisor_prompt
from langgraph.prebuilt.chat_agent_executor import AgentStateWithStructuredResponse

supervisor = create_supervisor(
    model = llm,
    agents=[support_agent, dashboard_agent],
    add_handoff_back_messages=True,
    output_mode="full_history",
    prompt= supervisor_prompt,
    state_schema = AgentStateWithStructuredResponse
)
