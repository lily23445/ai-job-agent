from state import AgentState
from llm import llm
from nodes.utils import parse_json_response

def generate_questions(state: AgentState) -> dict:
    prompt = f"""
You are a senior software engineer at {state["company_name"]} conducting 
a technical interview. You are rigorous, direct, and go deep.

Generate 15-20 technical interview questions that mirror a real interview loop.
Structure them like this:
- 2-3 questions on fundamentals (Python, data structures)
- 4-5 questions on required skills: {state["required_skills"]}
- 4-5 questions targeting skill gaps: {state["skill_gaps"]}
- 3-4 system design or architecture questions
- 2-3 questions on past weak areas: {state.get("weak_areas", [])}

Rules:
- No HR or behavioural questions
- Each question should require specific technical knowledge to answer
- Questions should get progressively harder
- Ask follow-up style questions that probe depth

Return ONLY a Python list of dicts. No markdown.
[{{"question": "...", "targets_skill": "..."}}]
"""
    content = llm.invoke(prompt).content
    return {"questions": parse_json_response(content)}