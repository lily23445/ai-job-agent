from state import AgentState
from llm import llm
from nodes.utils import parse_json_response

def skill_gap(state: AgentState):
    prompt = f"""
    Compare the resume to the required skills and identify gaps.

    Required skills: {state["required_skills"]}
    Resume: {state["resume"]}
    Known weak areas from past sessions: {state.get("weak_areas", [])}

    Return a raw JSON list of missing or weak skills only. No markdown.
    ["skill1", "skill2"]
    """
    content = llm.invoke(prompt).content
    return {"skill_gaps": parse_json_response(content)}