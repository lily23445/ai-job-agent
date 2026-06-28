# AI Job Agent

A LangGraph-powered agent that turns a job description and your resume into a complete interview prep session — research, gap analysis, resume rewriting, mock interview, and a final readiness report.

## What it does

1. **Researches the company** — searches the web for tech stack, culture, and recent news so you walk in knowing what they care about
2. **Finds your skill gaps** — honest comparison of what the role requires vs what your resume shows
3. **Rewrites your resume bullets** — tailored to the specific role and company, ATS-friendly
4. **Finds learning resources** — for every gap, surfaces the best free material to study before the interview
5. **Runs a mock technical interview** — 15-20 questions tailored to the role, the company, AND your specific weak areas
6. **Scores every answer** — real AI feedback after each answer so you know exactly where you stand
7. **Generates a readiness report** — average score, summary, and a prioritised list of what to fix
8. **Remembers your weak areas** — next time you use it for a different job, it already knows what you struggled with and weights questions toward those areas

## Stack

- **LangGraph** — agent graph orchestration
- **Groq + Llama 3.3 70B** — LLM for analysis, question generation, and scoring
- **Tavily** — web search for company research and learning resources
- **Streamlit** — 4-screen UI

## Setup

### 1. Clone & install

```bash
git clone https://github.com/lily23445/ai-job-agent.git
cd ai-job-agent
uv sync
```

### 2. Set environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Get keys from:
- Groq: https://console.groq.com
- Tavily: https://app.tavily.com

### 3. Run

```bash
uv run streamlit run app.py
```

Opens at `http://localhost:8501`.

## Agent graph

```
START
  └─ parse_inputs
       ├─ research_company ─┐
       └─ skill_gap ────────┤
                            ├─ rewrite_bullets
                            ├─ find_resources
                            └─ generate_questions
                                  └─ [interview loop]
                                        present_question → score_answer ──┐
                                                          ↑               │ (repeat)
                                                          └───────────────┘
                                        final_report
                                  END
```

## Project structure

```
ai-job-agent/
├── app.py              # Streamlit UI (4 screens)
├── agent.py            # LangGraph graph definition
├── state.py            # AgentState TypedDict
├── llm.py              # LLM client (Groq)
├── nodes/
│   ├── parse_inputs.py
│   ├── research_company.py
│   ├── skill_gap.py
│   ├── rewrite_bullets.py
│   ├── find_resources.py
│   ├── generate_questions.py
│   ├── present_question.py
│   ├── score_answer.py
│   └── final_report.py
└── memory/             # gitignored — stores weak areas per user
```
