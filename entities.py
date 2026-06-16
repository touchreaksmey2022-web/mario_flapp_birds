"""
entities.py
===========
Game-object classes: ``Bird`` (player) and ``Pipe`` (obstacle).

Both classes extend ``pygame.Rect`` so they integrate naturally with pygame's
collision and drawing APIs.

Notes
-----
  Import order: this module must be imported after ``pygame.init()`` has been
  called because ``pygame.Rect`` is a C-extension type.
"""

import pygame
from constants import GAME_WIDTH, GAME_HEIGHT, BIRD_W, BIRD_H, PIPE_WIDTH, PIPE_HEIGHT


class Bird(pygame.Rect):
    """
    Player-controlled Mario character sprite.

    Inherits from ``pygame.Rect`` to support ``colliderect`` checks directly.
    Positional data (x, y, width, height) lives in the Rect; the RGBA surface
    is stored separately in ``self.img``.

    Arguments
    ---------
    img : pygame.Surface
        Pre-loaded and pre-scaled RGBA surface for the character sprite.

    Attributes
    ----------
    img : pygame.Surface
        The character image rendered each frame.

    Notes
    -----
      Call ``reset()`` whenever starting a new game to return the bird to its
      initial position without re-allocating the object.
    """

    def __init__(self, img: pygame.Surface) -> None:
        super().__init__(GAME_WIDTH // 8, GAME_HEIGHT // 2, BIRD_W, BIRD_H)
        self.img: pygame.Surface = img

    def reset(self) -> None:
        """
        Return the bird to its default starting position.

        Notes
        -----
          Does not reset velocity – the caller (``GameState.reset``) is
          responsible for zeroing ``velocity_y``.
        """
        self.x = GAME_WIDTH // 8
        self.y = GAME_HEIGHT // 2


class Pipe(pygame.Rect):
    """
    A single scrolling pipe obstacle.

    Inherits from ``pygame.Rect``; pipe pairs (top + bottom) are managed as
    separate ``Pipe`` instances stored in ``GameState.pipes``.

    Arguments
    ---------
    img : pygame.Surface
        Pre-loaded RGBA surface (either the top-pipe or bottom-pipe image).
    x   : int
        Initial horizontal pixel position (typically ``GAME_WIDTH``).
    y   : int
        Initial vertical pixel position (may be negative for top pipes).

    Attributes
    ----------
    img    : pygame.Surface
        The pipe image rendered each frame.
    passed : bool
        Set to ``True`` once the bird's left edge has passed the pipe's right
        edge; used to award exactly one score-point per pipe pair.
    """

    def __init__(self, img: pygame.Surface, x: int, y: int) -> None:
        super().__init__(x, y, PIPE_WIDTH, PIPE_HEIGHT)
        self.img:    pygame.Surface = img
        self.passed: bool           = False
