from .sprite import Sprite
from .coord import Coord
from pydantic import PrivateAttr


class Hero(Sprite):
    _hp_val: int = PrivateAttr(30)

    def __init__(self, coord: Coord, hp: int = 30, **data):
        super().__init__(coord=coord, **data)
        object.__setattr__(self, "_hp_val", int(hp))

    @property
    def _hp(self) -> int:
        return self._hp_val

    @_hp.setter
    def _hp(self, value: int) -> None:
        v = int(value)
        object.__setattr__(self, "_hp_val", v)

    def _is_dead(self) -> bool:
        return self._hp_val <= 0

    def _damage(self, amount: int) -> bool:
        """Apply damage to hero. Returns True if hero died."""
        self._hp = self._hp - int(amount)
        return self._hp <= 0

    def _heal(self, amount: int) -> None:
        self._hp += int(amount)
