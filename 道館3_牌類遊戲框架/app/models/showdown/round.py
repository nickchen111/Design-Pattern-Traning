from typing import List, Optional, Tuple
from app.models.showdown.card import Card_showdown
from app.models.showdown.player import Player_showdown


class Round:
    def __init__(self, plays: List[Tuple[Player_showdown, Optional[Card_showdown]]]):
        self.plays = plays

    def _show_plays(self) -> None:
        for p, c in self.plays:
            print(f"  {p.name}: {p._format_play(c)}")

    def _determine_winner(self) -> Optional[Player_showdown]:
        winner: Optional[Player_showdown] = None
        winning_card: Optional[Card_showdown] = None
        for p, c in self.plays:
            if c is None:
                continue
            if winning_card is None:
                winner = p
                winning_card = c
                continue
            if winning_card._compare(c) < 0:
                winning_card = c
                winner = p
        return winner
