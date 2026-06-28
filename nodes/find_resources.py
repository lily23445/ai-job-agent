from state import AgentState
from nodes.research_company import search

def find_resources(state: AgentState) -> dict:
    resources = []
    for skill in state["skill_gaps"]:
        try:
            results = search.invoke(f"best free resources to learn {skill}")
            for r in results:
                title = r.get("title") or r.get("content", "Resource")[:60]
                url = r.get("url", "")
                resources.append(f"{skill}: {title} - {url}")
        except Exception:
            pass
    return {"learning_resources": resources}