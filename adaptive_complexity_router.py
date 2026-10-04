#!/usr/bin/env python3
"""
Adaptive Complexity Router for Claude 3.7 Sonnet
Dynamically allocates 0 tokens (Instant) vs High Budget (Extended Thinking)
"""
import re
from typing import Dict, Any

class AdaptiveComplexityRouter:
    COMPLEX_PATTERNS = [
        r"\b(prove|refactor|debug|architect|concurrency|deadlock|formal verification)\b",
        r"\b(distributed|consensus|byzantine|microservices|failover|sub-millisecond)\b",
        r"\b(kernel|ebpf|assembly|memory leak|buffer overflow|zero-day)\b"
    ]

    def __init__(self, max_budget: int = 16384):
        self.max_budget = max_budget

    def determine_thinking_budget(self, user_prompt: str) -> Dict[str, Any]:
        prompt_lower = user_prompt.lower()
        score = sum(1 for pattern in self.COMPLEX_PATTERNS if re.search(pattern, prompt_lower))
        
        if score == 0 and len(user_prompt.split()) < 30:
            return {"mode": "fast_instant", "thinking": None, "budget_tokens": 0}
        elif score == 1:
            return {"mode": "moderate", "thinking": {"type": "enabled", "budget_tokens": 4096}, "budget_tokens": 4096}
        else:
            return {"mode": "deep_extended", "thinking": {"type": "enabled", "budget_tokens": self.max_budget}, "budget_tokens": self.max_budget}

if __name__ == "__main__":
    router = AdaptiveComplexityRouter()
    print("Simple prompt result:", router.determine_thinking_budget("What is DNS?"))
    print("Complex prompt result:", router.determine_thinking_budget("Debug distributed deadlock in Raft consensus."))
