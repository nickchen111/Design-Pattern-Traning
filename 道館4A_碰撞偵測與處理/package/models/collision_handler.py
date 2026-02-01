from __future__ import annotations
from abc import abstractmethod
from typing import List, Optional
from .sprite import Sprite

# Action is a tuple like ("remove", sprite) or ("move", sprite, pos)
Action = tuple


class AbstractCollisionHandler:
    def __init__(self, nxt: Optional["AbstractCollisionHandler"] = None):
        self.next = nxt

    def _set_next(self, nxt: "AbstractCollisionHandler") -> "AbstractCollisionHandler":
        self.next = nxt
        return nxt

    def _handle(self, a: Sprite, b: Sprite) -> List[Action]:
        if self._can_handle(a, b): # template method
            return self._do_handle(a, b)
        if self.next:
            return self.next._handle(a, b)
        return []
    
    @abstractmethod
    def _can_handle(self, a: Sprite, b: Sprite) -> bool:
        raise NotImplementedError

    @abstractmethod
    def _do_handle(self, a: Sprite, b: Sprite) -> List[Action]:
        raise NotImplementedError


def build_chain(handlers: List[AbstractCollisionHandler]) -> Optional[AbstractCollisionHandler]:
    if not handlers:
        return None
    head = handlers[0]
    curr = head
    for h in handlers[1:]:
        curr._set_next(h)
        curr = h
    return head



_handlers_registry: dict[type, List[AbstractCollisionHandler]] = {}
_chain_cache: dict[type, AbstractCollisionHandler] = {}


def register_handlers_for(cls_type: type, handlers: List[AbstractCollisionHandler]) -> None:
    """Register a list of handler instances for a given Sprite class.

    Modules (e.g. hero.py, water.py) should call this once at import time.
    """
    _handlers_registry[cls_type] = handlers
    # invalidate cache for this class if previously built
    if cls_type in _chain_cache:
        del _chain_cache[cls_type]


def build_chain_for_class(cls_type: type) -> Optional[AbstractCollisionHandler]:
    """Build (but do not cache) a chain for the registered handlers of cls_type."""
    handlers = _handlers_registry.get(cls_type)
    if not handlers:
        return None
    return build_chain(handlers)


def get_chain_for_class(cls_type: type) -> Optional[AbstractCollisionHandler]:
    """Get a cached chain for cls_type, building and caching it on first access.

    If no handlers have been registered yet, attempt to lazily register the
    project's default handler sets. This deferred registration avoids
    import-time cycles when Sprite modules import this module.
    """
    # Ensure any default registrations are performed lazily
    _ensure_default_registrations()

    if cls_type in _chain_cache:
        return _chain_cache[cls_type]
    chain = build_chain_for_class(cls_type)
    if chain is not None:
        _chain_cache[cls_type] = chain
    return chain


def _ensure_default_registrations() -> None:
    """Perform lazy registration of the project's concrete handlers.

    This imports concrete Sprite classes and handler implementations and
    registers default handler lists for them. It is safe to call multiple
    times; registration only happens once when the registry is empty.
    """
    if _handlers_registry:
        return

    # Local imports to avoid top-level import cycles
    from .handlers import (
        WaterVsFireHandler,
        HeroVsFireHandler,
        HeroVsWaterHandler,
        SameTypeBlockerHandler,
    )

    try:
        from .hero import Hero
        from .water import Water
        from .fire import Fire
    except Exception:
        return

    register_handlers_for(Hero, [HeroVsFireHandler(), HeroVsWaterHandler(), SameTypeBlockerHandler()])
    register_handlers_for(Water, [WaterVsFireHandler(), SameTypeBlockerHandler()])
    register_handlers_for(Fire, [WaterVsFireHandler(), SameTypeBlockerHandler()])

