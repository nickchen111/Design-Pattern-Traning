from typing import List
from ..collision_handler import AbstractCollisionHandler, Action
from ..sprite import Sprite


class HeroVsWaterHandler(AbstractCollisionHandler):
    def _can_handle(self, a: Sprite, b: Sprite) -> bool:
        from ..hero import Hero
        from ..water import Water
        return (isinstance(a, Hero) and isinstance(b, Water)) or (
            isinstance(a, Water) and isinstance(b, Hero)
        )

    def _do_handle(self, a: Sprite, b: Sprite) -> List[Action]:
        from ..hero import Hero
        hero = a if isinstance(a, Hero) else b
        hero._heal(10)
        other = b if hero is a else a
        return [("remove", other)]
