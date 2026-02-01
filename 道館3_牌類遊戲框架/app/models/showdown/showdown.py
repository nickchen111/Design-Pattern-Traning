from typing import List, Optional
from app.models.showdown.deck import Deck_showdown
from app.models.showdown.player import Player_showdown
from app.models.base.game_base import GameBase


class Showdown(GameBase):
    def __init__(self, players: Optional[List[Player_showdown]] = None):
        super().__init__(players=players, deck=Deck_showdown())
    
    def _turns_setup(self):
        return {"rounds": 13}

    def _player_take_turn(self, player):
        playable = player._hand._get_playable()
        card = player._take_turn(playable=playable)
        return {"card": card}

    def _after_round(self, plays):
        # plays: list of tuples (player, card)
        from app.models.showdown.round import Round

        # determine round winner and award point
        round_obj = Round(plays)
        round_obj._show_plays()
        winner = round_obj._determine_winner()
        winner._add_point(1)
        print(f"  Winner: {winner.name} (+1 point)\n")

    def _finalize(self):
        top = max(self.players, key=lambda pp: pp.point)
        print("Game over. Scores:")
        for p in self.players:
            print(f"  {p.name}: {p.point}")
        print(f"Overall winner: {top.name}")
