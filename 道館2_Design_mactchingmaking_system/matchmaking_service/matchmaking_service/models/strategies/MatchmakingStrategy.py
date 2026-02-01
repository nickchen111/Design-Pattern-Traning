from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..individual import Individual


class MatchmakingStrategy(ABC):
    @abstractmethod
    def _score(self, subject: "Individual", candidate: "Individual") -> float:
        """Return a numeric score for candidate relative to subject. Higher is better."""

    def _rank(self, subject: "Individual", candidates: List["Individual"]) -> List["Individual"]:
        return sorted(candidates, key=lambda c: self._score(subject, c), reverse=True)