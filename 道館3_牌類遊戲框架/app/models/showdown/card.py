from pydantic import PrivateAttr
from typing import ClassVar
from app.models.base.card import BaseCard


class Rank:
    ranks: ClassVar[list[str]] = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]


class Suit:
    CLUB = "CLUB"
    DIAMOND = "DIAMOND"
    HEART = "HEART"
    SPADE = "SPADE"


class Card_showdown(BaseCard):
    _rank: str = PrivateAttr()
    _suit: str = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        self._repr_fields = ["rank", "suit"]

    @classmethod
    def create(cls, rank: str, suit: str) -> "Card_showdown":
        inst = cls.model_construct()
        inst._rank = rank
        inst._suit = suit
        # ensure repr fields are set even when bypassing __init__ via model_construct
        inst._repr_fields = ["rank", "suit"]
        return inst

    def _compare(self, other: "Card_showdown") -> int:
        rank_values = {r: i for i, r in enumerate(Rank.ranks, start=2)}
        v1 = rank_values[self.rank]
        v2 = rank_values[other.rank]
        if v1 != v2:
            return v1 - v2

        suit_order = {
            Suit.CLUB: 0,
            Suit.DIAMOND: 1,
            Suit.HEART: 2,
            Suit.SPADE: 3,
        }
        s1 = suit_order.get(self.suit, 0)
        s2 = suit_order.get(other.suit, 0)
        return s1 - s2

    def __repr__(self) -> str:
        return f"{self.rank} of {self.suit}"

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def rank(self) -> str:
        return self._rank

    @property
    def suit(self) -> str:
        return self._suit

    @rank.setter
    def rank(self, value: str) -> None:
        self._rank = value

    @suit.setter
    def suit(self, value: str) -> None:
        self._suit = value

    def model_dump(self, *args, **kwargs):
        return super().model_dump(*args, **kwargs)
