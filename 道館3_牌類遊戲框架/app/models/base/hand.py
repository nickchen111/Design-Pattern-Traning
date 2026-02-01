from __future__ import annotations
from abc import ABC, abstractmethod
from pydantic import BaseModel, PrivateAttr
from typing import Generic, Iterator, List, Optional, TypeVar

C = TypeVar("C")


class BaseHand(BaseModel, ABC, Generic[C]):
    _cards: List[C] = PrivateAttr(default_factory=list)

    def _add(self, card: C) -> None:
        self._cards.append(card)

    def _remove(self, card: C) -> None:
        self._cards.remove(card)

    @abstractmethod
    def _get_playable(self, top_card: Optional[C]) -> List[C]:
        ...

    def __len__(self) -> int:
        return len(self._cards)

    def __iter__(self) -> Iterator[C]:
        return iter(self._cards)

    def _receive_card(self, card: C) -> None:
        if not card:
            raise ValueError("Cannot receive a None card")
        self._cards.append(card)

    @property
    def cards(self) -> List[C]:
        return self._cards

    @cards.setter
    def cards(self, value: Optional[List[C]]) -> None:
        self._cards = value or []

