from typing import Optional
from app.models.base.player import BasePlayer
from app.models.showdown.hand import Hand_showdown
from app.models.showdown.card import Card_showdown
from app.models.strategy.player import PlayerStrategy


class Player_showdown(BasePlayer[Card_showdown]):
    def __init__(self, strategy: Optional[PlayerStrategy] = None, **data):
        super().__init__(strategy=strategy, **data)
        if getattr(self, "_hand", None) is None:
            self._hand = Hand_showdown()

    def _take_turn(self, playable: Optional[list] = None, top_card: Optional[Card_showdown] = None, **kwargs) -> Optional[Card_showdown]:
        return super()._take_turn(playable=playable, top_card=top_card, **kwargs)

    def _add_point(self, n: int = 1) -> None:
        self.point += n

    def _format_play(self, card: Optional[Card_showdown]) -> str:
        if card is None:
            return "(no card)"
        return card.__repr__()

    @property
    def point(self) -> int:
        return getattr(self, "_point", 0)

    @point.setter
    def point(self, value: int) -> None:
        setattr(self, "_point", value)

    @property
    def hand(self) -> Hand_showdown:
        return self._hand

    @hand.setter
    def hand(self, value: Optional[Hand_showdown]) -> None:
        self._hand = value or Hand_showdown()


class HumanPlayer_showdown(Player_showdown):
    def _take_turn(self, playable: Optional[list] = None, top_card: Optional[Card_showdown] = None, **kwargs) -> Optional[Card_showdown]:
        if not self.hand._cards:
            return None
        playable = playable or self._hand._get_playable()
        return super()._take_turn(playable=playable, top_card=top_card, **kwargs)
        


class AIPlayer_showdown(Player_showdown):
    def _take_turn(self, playable: Optional[list] = None, top_card: Optional[Card_showdown] = None, **kwargs) -> Optional[Card_showdown]:
        if not self.hand._cards:
            return None
        playable = playable or self.hand._get_playable()
        return super()._take_turn(playable=playable, top_card=top_card, **kwargs)