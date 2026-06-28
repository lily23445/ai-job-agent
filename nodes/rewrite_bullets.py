from state import AgentState
from llm import llm
from nodes.utils import parse_json_response

def rewrite_bullets(state: AgentState) -> dict:
    prompt = f"""
    Rewrite the resume as strong bullet points tailored to {state["company_name"]}.

    Required skills: {state["required_skills"]}
    Skill gaps to address: {state["skill_gaps"]}
    Resume: {state["resume"]}

    Return a raw JSON list of bullet point strings. No markdown.
    ["bullet1", "bullet2"]
    """
    content = llm.invoke(prompt).content
    return {"rewritten_bullets": parse_json_response(content)}