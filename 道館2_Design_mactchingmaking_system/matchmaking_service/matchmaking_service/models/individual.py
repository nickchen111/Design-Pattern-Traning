from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum


class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class Individual(BaseModel):
    id: int = Field(..., gt=0, description="Unique identifier (>0)")
    gender: Gender = Field(..., description="Gender: MALE or FEMALE")
    age: int = Field(..., ge=18, description="Age (>=18)")
    intro: str = Field(..., max_length=200)
    habits: str = Field("", description="Comma-separated habits, each 1..10 chars, e.g. 'basketball,cooking'")
    coord: List[int] = Field(..., min_items=2, max_items=2, description="Coordinate [x, y]")
    partner: Optional[int] = Field(None, description="Partner identifier (if matched)")

    def __init__(self, **data):
        super().__init__(**data)

    @validator("habits")
    def validate_habits(cls, v: str):
        if v is None:
            return ""
        parts = [h.strip() for h in v.split(",") if h.strip()]
        for h in parts:
            if not (1 <= len(h) <= 10):
                raise ValueError("Each habit must be 1..10 characters")
        return ",".join(parts)

    def _apply_strategy(self, strategy, candidates: List["Individual"]):
        """
        Apply a strategy. `strategy` must implement `rank(subject, candidates)`.
        """
        if not hasattr(strategy, "_rank"):
            raise ValueError("strategy must implement a rank(subject, candidates) method")

        ranked = strategy._rank(self, candidates)
        if ranked:
            self.partner = ranked[0].id
        return ranked

    @property
    def habits_list(self) -> List[str]:
        if not self.habits:
            return []
        return [h.strip() for h in self.habits.split(",") if h.strip()]

    # -- Read-only properties to enforce encapsulation externally --
    @property
    def _id(self) -> int:
        return self.id

    @property
    def _gender(self) -> Gender:
        return self.gender

    @property
    def _age(self) -> int:
        return self.age

    @property
    def _intro(self) -> str:
        return self.intro

    @property
    def _habits(self) -> List[str]:
        return list(self.habits_list)

    @property
    def _coord(self) -> List[int]:
        return list(self.coord)