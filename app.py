import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st

from nodes.parse_inputs import parse_inputs
from nodes.research_company import research_company
from nodes.skill_gap import skill_gap
from nodes.rewrite_bullets import rewrite_bullets
from nodes.find_resources import find_resources
from nodes.generate_questions import generate_questions
from nodes.score_answer import score_answer as _score_node
from nodes.final_report import final_report as _report_node

st.set_page_config(page_title="AI Job Agent", page_icon="🧭", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');

/* Base */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp {
    background:
        radial-gradient(circle at 15% 0%, rgba(108,99,255,0.12), transparent 45%),
        radial-gradient(circle at 85% 15%, rgba(167,139,250,0.10), transparent 40%),
        #0b0d14;
    color: #e0e0e0;
}
h1, h2, h3 { font-family: 'Sora', sans-serif; color: #ffffff; letter-spacing: -0.01em; }

h2:first-of-type, .stMarkdown h2 {
    background: linear-gradient(90deg, #ffffff 20%, #a78bfa 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    display: inline-block;
}

/* Cards */
.card, div[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(180deg, #171a29 0%, #14161f 100%) !important;
    border: 1px solid #262b45 !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 18px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.03);
    transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
    position: relative;
}
.card { padding: 20px 24px; margin-bottom: 16px; overflow: hidden; }
.card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #6c63ff, #a78bfa, #f472b6);
    opacity: 0.9;
}
.card:hover, div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: #3d4372 !important;
    box-shadow: 0 8px 28px rgba(108,99,255,0.14), inset 0 1px 0 rgba(255,255,255,0.05);
}
.card-title {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #9aa4e8;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Badges */
.badge {
    display: inline-block;
    background: #232748;
    border: 1px solid #333a63;
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 13px;
    font-weight: 500;
    margin: 4px;
    color: #c0c8f0;
    transition: transform 0.15s ease;
}
.badge:hover { transform: translateY(-1px); }
.badge-red { background: #3b1f2b; border-color: #5c2c3d; color: #f5a3a3; }
.badge-green { background: #16352a; border-color: #1f4d3a; color: #8ff0b4; }

/* Progress bar */
.progress-track {
    background: #1c2036;
    border: 1px solid #262b45;
    border-radius: 8px;
    height: 10px;
    width: 100%;
    margin: 8px 0 16px;
    overflow: hidden;
}
.progress-fill {
    background: linear-gradient(90deg, #6c63ff, #a78bfa, #f472b6);
    border-radius: 8px;
    height: 100%;
    box-shadow: 0 0 12px rgba(167,139,250,0.6);
    transition: width 0.4s ease;
}

/* Score ring */
.score-circle {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 72px; height: 72px;
    border-radius: 50%;
    border: 4px solid;
    font-family: 'Sora', sans-serif;
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 8px;
    background: #14161f;
    box-shadow: 0 0 0 6px rgba(255,255,255,0.02);
}

/* Divider */
.divider { border: none; border-top: 1px solid #262b45; margin: 22px 0; }

/* Text areas */
.stTextArea textarea {
    background: #14161f !important;
    border: 1px solid #262b45 !important;
    border-radius: 10px !important;
    color: #e6e8f5 !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.stTextArea textarea:focus {
    border-color: #6c63ff !important;
    box-shadow: 0 0 0 3px rgba(108,99,255,0.25) !important;
}

/* Override Streamlit button */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 700 !important;
    padding: 10px 28px !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #6c63ff, #8b7bff) !important;
    border: none !important;
    box-shadow: 0 4px 16px rgba(108,99,255,0.35) !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 22px rgba(108,99,255,0.5) !important;
}
.stButton > button:not([kind="primary"]):hover {
    transform: translateY(-1px);
    border-color: #6c63ff !important;
    color: #a78bfa !important;
}
</style>
""", unsafe_allow_html=True)


# ── Session state ────────────────────────────────────────────────────────────

def _init():
    defaults = {
        "screen": "input",
        "job_description": "",
        "resume": "",
        "results": None,          # dict from run_analysis()
        "current_q": 0,
        "scores": [],             # list of {question, score, feedback}
        "last_feedback": None,    # shown after submitting an answer
        "report": None,           # dict from generate_report()
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()


# ── Real agent calls ─────────────────────────────────────────────────────────

def run_analysis(job_desc: str, resume: str) -> dict:
    state: dict = {
        "job_description": job_desc,
        "resume": resume,
        "current_question_index": 0,
        "scores": [],
        "weak_areas": [],
    }
    state.update(parse_inputs(state))
    state.update(research_company(state))
    state.update(skill_gap(state))
    state.update(rewrite_bullets(state))
    state.update(find_resources(state))
    state.update(generate_questions(state))
    return {
        "company_name": state["company_name"],
        "company_research": state["company_research"],
        "skill_gaps": state["skill_gaps"],
        "rewritten_bullets": state["rewritten_bullets"],
        "learning_resources": state["learning_resources"],
        "questions": state["questions"],
    }


def score_answer(question: str, answer: str, targets_skill: str) -> dict:
    questions = st.session_state.results["questions"]
    idx = st.session_state.current_q
    state: dict = {
        "questions": questions,
        "current_question_index": idx,
        "current_answer": answer,
        "weak_areas": [s["targets_skill"] for s in st.session_state.scores if s["score"] < 6],
    }
    result = _score_node(state)
    scored = result["scores"][0]
    return {"score": scored["score"], "feedback": scored["feedback"]}


def generate_report(scores: list, skill_gaps: list, company_name: str) -> dict:
    state: dict = {
        "company_name": company_name,
        "scores": scores,
        "skill_gaps": skill_gaps,
        "weak_areas": [],
    }
    result = _report_node(state)
    avg = sum(s["score"] for s in scores) / len(scores) if scores else 0
    return {
        "average_score": avg,
        "summary": result["report"],
        "weak_areas": result["weak_areas"],
        "learning_resources": st.session_state.results.get("learning_resources", []),
    }


# ── Helpers ──────────────────────────────────────────────────────────────────

def score_color(score: int) -> str:
    if score >= 8:
        return "#4ade80"
    if score >= 5:
        return "#facc15"
    return "#f87171"


def go(screen: str):
    st.session_state.screen = screen
    st.rerun()


# ── Screen 1 – Input ─────────────────────────────────────────────────────────

def screen_input():
    st.markdown("## 🧭 AI Job Agent")
    st.markdown(
        '<span style="color:#9aa4e8;font-size:15px">'
        'Paste the job description and your resume to get a personalised prep report.</span>',
        unsafe_allow_html=True,
    )
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("**Job Description**")
        jd = st.text_area(
            label="job_description",
            label_visibility="collapsed",
            height=320,
            placeholder="Paste the full job posting here…",
            value=st.session_state.job_description,
            key="jd_input",
        )
    with col2:
        st.markdown("**Your Resume**")
        res = st.text_area(
            label="resume",
            label_visibility="collapsed",
            height=320,
            placeholder="Paste your resume text here…",
            value=st.session_state.resume,
            key="res_input",
        )

    st.markdown("")
    _, btn_col, _ = st.columns([3, 2, 3])
    with btn_col:
        if st.button("Analyse & Start →", use_container_width=True, type="primary"):
            if not jd.strip() or not res.strip():
                st.error("Please fill in both fields before continuing.")
            else:
                st.session_state.job_description = jd
                st.session_state.resume = res
                with st.spinner("Running agent… this may take a moment"):
                    st.session_state.results = run_analysis(jd, res)
                st.session_state.current_q = 0
                st.session_state.scores = []
                st.session_state.last_feedback = None
                go("results")


# ── Screen 2 – Results ───────────────────────────────────────────────────────

def screen_results():
    r = st.session_state.results
    st.markdown(f"## 📊 Results — {r['company_name']}")
    if st.button("← Back"):
        go("input")
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2], gap="large")

    with col_left:
        # Company research
        st.markdown('<div class="card-title">🏢 Company Research</div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.write(r["company_research"])

        # Rewritten bullets
        st.markdown('<div class="card-title" style="margin-top:16px">✍️ Rewritten Resume Bullets</div>', unsafe_allow_html=True)
        with st.container(border=True):
            bullets = r.get("rewritten_bullets") or []
            if bullets:
                for b in bullets:
                    st.markdown(f"- {b}")
            else:
                st.caption("No bullets generated.")

    with col_right:
        # Skill gaps
        st.markdown('<div class="card-title">🎯 Skill Gaps</div>', unsafe_allow_html=True)
        with st.container(border=True):
            gaps = r.get("skill_gaps") or []
            if gaps:
                gaps_html = "".join(f'<span class="badge badge-red">{g}</span>' for g in gaps)
                st.markdown(gaps_html, unsafe_allow_html=True)
            else:
                st.caption("No gaps identified.")

        # Learning resources
        st.markdown('<div class="card-title" style="margin-top:16px">📚 Learning Resources</div>', unsafe_allow_html=True)
        with st.container(border=True):
            resources = r.get("learning_resources") or []
            if resources:
                for res in resources:
                    st.markdown(f"- {res}")
            else:
                st.caption("No resources found.")

    st.markdown("")
    _, btn_col, _ = st.columns([3, 2, 3])
    with btn_col:
        if st.button("Start Interview →", use_container_width=True, type="primary"):
            go("interview")


# ── Screen 3 – Interview Loop ────────────────────────────────────────────────

def screen_interview():
    r = st.session_state.results
    questions = r["questions"]
    total = len(questions)
    idx = st.session_state.current_q

    # All questions answered → final report
    if idx >= total:
        st.session_state.report = generate_report(
            st.session_state.scores, r["skill_gaps"], r["company_name"]
        )
        go("report")
        return

    q = questions[idx]
    progress_pct = int(idx / total * 100)

    st.markdown(f"## 🎤 Interview — {r['company_name']}")
    st.markdown(f"Question **{idx + 1}** of **{total}**")
    st.markdown(
        f'<div class="progress-track"><div class="progress-fill" style="width:{progress_pct}%"></div></div>',
        unsafe_allow_html=True,
    )

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Show question
    st.markdown(
        f'<div class="card"><div class="card-title">💬 Question {idx + 1}</div>'
        f'<span style="font-size:17px;line-height:1.5">{q["question"]}</span></div>',
        unsafe_allow_html=True,
    )

    # If feedback for the previous submit is waiting, show it first
    if st.session_state.last_feedback:
        fb = st.session_state.last_feedback
        color = score_color(fb["score"])
        st.markdown(
            f'<div class="card" style="border-color:{color}44">'
            f'<div class="card-title">✅ Last Answer — Score</div>'
            f'<div style="display:flex;align-items:center;gap:16px">'
            f'<div class="score-circle" style="border-color:{color};color:{color}">{fb["score"]}</div>'
            f'<div style="flex:1">{fb["feedback"]}</div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )
        st.session_state.last_feedback = None

    # Answer input
    st.markdown("**Your Answer**")
    answer = st.text_area(
        label="answer",
        label_visibility="collapsed",
        height=180,
        placeholder="Type your answer here…",
        key=f"answer_{idx}",
    )

    _, btn_col, _ = st.columns([3, 2, 3])
    with btn_col:
        if st.button("Submit Answer →", use_container_width=True, type="primary"):
            if not answer.strip():
                st.error("Please write an answer before submitting.")
            else:
                with st.spinner("Scoring…"):
                    result = score_answer(q["question"], answer, q["targets_skill"])
                st.session_state.scores.append({
                    "question": q["question"],
                    "targets_skill": q["targets_skill"],
                    "score": result["score"],
                    "feedback": result["feedback"],
                })
                st.session_state.last_feedback = result
                st.session_state.current_q += 1
                st.rerun()


# ── Screen 4 – Final Report ──────────────────────────────────────────────────

def screen_report():
    rep = st.session_state.report
    avg = rep["average_score"]
    color = score_color(int(avg))

    st.markdown("## 🏆 Final Report")
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Average score hero
    st.markdown(
        f'<div style="text-align:center;margin-bottom:24px">'
        f'<div class="score-circle" style="border-color:{color};color:{color};width:96px;height:96px;font-size:28px;margin:0 auto 8px">{avg:.1f}</div>'
        f'<div style="color:#7c85b3;font-size:14px">Average Score / 10</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    col_left, col_right = st.columns([3, 2], gap="large")

    with col_left:
        # Summary
        st.markdown(
            f'<div class="card"><div class="card-title">📝 Summary</div>{rep["summary"]}</div>',
            unsafe_allow_html=True,
        )

        # Per-question breakdown
        rows_html = ""
        for s in st.session_state.scores:
            c = score_color(s["score"])
            rows_html += (
                f'<div style="display:flex;justify-content:space-between;align-items:flex-start;'
                f'padding:10px 0;border-bottom:1px solid #262b45">'
                f'<div style="flex:1;padding-right:16px;font-size:14px">{s["question"]}</div>'
                f'<div style="color:{c};font-weight:700;font-size:16px;white-space:nowrap">{s["score"]}/10</div>'
                f'</div>'
            )
        st.markdown(
            f'<div class="card"><div class="card-title">📋 Question Breakdown</div>{rows_html}</div>',
            unsafe_allow_html=True,
        )

    with col_right:
        # Weak areas
        weak_html = "".join(f'<span class="badge badge-red">{w}</span>' for w in rep["weak_areas"])
        st.markdown(
            f'<div class="card"><div class="card-title">⚠️ Weak Areas to Focus On</div>{weak_html}</div>',
            unsafe_allow_html=True,
        )

        # Resources
        res_html = "".join(f"<li style='margin-bottom:8px'>{r}</li>" for r in rep["learning_resources"])
        st.markdown(
            f'<div class="card"><div class="card-title">📚 Learning Resources</div><ul style="margin:0;padding-left:18px">{res_html}</ul></div>',
            unsafe_allow_html=True,
        )

    st.markdown("")
    _, btn_col, _ = st.columns([3, 2, 3])
    with btn_col:
        if st.button("Start Over", use_container_width=True):
            for key in ["screen", "job_description", "resume", "results",
                        "current_q", "scores", "last_feedback", "report"]:
                del st.session_state[key]
            _init()
            go("input")


# ── Router ────────────────────────────────────────────────────────────────────

{
    "input": screen_input,
    "results": screen_results,
    "interview": screen_interview,
    "report": screen_report,
}[st.session_state.screen]()
