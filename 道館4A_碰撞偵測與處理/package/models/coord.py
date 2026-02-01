from pydantic import BaseModel, PrivateAttr


class Coord(BaseModel):
    _pos_val: int = PrivateAttr(0)

    def __init__(self, pos: int = 0, **data):
        super().__init__(**data)
        object.__setattr__(self, "_pos_val", int(pos))

    @property
    def _pos(self) -> int:
        return self._pos_val

    @_pos.setter
    def _pos(self, value: int) -> None:
        v = int(value)
        if not (0 <= v <= 29):
            raise ValueError("pos must be between 0 and 29")
        object.__setattr__(self, "_pos_val", v)