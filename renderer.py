"""
renderer.py
===========
All in-game rendering functions (gameplay frame + game-over overlay).

Menu rendering lives in ``menu.py``; only the active play screen is here.

Functions
---------
make_level_tag(font, level_name)            – build the HUD level-badge surface
draw_frame(window, bg, state, bird, ...)    – render one gameplay frame
draw_game_over(window, state, font_big, font_med) – semi-transparent death screen

Notes
-----
  None of these functions mutate game state – they are read-only consumers
  of ``GameState`` and ``Bird``.
"""

import pygame

from constants import GAME_WIDTH, GAME_HEIGHT, WHITE, BLACK, RED, YELLOW, GOLD
from entities  import Bird
from state     import GameState


def make_level_tag(font: pygame.font.Font, level_name: str) -> pygame.Surface:
    """
    Build the small HUD badge that displays the active level name.

    Arguments
    ---------
    font       : pygame.font.Font
        Medium-sized font used to render the label text.
    level_name : str
        E.g. ``'Easy'``, ``'Medium'``, or ``'Hard'``.

    Returns
    -------
    pygame.Surface
        A pre-rendered RGBA surface with a dark semi-transparent background
        behind the gold text.  Re-create whenever the level changes.

    Notes
    -----
      The returned surface is cached by the caller and re-used every frame,
      so this function is only called once per level change, not every tick.
    """
    text_surf = font.render(level_name, True, GOLD)
    w, h      = text_surf.get_size()
    badge     = pygame.Surface((w + 12, h + 6), pygame.SRCALPHA)
    badge.fill((0, 0, 0, 120))
    badge.blit(text_surf, (6, 3))
    return badge


def draw_frame(
    window:    pygame.Surface,
    bg:        pygame.Surface,
    state:     GameState,
    bird:      Bird,
    font_big:  pygame.font.Font,
    font_med:  pygame.font.Font,
    level_tag: pygame.Surface,
) -> None:
    """
    Render a complete gameplay frame to *window*.

    Drawing order (painter's algorithm):

    1. Background
    2. Pipes
    3. Bird (Mario)
    4. HUD: level badge (top-right) + score (top-left, with drop-shadow)
    5. Game-over overlay (if ``state.game_over`` is True)

    Arguments
    ---------
    window    : pygame.Surface
        The display surface (render target).
    bg        : pygame.Surface
        Full-screen background for the current level.
    state     : GameState
        Read to obtain pipe positions, score, and game_over flag.
    bird      : Bird
        Player sprite; position taken from ``bird.x / bird.y``.
    font_big  : pygame.font.Font
        Large font for score and game-over title.
    font_med  : pygame.font.Font
        Medium font for hints and sub-text.
    level_tag : pygame.Surface
        Pre-rendered level badge (see ``make_level_tag``).
    """
    # 1. Background
    window.blit(bg, (0, 0))

    # 2. Pipes
    for pipe in state.pipes:
        window.blit(pipe.img, pipe)

    # 3. Bird
    window.blit(bird.img, bird)

    # 4. HUD
    window.blit(level_tag, (GAME_WIDTH - level_tag.get_width() - 8, 8))

    if state.game_over:
        # 5. Game-over overlay replaces score display
        draw_game_over(window, state, font_big, font_med)
    else:
        score_text = str(int(state.score))
        shadow     = font_big.render(score_text, True, BLACK)
        score_surf = font_big.render(score_text, True, WHITE)
        window.blit(shadow,     (12, 12))   # drop-shadow offset
        window.blit(score_surf, (10, 10))


def draw_game_over(
    window:   pygame.Surface,
    state:    GameState,
    font_big: pygame.font.Font,
    font_med: pygame.font.Font,
) -> None:
    """
    Draw the semi-transparent game-over overlay on top of the last frame.

    Contents:
      - Dark translucent full-screen panel
      - "GAME OVER" title in red
      - Final score in white
      - Restart / menu hint in yellow

    Arguments
    ---------
    window   : pygame.Surface
        Render target (written on top of whatever was drawn last).
    state    : GameState
        Used to read ``state.score`` for the final-score display.
    font_big : pygame.font.Font
        Large font for the "GAME OVER" heading.
    font_med : pygame.font.Font
        Medium font for score and hint text.

    Notes
    -----
      This function uses ``pygame.SRCALPHA`` for the overlay so the last
      gameplay frame is still dimly visible behind the text.
    """
    overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    window.blit(overlay, (0, 0))

    cx = GAME_WIDTH // 2

    title = font_big.render("GAME OVER", True, RED)
    score = font_med.render(f"Score: {int(state.score)}", True, WHITE)
    hint  = font_med.render("SPACE to retry   ESC for menu", True, YELLOW)

    window.blit(title, (cx - title.get_width() // 2, 220))
    window.blit(score, (cx - score.get_width() // 2, 290))
    window.blit(hint,  (cx - hint.get_width()  // 2, 350))
