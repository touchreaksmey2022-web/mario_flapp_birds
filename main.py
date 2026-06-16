"""
main.py
=======
Entry point for Mario Flappy Bird.

Responsibilities
----------------
  * Initialise pygame and create the display window.
  * Load all assets (surfaces, fonts).
  * Own the top-level screen state-machine:
      "menu" → "level_select" → "playing" (→ game_over overlay) → back
  * Forward events to the appropriate handler (Menu, physics, etc.).
  * Manage the pipe-spawn timer and high-score updates.

Usage
-----
  python main.py

Notes
-----
  All game logic is in ``physics.py``.
  All rendering is in ``renderer.py`` and ``menu.py``.
  Constants are in ``constants.py``.
  Exceptions are in ``exceptions.py``.
  Asset I/O is in ``assets.py``.
  Data classes are in ``entities.py`` and ``state.py``.
"""

import sys

try:
    import pygame
except ImportError as exc:
    raise SystemExit(
        "pygame is required.  Install it with:  pip install pygame"
    ) from exc

from constants  import (
    GAME_WIDTH, GAME_HEIGHT, FPS,
    LEVEL_CONFIG, LEVEL_ORDER,
    PIPE_WIDTH, PIPE_HEIGHT, BIRD_W, BIRD_H,
)
from exceptions import AssetNotFoundError, SaveFileCorruptError
from assets     import asset_path, load_surface, load_scores, save_scores
from entities   import Bird
from state      import GameState
from physics    import create_pipes, update_physics
from renderer   import make_level_tag, draw_frame
from menu       import Menu, draw_level_select


# ══════════════════════════════════════════════════════════════════════════════
def main() -> None:
    """
    Initialise pygame, build all game objects, and run the main event loop.

    The loop drives a simple screen state-machine with three states:
      * ``"menu"``         – main menu rendered by ``Menu.draw``
      * ``"level_select"`` – level picker rendered by ``draw_level_select``
      * ``"playing"``      – gameplay rendered by ``draw_frame``
                             (the game-over overlay is part of ``draw_frame``)

    Returns
    -------
    None  (exits via ``sys.exit`` on Quit or Exit menu action)
    """

    # ── pygame setup ──────────────────────────────────────────────────────────
    pygame.init()
    pygame.display.set_caption("Mario Flappy Bird")

    try:
        icon = pygame.image.load(asset_path("mario.png"))
        pygame.display.set_icon(icon)
    except (AssetNotFoundError, pygame.error):
        pass   # icon is optional; silently continue without it

    window: pygame.Surface    = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    clock:  pygame.time.Clock = pygame.time.Clock()

    # ── Fonts ─────────────────────────────────────────────────────────────────
    try:
        font_big = pygame.font.SysFont("Arial", 40, bold=True)
        font_med = pygame.font.SysFont("Arial", 24)
    except Exception:
        font_big = pygame.font.Font(None, 40)
        font_med = pygame.font.Font(None, 24)

    # ── Load shared surfaces ──────────────────────────────────────────────────
    mario_surf = load_surface("mario.png",       (BIRD_W, BIRD_H))
    top_surf   = load_surface("top_pipe.png",    (PIPE_WIDTH, PIPE_HEIGHT))
    bot_surf   = load_surface("bottom_pipe.png", (PIPE_WIDTH, PIPE_HEIGHT))

    # ── Background cache (lazy, keyed by level name) ──────────────────────────
    bg_cache: dict[str, pygame.Surface] = {}

    def get_bg(level_name: str) -> pygame.Surface:
        """
        Return the cached background surface for *level_name*, loading it
        on first access.

        Arguments
        ---------
        level_name : str

        Returns
        -------
        pygame.Surface
        """
        if level_name not in bg_cache:
            asset_name          = LEVEL_CONFIG[level_name]["bg_asset"]
            bg_cache[level_name] = load_surface(asset_name, (GAME_WIDTH, GAME_HEIGHT))
        return bg_cache[level_name]

    # ── Persistent / session state ────────────────────────────────────────────
    try:
        high_scores: dict[str, int] = load_scores()
    except SaveFileCorruptError as exc:
        print(f"Warning – corrupt save file reset: {exc}")
        high_scores = {lvl: 0 for lvl in LEVEL_ORDER}

    current_level: str            = "Easy"
    sound_on:      bool           = True
    saved_state:   GameState | None = None   # snapshot kept for "Continue"

    # ── Game objects ──────────────────────────────────────────────────────────
    bird  = Bird(mario_surf)
    state = GameState(current_level)

    level_tag = make_level_tag(font_med, current_level)

    # ── Pipe-spawn timer ──────────────────────────────────────────────────────
    CREATE_PIPES_EVENT: int = pygame.USEREVENT + 1

    def set_pipe_timer(level_name: str) -> None:
        """
        (Re)start the recurring pipe-spawn timer for *level_name*.

        Arguments
        ---------
        level_name : str
        """
        pygame.time.set_timer(
            CREATE_PIPES_EVENT,
            LEVEL_CONFIG[level_name]["spawn_ms"],
        )

    set_pipe_timer(current_level)

    # ── Screen state-machine ──────────────────────────────────────────────────
    screen:     str = "menu"
    lvl_cursor: int = LEVEL_ORDER.index(current_level)
    menu            = Menu(window, font_big, font_med)

    # ══════════════════════════════════════════════════════════════════════════
    # Main loop
    # ══════════════════════════════════════════════════════════════════════════
    while True:
        bg = get_bg(current_level)

        # ── Events ────────────────────────────────────────────────────────────
        for event in pygame.event.get():

            # Window close button
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            # Timed pipe spawn
            if (event.type == CREATE_PIPES_EVENT
                    and screen == "playing"
                    and not state.game_over):
                create_pipes(state, top_surf, bot_surf)

            if event.type == pygame.KEYDOWN:

                # ── ESC: back to menu from anywhere ───────────────────────────
                if event.key == pygame.K_ESCAPE:
                    if screen in ("playing", "paused"):
                        if not state.game_over:
                            saved_state = state   # preserve for Continue
                        screen = "menu"
                    elif screen == "level_select":
                        screen = "menu"

                # ── Main menu ─────────────────────────────────────────────────
                elif screen == "menu":
                    action = menu.handle_key(event.key)

                    if action == "Start":
                        state       = GameState(current_level)
                        saved_state = None
                        bird.reset()
                        set_pipe_timer(current_level)
                        screen = "playing"

                    elif action == "Continue":
                        if saved_state is not None:
                            state  = saved_state
                            screen = "playing"
                        # else: nothing to continue – silently ignore

                    elif action == "Level":
                        lvl_cursor = LEVEL_ORDER.index(current_level)
                        screen     = "level_select"

                    elif action == "Sound":
                        sound_on = not sound_on
                        # Wire real audio here when adding SFX/music

                    elif action == "Exit":
                        pygame.quit()
                        sys.exit(0)

                # ── Level select ──────────────────────────────────────────────
                elif screen == "level_select":
                    if event.key == pygame.K_UP:
                        lvl_cursor = (lvl_cursor - 1) % len(LEVEL_ORDER)
                    elif event.key == pygame.K_DOWN:
                        lvl_cursor = (lvl_cursor + 1) % len(LEVEL_ORDER)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        current_level = LEVEL_ORDER[lvl_cursor]
                        level_tag     = make_level_tag(font_med, current_level)
                        set_pipe_timer(current_level)
                        saved_state   = None   # old save belongs to old level
                        screen        = "menu"

                # ── Playing / game-over ───────────────────────────────────────
                elif screen == "playing":
                    jump_keys = (pygame.K_SPACE, pygame.K_UP, pygame.K_x)
                    if event.key in jump_keys:
                        if state.game_over:
                            # Persist best score, then restart
                            final = int(state.score)
                            if final > high_scores.get(current_level, 0):
                                high_scores[current_level] = final
                                save_scores(high_scores)
                            state = GameState(current_level)
                            bird.reset()
                        else:
                            state.velocity_y = LEVEL_CONFIG[current_level]["jump_velocity"]

        # ── Update ────────────────────────────────────────────────────────────
        if screen == "playing" and not state.game_over:
            update_physics(state, bird)
            # Keep high score live during play
            live = int(state.score)
            if live > high_scores.get(current_level, 0):
                high_scores[current_level] = live

        # ── Draw ──────────────────────────────────────────────────────────────
        if screen == "menu":
            menu.draw(
                bg, current_level, sound_on, high_scores,
                has_saved_game=(saved_state is not None),
            )
        elif screen == "level_select":
            draw_level_select(
                window, current_level, lvl_cursor, font_big, font_med, bg
            )
        elif screen == "playing":
            draw_frame(window, bg, state, bird, font_big, font_med, level_tag)

        pygame.display.update()
        clock.tick(FPS)


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    main()
