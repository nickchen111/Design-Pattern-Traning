from __future__ import annotations
from abc import ABC, abstractmethod
from pydantic import BaseModel, PrivateAttr
from typing import Generic, List, Optional, TypeVar
import random

C = TypeVar("C")


class BaseDeck(BaseModel, ABC, Generic[C]):
    _cards: List[C] = PrivateAttr(default_factory=list)
    _discard: List[C] = PrivateAttr(default_factory=list)

    @abstractmethod
    def _fill_standard(self) -> None:
        ...

    def _shuffle(self) -> None:
        random.shuffle(self._cards)

    def _draw_card(self) -> Optional[C]:
        if not self._cards:
            self._refill_from_discard()
            if not self._cards:
                return None
        return self._cards.pop()

    def _discard_card(self, card: C) -> None:
        self._discard.append(card)

    def _refill_from_discard(self, latest_card: Optional[C] = None) -> None:
        if not self._discard:
            return
        to_refill = []
        for c in self._discard:
            if latest_card is not None and c is latest_card:
                continue
            to_refill.append(c)
        self._discard = [c for c in self._discard if c is latest_card]
        random.shuffle(to_refill)
        self._cards = to_refill + self._cards

    @property
    def cards(self) -> List[C]:
        return self._cards

    @cards.setter
    def cards(self, value: Optional[List[C]]) -> None:
        self._cards = value or []

