from typing import List
from ..collision_handler import AbstractCollisionHandler, Action
from ..sprite import Sprite


class SameTypeBlockerHandler(AbstractCollisionHandler):
    def _can_handle(self, a: Sprite, b: Sprite) -> bool:
        return type(a) is type(b)

    def _do_handle(self, a: Sprite, b: Sprite) -> List[Action]:
        return []
