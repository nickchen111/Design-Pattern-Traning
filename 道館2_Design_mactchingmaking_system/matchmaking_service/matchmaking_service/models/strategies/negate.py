from __future__ import annotations

from .MatchmakingStrategy import MatchmakingStrategy

if False:
    from ..individual import Individual


class NegateStrategy(MatchmakingStrategy):
    def __init__(self, inner: MatchmakingStrategy):
        self.inner = inner

    def _score(self, subject: "Individual", candidate: "Individual") -> float:
        return -self.inner._score(subject, candidate)