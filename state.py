"""
state.py
========
``GameState`` encapsulates every piece of mutable data for one play session:
physics velocity, current score, pipe list, and game-over flag.

Separating state from rendering and input logic keeps ``main.py`` lean and
makes it straightforward to implement the "Continue" feature (just keep a
reference to a ``GameState`` instance while on the menu).

Notes
-----
  ``GameState`` does **not** hold pygame Surfaces or fonts; those belong to
  the rendering layer (``renderer.py`` / ``menu.py``).
"""

from __future__ import annotations

from constants  import LEVEL_CONFIG, LEVEL_ORDER
from exceptions import InvalidLevelError
from entities   import Bird, Pipe


class GameState:
    """
    All mutable runtime data for a single play session.

    Arguments
    ---------
    level_name : str
        One of ``'Easy'``, ``'Medium'``, ``'Hard'``.

    Attributes
    ----------
    level_name : str
        Active level key.
    cfg        : dict
        Reference to the level's entry in ``LEVEL_CONFIG``.
    velocity_y : float
        Vertical velocity applied to the bird each physics tick.
    score      : float
        Accumulated score (incremented by 0.5 per pipe passed; two pipes
        per pair = +1 per opening cleared).
    game_over  : bool
        ``True`` once the bird hits a pipe or the floor.
    pipes      : list[Pipe]
        All live ``Pipe`` instances currently on screen.

    Raises
    ------
    InvalidLevelError
        If *level_name* is not present in ``LEVEL_CONFIG``.

    Notes
    -----
      Call ``reset(bird)`` to restart within the same level without
      constructing a new ``GameState``.

    Example
    -------
    >>> state = GameState("Easy")
    >>> state.score
    0.0
    >>> state.game_over
    False
    """

    def __init__(self, level_name: str) -> None:
        if level_name not in LEVEL_CONFIG:
            raise InvalidLevelError(level_name, LEVEL_ORDER)

        self.level_name: str        = level_name
        self.cfg:        dict       = LEVEL_CONFIG[level_name]
        self.velocity_y: float      = 0.0
        self.score:      float      = 0.0
        self.game_over:  bool       = False
        self.pipes:      list[Pipe] = []

    def reset(self, bird: Bird) -> None:
        """
        Reset physics, clear pipes, and reposition the bird.

        Arguments
        ---------
        bird : Bird
            The player object whose position will be reset.

        Notes
        -----
          ``level_name`` and ``cfg`` are intentionally preserved so the same
          ``GameState`` object can be reused for multiple rounds on the same
          level.
        """
        self.velocity_y = 0.0
        self.score      = 0.0
        self.game_over  = False
        self.pipes.clear()
        bird.reset()
