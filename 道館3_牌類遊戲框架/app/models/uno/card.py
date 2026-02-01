from pydantic import PrivateAttr
from enum import Enum
from typing import Union
from app.models.base.card import BaseCard


class Color(Enum):
    RED = "RED"
    BLUE = "BLUE"
    GREEN = "GREEN"
    YELLOW = "YELLOW"


class Number(Enum):
    V0 = "0"
    V1 = "1"
    V2 = "2"
    V3 = "3"
    V4 = "4"
    V5 = "5"
    V6 = "6"
    V7 = "7"
    V8 = "8"
    V9 = "9"

    @classmethod
    def values(cls):
        return [m.value for m in cls]


class Card_uno(BaseCard):
    _color: str = PrivateAttr()
    _number: str = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        self._repr_fields = ["color", "number"]

    @classmethod
    def create(cls, col: Union[Color, str], num: Union[Number, str]) -> "Card_uno":
        # accept either Enum members or raw strings
        if isinstance(col, Color):
            color_val = col.value
        else:
            try:
                color_val = Color[col.upper()].value
            except Exception:
                if col in [c.value for c in Color]:
                    color_val = col
                else:
                    raise ValueError(f"Invalid color: {col}. Valid: {[c.value for c in Color]}")

        if isinstance(num, Number):
            num_val = num.value
        else:
            if num in Number.values():
                num_val = num
            else:
                raise ValueError(f"Invalid number: {num}. Valid: {Number.values()}")

        inst = cls.model_construct()
        inst._color = color_val
        inst._number = num_val
        return inst

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, value: str) -> None:
        self._color = value

    @property
    def number(self) -> str:
        return self._number

    @number.setter
    def number(self, value: str) -> None:
        self._number = value

    def __str__(self) -> str:
        return f"{self.color} {self.number}"

    def __repr__(self) -> str:
        return f"Card_uno(color={self.color!r}, number={self.number!r})"

    def model_dump(self, *args, **kwargs):
        return super().model_dump(*args, **kwargs)