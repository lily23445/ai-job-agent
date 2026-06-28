from state import AgentState
from llm import llm
from nodes.utils import parse_json_response

def score_answer(state: AgentState) -> dict:
    idx = state["current_question_index"]
    question = state["questions"][idx]["question"]
    prompt = f"""
    Score this interview answer out of 10 and give brief feedback.

    Question: {question}
    Answer: {state["current_answer"]}

    Return raw JSON only. No markdown.
    {{"score": 7, "feedback": "..."}}
    """
    content = llm.invoke(prompt).content
    result = parse_json_response(content)
    targeted_skill = state["questions"][idx]["targets_skill"]
    weak_areas = state.get("weak_areas", [])

    if result["score"] < 6 and targeted_skill not in weak_areas:
        weak_areas = weak_areas + [targeted_skill]

    return {
        "scores": [{"question": question, **result}],
        "current_question_index": idx + 1,
        "weak_areas": weak_areas,
    }