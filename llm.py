# llm.py
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import time
import groq
from langchain_core.messages import BaseMessage

load_dotenv()

# Use the smaller model by default — it has a higher rate-limit quota.
# Switch to "openai/gpt-oss-120b" if you need the larger model.
_BASE_MODEL = "openai/gpt-oss-20b"
_FALLBACK_MODEL = "openai/gpt-oss-120b"

_llm_primary  = ChatGroq(model=_BASE_MODEL,   max_retries=2)
_llm_fallback = ChatGroq(model=_FALLBACK_MODEL, max_retries=2)


class _RobustLLM:
    """Wraps ChatGroq with exponential-backoff retry on RateLimitError."""

    def invoke(self, prompt, **kwargs):
        for attempt in range(5):
            try:
                return _llm_primary.invoke(prompt, **kwargs)
            except groq.RateLimitError:
                wait = 2 ** attempt          # 1 s, 2 s, 4 s, 8 s, 16 s
                print(f"[llm] Rate-limit hit (attempt {attempt+1}). "
                      f"Retrying in {wait}s …")
                time.sleep(wait)
        # Last resort — try the larger model (different quota bucket)
        print("[llm] Switching to fallback model for this call.")
        return _llm_fallback.invoke(prompt, **kwargs)


llm = _RobustLLM()