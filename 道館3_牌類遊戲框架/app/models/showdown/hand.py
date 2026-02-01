from typing import List
from app.models.base.hand import BaseHand
from app.models.showdown.card import Card_showdown


class Hand_showdown(BaseHand[Card_showdown]):
    def _get_playable(self) -> List[Card_showdown]:
        return [c for c in self._cards]
