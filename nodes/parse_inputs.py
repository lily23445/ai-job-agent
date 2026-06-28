import os
from state import AgentState
from llm import llm
from nodes.utils import parse_json_response
import json


def load_weak_areas(user_id: str) -> list[str]:
    path = f"memory/{user_id}.json"
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f).get("weak_areas", [])
    return []


def parse_inputs(state: AgentState) -> dict:
    prompt = f"""
    Extract from this job description:
    1. Company name
    2. Required skills as a list

    Job Description:
    {state["job_description"]}

    Respond in raw JSON only. No markdown, no code fences.
    {{"company_name": "...", "required_skills": ["skill1", "skill2"]}}
    """
    content = llm.invoke(prompt).content
    parsed = parse_json_response(content)
    return {
        "company_name": parsed["company_name"],
        "required_skills": parsed["required_skills"],
        "weak_areas": load_weak_areas("user_1"),
    }
