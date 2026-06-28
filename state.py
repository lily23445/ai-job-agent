from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    # inputs
    job_description: str
    resume: str
    
    # parsed by node 1
    company_name: str
    required_skills: list[str]
    
    # node outputs
    company_research: str
    skill_gaps: list[str]
    rewritten_bullets: list[str]
    learning_resources: list[str]
    
    # interview loop
    questions: list[dict]
    current_question_index: int
    current_answer: str
    scores: Annotated[list[dict], operator.add]
    
    # long term memory
    weak_areas: list[str]
    report: str
