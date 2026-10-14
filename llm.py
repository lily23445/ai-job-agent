# llm.py
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import time
import groq

load_dotenv()

# Use the smaller model — it has a higher rate-limit quota on the free tier.
# Falls back to 120b after exhausting retries.
_PRIMARY_MODEL  = "openai/gpt-oss-20b"
_FALLBACK_MODEL = "openai/gpt-oss-120b"


class _RetryingGroq(ChatGroq):
    """ChatGroq subclass that retries on RateLimitError with exponential backoff."""

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        for attempt in range(5):
            try:
                return super()._generate(messages, stop=stop, run_manager=run_manager, **kwargs)
            except groq.RateLimitError:
                wait = 2 ** attempt          # 1 s → 2 s → 4 s → 8 s → 16 s
                print(f"[llm] Rate-limit hit (attempt {attempt + 1}/5). "
                      f"Retrying in {wait}s …")
                time.sleep(wait)
        # Final attempt — switch to the other model (different quota bucket)
        print(f"[llm] All retries exhausted on {self.model_name}. "
              f"Switching to {_FALLBACK_MODEL}.")
        fallback = ChatGroq(model=_FALLBACK_MODEL)
        return fallback._generate(messages, stop=stop, run_manager=run_manager, **kwargs)


llm = _RetryingGroq(model=_PRIMARY_MODEL, max_retries=0)