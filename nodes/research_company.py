from state import AgentState
from llm import llm
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from dotenv import load_dotenv
load_dotenv()
search = TavilySearchResults(max_results=2)

MAX_SEARCH_ITERATIONS = 2
MAX_RESULT_CHARS = 1500

@tool
def web_search(query: str) -> str:
    """Search the web for information about a company.
    Use this to find tech stack, culture, recent news,
    engineering blogs, and what the company actually does."""
    results = search.invoke(query)
    return str(results)[:MAX_RESULT_CHARS]

tools = [web_search]
research_llm = llm.bind_tools(tools)

def research_company(state: AgentState) -> dict:
    system = SystemMessage(content="""You are a company research agent.
    Search for information about the company and gather:
    - What the company does
    - Their tech stack
    - Engineering culture
    - Recent news
    Do at most 2 searches, then summarize concisely.""")

    human = HumanMessage(content=f"""
    Research this company: {state['company_name']}
    For a job application requiring: {state['required_skills']}
    """)

    messages = [system, human]
    iterations = 0

    while iterations < MAX_SEARCH_ITERATIONS:
        response = research_llm.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            break

        for tool_call in response.tool_calls:
            result = web_search.invoke(tool_call["args"])
            messages.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))

        iterations += 1

    # if the last response still wants to call tools, get a final summary
    if response.tool_calls:
        messages.append(HumanMessage(content="Summarize what you've found so far."))
        response = llm.invoke(messages)

    return {"company_research": response.content}
