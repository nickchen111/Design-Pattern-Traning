from __future__ import annotations
from typing import TYPE_CHECKING

from .MatchmakingStrategy import MatchmakingStrategy

if TYPE_CHECKING:
    from ..individual import Individual


class DistanceStrategy(MatchmakingStrategy):
    def _score(self, subject: "Individual", candidate: "Individual") -> float:
        dx = subject.coord[0] - candidate.coord[0]
        dy = subject.coord[1] - candidate.coord[1]
        dist2 = dx * dx + dy * dy
        return -dist2

