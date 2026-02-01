from pydantic import BaseModel, PrivateAttr
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .individual import Individual
    from matchmaking_service.matchmaking_service.models.strategies import MatchmakingStrategy

class MatchmakingSystem(BaseModel):
    __user_list: List[int] = PrivateAttr(default_factory=list)
    __id: int = PrivateAttr(0)

    def _ensure_registry(self):
        """Protected: 確保 registry 存在"""
        if not hasattr(self, "_registry"):
            object.__setattr__(self, "_registry", {})

    def register(self, individual: "Individual"):
        """Public: 外部註冊介面"""
        self._ensure_registry()
        self._registry[individual.id] = individual
        if individual.id not in self.__user_list:
            self.__user_list.append(individual.id)

    def __init__(self, **data):
        individuals = data.pop("individuals", None)
        super().__init__(**data)
        if individuals:
            for ind in individuals:
                self.register(ind)

    def _execute_strategies(self, strategy: "MatchmakingStrategy") -> None:
        self._ensure_registry()
        strat = strategy

        for uid, user in list(self._registry.items()):
            candidates = [self._registry[i] for i in self.__user_list if i in self._registry and i != uid]
            user._apply_strategy(strat, candidates)

    # --- dynamic APIs ---
    def _add_individuals(self, individuals: List["Individual"]):
        for ind in individuals:
            self.register(ind)

    @property
    def user_list(self):
        return self.__user_list

    class Config:
        schema_extra = {
            "example": {"id": 0}
        }