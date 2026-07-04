from state import AgentState
from llm import llm
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()

search = TavilySearchResults(max_results=2)
MAX_RESULT_CHARS = 1500

@tool
def web_search(query: str) -> str:
    """Search the web for information about a company.
    Use this to find tech stack, culture, recent news,
    engineering blogs, and what the company actually does."""
    results = search.invoke(query)
    return str(results)[:MAX_RESULT_CHARS]

RESEARCH_AGENT_PROMPT = """You are a company research agent.
Search for information about the company and gather:
- What the company does
- Their tech stack
- Engineering culture
- Recent news
Do at most 2 searches, then summarize concisely."""

# A standalone ReAct sub-agent (own tool-call loop, own message history) that
# the parent LangGraph orchestrator invokes as a single node.
research_agent = create_agent(llm, tools=[web_search], system_prompt=RESEARCH_AGENT_PROMPT)

def research_company(state: AgentState) -> dict:
    result = research_agent.invoke({
        "messages": [
            (
                "human",
                f"Research this company: {state['company_name']}\n"
                f"For a job application requiring: {state['required_skills']}",
            )
        ]
    })
    return {"company_research": result["messages"][-1].content}
