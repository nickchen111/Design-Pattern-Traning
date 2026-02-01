from typing import List, Optional
from app.models.uno.deck import Deck_uno
from app.models.uno.player import Player_uno
from app.models.base.game_base import GameBase


class Uno(GameBase):
    def __init__(self, players: Optional[List[Player_uno]] = None):
        super().__init__(players=players, deck=Deck_uno())

    def _post_deal_setup(self):
        # flip one card to start the table and put it in discard
        if self._deck is None:
            return None
        top = self._deck._draw_card()
        if top:
            self._deck._discard_card(top)
    def _turns_setup(self):
        # Uno uses infinite rounds until someone wins
        top_card = self._deck._flip_card()
        print(f"遊戲開始！檯面上的第一張牌是: {top_card}")
        return {"rounds": None, "top_card": top_card, "ended": False}

    def _player_take_turn(self, player, context):
        top_card = context.get("top_card")
        playable = player._hand._get_playable(top_card)
        played = player._take_turn(playable=playable, top_card=top_card)
        return {"card": played}

    def _after_player(self, player, result, context):
        card = result.get("card")
        if card:
            self._deck._discard_card(card)
            context["top_card"] = card
            print(f"{player.name} 出了 {card}，現在檯面上的牌是: {context['top_card']}")
            if len(player._hand) == 0:
                context["ended"] = True
        else:
            print(f"{player.name} 無法出牌，跳過此回合。")
            drawn_card = self._deck._draw_card()
            if drawn_card is None:
                self._deck._refill_from_discard(latest_card=context.get("top_card"))
                drawn_card = self._deck._draw_card()
            player._hand._receive_card(drawn_card)
            print(f"{player.name} 從牌堆抽了一張牌: {drawn_card}")

    def _check_end(self, context):
        return context.get("ended", False)

    def _finalize(self):
        # find winner (player with empty hand)
        winner = None
        for p in self._players:
            if len(p._hand) == 0:
                winner = p
                break
        if winner:
            print(f"{winner.name} 已經沒有牌了，遊戲結束！")