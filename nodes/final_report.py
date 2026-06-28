import json
import os
from state import AgentState
from llm import llm
from nodes.utils import parse_json_response

def final_report(state: AgentState) -> dict:
    scores = state.get("scores", [])
    avg = sum(s["score"] for s in scores) / len(scores) if scores else 0

    prompt = f"""
    Generate a final interview prep report for a candidate applying to {state["company_name"]}.

    Scores: {scores}
    Skill gaps: {state.get("skill_gaps", [])}
    Identify the top 2-3 weak areas to focus on.

    Return raw JSON only. No markdown.
    {{"summary": "...", "weak_areas": ["area1", "area2"]}}
    """
    content = llm.invoke(prompt).content
    report = parse_json_response(content)

    os.makedirs("memory", exist_ok=True)
    with open("memory/user_1.json", "w") as f:
        json.dump({"weak_areas": report["weak_areas"]}, f, indent=2)

    print("\n=== FINAL REPORT ===")
    print(f"Average score: {avg:.1f}/10")
    print(f"Summary: {report['summary']}")
    print(f"Weak areas saved: {report['weak_areas']}")

    return {"weak_areas": report["weak_areas"], "report": report["summary"]}
