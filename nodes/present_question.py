from state import AgentState


def present_question(state: AgentState) -> dict:
    idx = state["current_question_index"]
    question = state["questions"][idx]["question"]
    print(f"\nQuestion {idx + 1}: {question}")
    answer = input("Your answer: ").strip()
    return {"current_answer": answer}
