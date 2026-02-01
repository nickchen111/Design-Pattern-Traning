from pydantic import BaseModel, PrivateAttr
from .coord import Coord
from typing import Optional


class Sprite(BaseModel):
    _coord_obj: Coord = PrivateAttr()

    def __init__(self, coord: Optional[Coord] = None, **data):
        super().__init__(**data)
        object.__setattr__(self, "_coord_obj", coord)

    @property
    def _coord(self) -> Coord:
        return self._coord_obj

    @_coord.setter
    def _coord(self, value: Coord) -> None:
        if not isinstance(value, Coord):
            raise TypeError("coord must be Coord instance")
        object.__setattr__(self, "_coord_obj", value)

    def _get_chain(self):
        from package.models.collision_handler import get_chain_for_class
        return get_chain_for_class(type(self))
    
    def _on_collision(self, other: "Sprite") -> list:
        chain = self._get_chain()
        if chain is None:
            return []
        return chain._handle(self, other)

    # Protected convenience methods to encapsulate coord access
    def _position(self) -> int:
        return self._coord._pos

    def _move_to(self, new_pos: int) -> None:
        self._coord._pos = new_pos

