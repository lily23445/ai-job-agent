import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from langgraph.graph import StateGraph, END, START
from state import AgentState
from nodes.parse_inputs import parse_inputs
from nodes.research_company import research_company
from nodes.skill_gap import skill_gap
from nodes.rewrite_bullets import rewrite_bullets
from nodes.find_resources import find_resources
from nodes.generate_questions import generate_questions
from nodes.present_question import present_question
from nodes.score_answer import score_answer
from nodes.final_report import final_report


def should_continue_interview(state: AgentState) -> str:
    if state["current_question_index"] < len(state["questions"]):
        return "present_question"
    return "final_report"


graph = StateGraph(AgentState)

graph.add_node("parse_inputs", parse_inputs)
graph.add_node("research_company", research_company)
graph.add_node("skill_gap", skill_gap)
graph.add_node("rewrite_bullets", rewrite_bullets)
graph.add_node("find_resources", find_resources)
graph.add_node("generate_questions", generate_questions)
graph.add_node("present_question", present_question)
graph.add_node("score_answer", score_answer)
graph.add_node("final_report", final_report)

graph.add_edge(START, "parse_inputs")
# fan out from parse_inputs
graph.add_edge("parse_inputs", "research_company")
graph.add_edge("parse_inputs", "skill_gap")

# fan in — all three read from research + skill_gap outputs
graph.add_edge(["research_company", "skill_gap"], "rewrite_bullets")
graph.add_edge(["research_company", "skill_gap"], "find_resources")
graph.add_edge(["research_company", "skill_gap"], "generate_questions")

# linear from there
graph.add_edge("generate_questions", "present_question")
graph.add_edge("present_question", "score_answer")
graph.add_conditional_edges(
    "score_answer",
    should_continue_interview,
    {
        "present_question": "present_question",
        "final_report": "final_report"
    }
)
graph.add_edge("final_report", END)

app = graph.compile()

result = app.invoke({
    "job_description": "We are Google, looking for a Python engineer with FastAPI and LLM experience.",
    "resume": "I know Python, Flask, and some ML basics.",
    "current_question_index": 0,  # add this
    "scores": []  # and this
})
