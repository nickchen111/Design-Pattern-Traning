from __future__ import annotations
from typing import TYPE_CHECKING

from .MatchmakingStrategy import MatchmakingStrategy

if TYPE_CHECKING:
    from ..individual import Individual


class HabitStrategy(MatchmakingStrategy):
    def _score(self, subject: "Individual", candidate: "Individual") -> float:
        return float(len(set(subject.habits_list) & set(candidate.habits_list)))

