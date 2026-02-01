from __future__ import annotations
from abc import ABC, abstractmethod
from pydantic import BaseModel, PrivateAttr
from typing import Any


class BaseCard(BaseModel, ABC):
    _repr_fields: list[str] = PrivateAttr(default_factory=list)

    @classmethod
    @abstractmethod
    def create(cls, *args: Any, **kwargs: Any) -> "BaseCard":
        ...

    def model_dump(self, *args, **kwargs):
        data = {}
        for f in self._repr_fields:
            val = getattr(self, f, None)
            data[f] = val
        return data

