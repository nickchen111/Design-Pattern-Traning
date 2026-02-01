from typing import List, Optional
from app.models.base.hand import BaseHand
from app.models.uno.card import Card_uno


class Hand_uno(BaseHand[Card_uno]):
    def _get_playable(self, top_card: Optional[Card_uno]) -> List[Card_uno]:
        if top_card is None:
            return list(self._cards)
        return [c for c in self._cards if c.color == top_card.color or c.number == top_card.number]
