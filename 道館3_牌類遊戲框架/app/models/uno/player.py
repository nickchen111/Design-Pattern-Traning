from typing import Optional
from app.models.base.player import BasePlayer
from app.models.uno.card import Card_uno
from app.models.uno.hand import Hand_uno
from app.models.strategy.player import PlayerStrategy


class Player_uno(BasePlayer[Card_uno]):
    def __init__(self, strategy: Optional[PlayerStrategy] = None, **data):
        super().__init__(strategy=strategy, **data)
        if getattr(self, "_hand", None) is None:
            self._hand = Hand_uno()

    def _take_turn(self, playable: Optional[list] = None, top_card: Optional[Card_uno] = None, **kwargs) -> Optional[Card_uno]:
        return super()._take_turn(playable=playable, top_card=top_card, **kwargs)


    @property
    def hand(self) -> Hand_uno:
        return self._hand
    
    @hand.setter
    def hand(self, value: Optional[Hand_uno]) -> None:
        self._hand = value or Hand_uno()


class HumanPlayer_uno(Player_uno):
    def _take_turn(self, playable: Optional[list] = None, top_card: Optional[Card_uno] = None, **kwargs) -> Optional[Card_uno]:
        playable = playable or self._hand._get_playable(top_card)
        # show top card
        print(f"Top card on table: {top_card}")
        return super()._take_turn(playable=playable, top_card=top_card, **kwargs)

class AIPlayer_uno(Player_uno):
    def _take_turn(self, playable: Optional[list] = None, top_card: Optional[Card_uno] = None, **kwargs) -> Optional[Card_uno]:
        playable = playable or self._hand._get_playable(top_card)
        return super()._take_turn(playable=playable, top_card=top_card, **kwargs)
