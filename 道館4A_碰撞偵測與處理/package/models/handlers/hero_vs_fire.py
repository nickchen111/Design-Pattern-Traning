from typing import List
from ..collision_handler import AbstractCollisionHandler, Action
from ..sprite import Sprite


class HeroVsFireHandler(AbstractCollisionHandler):
    def _can_handle(self, a: Sprite, b: Sprite) -> bool:
        from ..hero import Hero
        from ..fire import Fire
        return (isinstance(a, Hero) and isinstance(b, Fire)) or (
            isinstance(a, Fire) and isinstance(b, Hero)
        )

    def _do_handle(self, a: Sprite, b: Sprite) -> List[Action]:
        from ..hero import Hero
        hero = a if isinstance(a, Hero) else b
        fire = b if hero is a else a
        died = hero._damage(10)
        actions = [("remove", fire)]
        if died:
            actions.append(("remove", hero))
        return actions
