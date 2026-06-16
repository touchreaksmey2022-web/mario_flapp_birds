"""
physics.py
==========
Core game-logic functions: pipe spawning, physics integration, and
collision detection.

All functions are pure with respect to pygame rendering – they mutate
``GameState`` and ``Bird`` but never touch a ``Surface`` or the display.
This makes them straightforward to unit-test without a display.

Functions
---------
create_pipes(state, top_img, bot_img)  – spawn a new pipe pair
update_physics(state, bird)            – apply gravity, move objects, check collisions

Notes
-----
  Score is incremented by 0.5 per pipe object passed; because each gap
  consists of two ``Pipe`` objects (top + bottom), the player gains exactly
  +1 per opening cleared.
"""

import math
import random

import pygame

from constants import GAME_WIDTH, GAME_HEIGHT, PIPE_WIDTH, PIPE_HEIGHT
from entities  import Bird, Pipe
from state     import GameState


def create_pipes(
    state:   GameState,
    top_img: pygame.Surface,
    bot_img: pygame.Surface,
) -> None:
    """
    Spawn a new top/bottom pipe pair at the right edge of the screen.

    The vertical gap centre is chosen randomly so that the opening always
    sits between 25 % and 75 % of the screen height, keeping the game fair
    on every difficulty.

    Arguments
    ---------
    state   : GameState
        Current session – the two new ``Pipe`` objects are appended to
        ``state.pipes`` in-place.
    top_img : pygame.Surface
        Surface for the top (downward-facing) pipe.
    bot_img : pygame.Surface
        Surface for the bottom (upward-facing) pipe.

    Notes
    -----
      The gap width is read from ``state.cfg["gap"]`` so it automatically
      reflects the current difficulty level.
    """
    gap: int = state.cfg["gap"]

    gap_centre: int = random.randint(
        int(GAME_HEIGHT * 0.25),
        int(GAME_HEIGHT * 0.75),
    )

    top_y: int = gap_centre - PIPE_HEIGHT - gap // 2
    bot_y: int = gap_centre + gap // 2

    state.pipes.append(Pipe(top_img, GAME_WIDTH, top_y))
    state.pipes.append(Pipe(bot_img, GAME_WIDTH, bot_y))


def update_physics(state: GameState, bird: Bird) -> None:
    """
    Advance the simulation by one frame.

    Actions performed (in order):

    1. Apply gravity to ``state.velocity_y``.
    2. Move the bird vertically; clamp to ceiling.
    3. Detect floor collision → ``state.game_over = True``.
    4. Scroll all pipes left by ``cfg["velocity_x"]``.
    5. Award score for each pipe whose right edge the bird passes.
    6. Detect bird–pipe collision → ``state.game_over = True``.
    7. Prune pipes that have scrolled entirely off-screen (left side).

    Arguments
    ---------
    state : GameState
        Mutable session data (modified in-place).
    bird  : Bird
        Player rect (x/y modified in-place).

    Notes
    -----
      The function returns immediately after setting ``game_over`` so the
      caller does not need to guard against further mutation in the same
      tick.
    """
    cfg = state.cfg

    # ── 1 & 2: gravity + bird movement ───────────────────────────────────────
    state.velocity_y += cfg["gravity"]
    bird.y           += math.floor(state.velocity_y)

    # ── Ceiling clamp ─────────────────────────────────────────────────────────
    if bird.y < 0:
        bird.y = 0

    # ── 3: floor collision ────────────────────────────────────────────────────
    if bird.y + bird.height > GAME_HEIGHT:
        state.game_over = True
        return

    vx: int = cfg["velocity_x"]

    # ── 4–6: pipe scroll, scoring, collision ──────────────────────────────────
    for pipe in state.pipes:
        pipe.x += vx

        if not pipe.passed and bird.x > pipe.x + pipe.width:
            state.score += 0.5   # two pipes per pair → +1 total
            pipe.passed  = True

        if bird.colliderect(pipe):
            state.game_over = True
            return

    # ── 7: prune off-screen pipes ─────────────────────────────────────────────
    while state.pipes and state.pipes[0].x < -PIPE_WIDTH:
        state.pipes.pop(0)
