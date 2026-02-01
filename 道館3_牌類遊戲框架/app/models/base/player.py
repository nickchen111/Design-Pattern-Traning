from __future__ import annotations
from abc import ABC
from pydantic import BaseModel, PrivateAttr
from typing import Generic, Optional, TypeVar, List
from app.models.base.card import BaseCard
from app.models.base.hand import BaseHand
from app.models.strategy.player import PlayerStrategy

C = TypeVar("C", bound="BaseCard")


class BasePlayer(BaseModel, ABC, Generic[C]):
    _name: Optional[str] = PrivateAttr(default=None)
    _hand: Optional[BaseHand[C]] = PrivateAttr(default=None)
    _strategy: Optional[PlayerStrategy] = PrivateAttr(default=None)

    def __init__(self, strategy: Optional[PlayerStrategy] = None, **data):
        super().__init__(**data)
        if getattr(self, "_hand", None) is None:
            self._hand = None
        if strategy is not None:
            self._strategy = strategy

    def _take_turn(self, playable: Optional[List[C]] = None, top_card: Optional[C] = None, **kwargs) -> Optional[C]:
        if self._strategy is None:
            raise NotImplementedError("Player._take_turn not implemented and no strategy set")
        playable = playable or []
        return self._strategy.choose_card(self, playable, top_card=top_card, **kwargs)

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def hand(self) -> BaseHand[C]:
        return self._hand

    @hand.setter
    def hand(self, value: Optional[BaseHand[C]]) -> None:
        self._hand = value

    @property
    def strategy(self) -> Optional[PlayerStrategy]:
        return self._strategy
    @strategy.setter
    def strategy(self, value: Optional[PlayerStrategy]) -> None:
        self._strategy = value

