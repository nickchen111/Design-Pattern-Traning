from typing import List, Optional
from pydantic import BaseModel, PrivateAttr
from .sprite import Sprite

class World(BaseModel):
    _length_obj: int = PrivateAttr(30)
    _sprites_obj: List[Sprite] = PrivateAttr(default_factory=list)

    def __init__(self, length: int = 30, **data):
        super().__init__(**data)
        object.__setattr__(self, "_length_obj", int(length))
        object.__setattr__(self, "_sprites_obj", [])

    @property
    def _length(self) -> int:
        return self._length_obj

    @_length.setter
    def _length(self, value: int) -> None:
        v = int(value)
        if v <= 0:
            raise ValueError("Length must be a positive integer")
        object.__setattr__(self, "_length_obj", v)

    @property
    def _sprites(self) -> List[Sprite]:
        return self._sprites_obj

    @_sprites.setter
    def _sprites(self, value: List[Sprite]) -> None:
        object.__setattr__(self, "_sprites_obj", list(value))

    def _create(self, sprites: List[Sprite]) -> None:
        if len(sprites) < 10:
            raise ValueError("There must be at least 10 sprites to create the world")
        self._sprites = sprites

    def _find_sprite_at(self, pos: int, exclude: Optional[Sprite] = None):
        """Return a sprite at position `pos`, or None. If `exclude` is provided,
        that sprite will be ignored (useful to avoid detecting the mover itself).
        """
        for s in self._sprites:
            if exclude is not None and s is exclude:
                continue
            if s._position() == pos:
                return s
        return None

    def _display_sprites(self) -> None:
        """Display all sprites with their indices and positions."""
        for idx, s in enumerate(self._sprites):
            print(f"{idx}: {s.__class__.__name__} at {s._position()}")

    def _get_sprite_selection(self) -> Optional[int]:
        """Get user's sprite selection. Returns sprite index or None if quitting."""
        sel = input("Select sprite index to move (or 'q' to quit): ")
        if sel.strip().lower() == "q":
            return None
        try:
            sel_idx = int(sel)
            if not (0 <= sel_idx < len(self._sprites)):
                print("invalid move: index out of range")
                return -1  # Invalid selection
            return sel_idx
        except ValueError:
            print("invalid move: not an integer")
            return -1  # Invalid selection

    def _get_destination(self) -> Optional[int]:
        """Get user's destination position. Returns position or None if invalid."""
        dest = input(f"Enter destination position (0 <= pos <= {self._length - 1}): ")
        try:
            dest_pos = int(dest)
            if not (0 <= dest_pos <= self._length - 1):
                print("invalid move: destination out of range")
                return None
            return dest_pos
        except ValueError:
            print("invalid move: not an integer")
            return None

    def _collect_collision_actions(self, sprite1: Sprite, sprite2: Sprite) -> List:
        """Collect collision actions from both sprites involved in collision."""
        actions1 = []
        actions2 = []
        if hasattr(sprite1, "_on_collision"):
            actions1 = sprite1._on_collision(sprite2) or []
        if hasattr(sprite2, "_on_collision"):
            actions2 = sprite2._on_collision(sprite1) or []

        # Merge actions while preserving order and uniqueness
        actions = []
        for a in actions1 + actions2:
            if a not in actions:
                actions.append(a)
        return actions

    def _apply_collision_actions(self, actions: List) -> List[Sprite]:
        """Apply collision actions and return list of removed sprites."""
        removed = []
        for act in actions:
            if act[0] == "remove":
                _, sprite_to_remove = act
                if any(s is sprite_to_remove for s in self._sprites) and not any(r is sprite_to_remove for r in removed):
                    print(f"Removing {sprite_to_remove.__class__.__name__}")
                    self._sprites = [s for s in self._sprites if s is not sprite_to_remove]
                    removed.append(sprite_to_remove)
            elif act[0] == "move":
                _, sprite_to_move, pos = act
                if any(s is sprite_to_move for s in self._sprites) and not any(r is sprite_to_move for r in removed):
                    sprite_to_move._move_to(pos)
        return removed

    def _handle_collision(self, moving: Sprite, target: Sprite, dest_pos: int) -> bool:
        """
        Handle collision between moving sprite and target sprite.
        Returns True if movement should proceed, False otherwise.
        """
        src_pos = moving._position()
        print(f"Collision: {moving.__class__.__name__} ({src_pos} -> {dest_pos}) with {target.__class__.__name__} at {dest_pos}")

        # Collect actions from both sprites
        actions = self._collect_collision_actions(moving, target)

        # If no handler produced any actions, treat the collision as blocking
        if not actions:
            print("Move blocked: collision unresolved, movement cancelled")
            return False

        # Apply actions
        removed = self._apply_collision_actions(actions)

        # If moving sprite was removed, don't move it
        if moving in removed:
            return False

        return True

    def _start_loop(self) -> None:
        """
        Main interactive loop for sprite movement and collision handling.
        Repeatedly displays sprites, gets user input, and processes movement/collisions.
        """
        print("Starting interactive loop. Enter 'q' to quit.")
        while True:
            # Display all sprites
            self._display_sprites()

            # Get sprite selection
            sel_idx = self._get_sprite_selection()
            if sel_idx is None:
                print("Exiting loop")
                break
            if sel_idx == -1:
                continue  # Invalid selection, try again

            # Get destination position
            dest_pos = self._get_destination()
            if dest_pos is None:
                continue  # Invalid destination, try again

            moving = self._sprites[sel_idx]
            src_pos = moving._position()

            # Handle no-op move
            if dest_pos == src_pos:
                print(f"No-op move: {moving.__class__.__name__} already at {dest_pos}")
                continue

            # Check for collision
            target_sprite = self._find_sprite_at(dest_pos, exclude=moving)
            if target_sprite is None:
                # No collision, move directly
                print(f"Moving {moving.__class__.__name__} from {src_pos} to {dest_pos}")
                moving._move_to(dest_pos)
                continue

            # Handle collision
            should_move = self._handle_collision(moving, target_sprite, dest_pos)
            if should_move and moving in self._sprites:
                moving._move_to(dest_pos)
