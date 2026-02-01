from typing import List, Optional, Any
import sys
from abc import ABC, abstractmethod


class GameBase(ABC):
    def __init__(self, players: Optional[List[Any]] = None, deck: Optional[Any] = None):
        self._players = players or []
        self._deck = deck

    @property
    def players(self):
        return self._players
    
    @property
    def deck(self):
        return self._deck

    def _add_player(self, player: Any):
        self._players.append(player)

    def _start_game(self, per_player: int = 0):
        """Shared flow: name players, prepare deck, deal cards, then run post-deal hook."""
        ai_idx = 1
        human_idx = 1
        interactive = sys.stdin.isatty()

        for p in self._players:
            try:
                current_name = p.name
            except Exception:
                current_name = None

            if current_name:
                continue

            is_human = getattr(p, "__class__", None) and p.__class__.__name__.startswith("Human")
            if is_human:
                if interactive:
                    while True:
                        name = input(f"請輸入玩家名稱 (Player{human_idx}): ").strip()
                        if name:
                            p._name = name
                            break
                        p._name = f"Player{human_idx}"
                        break
                else:
                    p._name = f"Player{human_idx}"
                human_idx += 1
            else:
                p._name = f"AI{ai_idx}"
                ai_idx += 1

        if self._deck is not None:
            self._deck._cards = []
            self._deck._fill_standard()
            self._deck._shuffle()

            for _ in range(per_player):
                for p in self._players:
                    c = self._deck._draw_card()
                    if c:
                        p._hand._receive_card(c)

        self._post_deal_setup()

    def _post_deal_setup(self):
        """Hook for subclasses to run after dealing"""
        return None

    def _take_turns(self):
        """Template method for taking turns. Subclasses implement hooks below.

        Hooks to implement:
        - _turns_setup() -> context dict with 'rounds' key (None for infinite)
        - _player_take_turn(player, context) -> result dict
        - _after_player(player, result, context)
        - _after_round(plays, context) -> None
        - _check_end(context) -> bool
        - _finalize(context)
        """
        ctx = self._turns_setup()
        rounds = ctx.get("rounds")
        
        if rounds is not None:
            # Fixed number of rounds
            for r in range(1, rounds + 1):
                plays = []
                for p in self._players:
                    res = self._player_take_turn(p)
                    plays.append((p, res.get("card")))
                    self._after_player(p, res, ctx)
                self._after_round(plays)
        else:
            # Infinite rounds until _check_end returns True
            while True:
                for p in self._players:
                    res = self._player_take_turn(p, ctx)
                    self._after_player(p, res, ctx)
                    if self._check_end(ctx):
                        break
                if self._check_end(ctx):
                    break
        
        self._finalize()

    # Hook methods
    @abstractmethod
    def _turns_setup(self):
        """Return context dict with 'rounds' key (None for infinite)"""
        pass

    @abstractmethod
    def _player_take_turn(self, player, context):
        """Execute player's turn and return result dict with 'card' key"""
        pass

    def _after_player(self, player, result, context):
        """Hook after each player's turn"""
        return None

    def _after_round(self, plays, context):
        """Hook after all players have played in a round"""
        return None

    def _check_end(self, context):
        """Check if game should end (for infinite rounds mode)"""
        return False
    
    def _finalize(self):
        """Hook for game end logic"""
        return None
