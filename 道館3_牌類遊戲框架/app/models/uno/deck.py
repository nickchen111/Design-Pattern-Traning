from typing import Optional
from app.models.base.deck import BaseDeck
from app.models.uno.card import Card_uno, Color, Number


class Deck_uno(BaseDeck[Card_uno]):
    def _fill_standard(self) -> None:
        if not self._cards:
            for c in (Color.RED, Color.BLUE, Color.YELLOW, Color.GREEN):
                for n in Number:
                    self._cards.append(Card_uno.create(c, n))

    def _flip_card(self) -> Optional[Card_uno]:
        if not self._cards:
            raise IndexError("No cards left in the deck to flip.")
        return self._cards[-1]

