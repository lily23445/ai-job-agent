from state import AgentState
from llm import llm
from nodes.research_company import web_search
from nodes.utils import parse_json_response
from langchain.agents import create_agent

RESOURCES_AGENT_PROMPT = """You are a learning-resources agent.
For each skill gap given, search the web and pick the single best free
resource to learn it (prefer official docs, well-known tutorials, or
highly-rated courses over random blog posts).
Do at most one search per skill.

When done, respond with ONLY a raw JSON list of strings, no markdown,
each formatted as "<skill>: <title> - <url>"."""

resources_agent = create_agent(llm, tools=[web_search], system_prompt=RESOURCES_AGENT_PROMPT)

def find_resources(state: AgentState) -> dict:
    skill_gaps = state["skill_gaps"]
    if not skill_gaps:
        return {"learning_resources": []}

    result = resources_agent.invoke({
        "messages": [
            ("human", f"Find the best free learning resource for each of these skills: {skill_gaps}")
        ]
    })
    content = result["messages"][-1].content
    return {"learning_resources": parse_json_response(content)}
