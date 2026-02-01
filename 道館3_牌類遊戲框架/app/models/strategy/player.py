from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.base.player import BasePlayer
    from app.models.base.card import BaseCard


class PlayerStrategy(ABC):
    @abstractmethod
    def choose_card(self, player: "BasePlayer", playable: List["BaseCard"], **kwargs) -> Optional["BaseCard"]:
        pass


class HumanStrategy(PlayerStrategy):
    def __init__(self, format_card=None):
        self.format_card = format_card or (lambda c: str(c))

    def choose_card(self, player: "BasePlayer", playable: List["BaseCard"], **kwargs) -> Optional[Any]:
        # show playable for debug
        print("playable cards:", playable)
        print(f"{player.name}, it's your turn. Your hand:")
        display_list = list(player.hand)
        for idx, card in enumerate(display_list):
            mark = " (可出)" if card in playable else ""
            print(f"{idx}: {self.format_card(card)}{mark}")

        while True:
            choice = input("Select a card to play by number (or 'pass' to skip): ").strip()
            if choice.lower() == 'pass':
                if playable:
                    print("You have playable cards and cannot pass. Choose a card.")
                    continue
                return None
            if choice.isdigit():
                sel_idx = int(choice)
                if 0 <= sel_idx < len(display_list):
                    selected = display_list[sel_idx]
                    if selected in playable:
                        player.hand._remove(selected)
                        return selected
            print("Invalid choice. Please try again.")


class RandomAIStrategy(PlayerStrategy):
    def choose_card(self, player: "BasePlayer", playable: List["BaseCard"], **kwargs) -> Optional["BaseCard"]:
        if not playable:
            return None
        import random
        card = random.choice(playable)
        try:
            player.hand._remove(card)
        except Exception:
            pass
        return card
