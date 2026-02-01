from typing import List
from ..collision_handler import AbstractCollisionHandler, Action
from ..sprite import Sprite


class WaterVsFireHandler(AbstractCollisionHandler):
    def _can_handle(self, a: Sprite, b: Sprite) -> bool:
        from ..water import Water
        from ..fire import Fire
        return (isinstance(a, Water) and isinstance(b, Fire)) or (
            isinstance(a, Fire) and isinstance(b, Water)
        )

    def _do_handle(self, a: Sprite, b: Sprite) -> List[Action]:
        return [("remove", a), ("remove", b)]
