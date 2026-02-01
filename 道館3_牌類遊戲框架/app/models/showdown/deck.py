from app.models.base.deck import BaseDeck
from app.models.showdown.card import Card_showdown, Suit, Rank


class Deck_showdown(BaseDeck[Card_showdown]):
    def _fill_standard(self) -> None:
        if not self._cards:
            for s in (Suit.CLUB, Suit.DIAMOND, Suit.HEART, Suit.SPADE):
                for r in Rank.ranks:
                    self._cards.append(Card_showdown.create(r, s))
