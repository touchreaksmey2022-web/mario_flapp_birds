"""
constants.py
============
All game-wide constants, colour definitions, and level configuration.

Nothing in this module has side-effects; it is safe to import anywhere.

Notes
-----
  * LEVEL_CONFIG drives every difficulty difference in the game:
    gravity, pipe speed, gap size, spawn interval, and which background
    asset to use.
  * LEVEL_ORDER defines the display/cycle order for the level-select screen.
"""

import os

# ── Screen ─────────────────────────────────────────────────────────────────────
GAME_WIDTH:  int = 360
GAME_HEIGHT: int = 640
FPS:         int = 60

# ── Paths ──────────────────────────────────────────────────────────────────────
ASSET_DIR:  str = os.path.join(os.path.dirname(__file__), "assets")
SCORE_FILE: str = os.path.join(os.path.dirname(__file__), "mario_scores.txt")

# ── Colours (R, G, B) ──────────────────────────────────────────────────────────
WHITE:  tuple[int, int, int] = (255, 255, 255)
BLACK:  tuple[int, int, int] = (0,   0,   0  )
RED:    tuple[int, int, int] = (200, 30,  30 )
YELLOW: tuple[int, int, int] = (255, 220, 0  )
BLUE:   tuple[int, int, int] = (30,  80,  200)
DARK:   tuple[int, int, int] = (20,  20,  40 )
GOLD:   tuple[int, int, int] = (255, 200, 0  )

# ── Sprite sizes ───────────────────────────────────────────────────────────────
PIPE_WIDTH:  int = 64
PIPE_HEIGHT: int = 512
BIRD_W:      int = 34
BIRD_H:      int = 40

# ── Level configuration ────────────────────────────────────────────────────────
LEVEL_CONFIG: dict[str, dict] = {
    "Easy": {
        "gravity":        0.25,
        "velocity_x":    -2,
        "jump_velocity":  -5.5,
        "gap":            220,      # pixels between top and bottom pipe openings
        "spawn_ms":       2000,     # milliseconds between pipe spawns
        "bg_asset":       "bg_easy.png",
        "label":          "🌿 Easy – Grass World",
    },
    "Medium": {
        "gravity":        0.35,
        "velocity_x":    -3,
        "jump_velocity":  -6.0,
        "gap":            180,
        "spawn_ms":       1600,
        "bg_asset":       "bg_medium.png",
        "label":          "🌑 Medium – Cave World",
    },
    "Hard": {
        "gravity":        0.50,
        "velocity_x":    -4,
        "jump_velocity":  -7.0,
        "gap":            140,
        "spawn_ms":       1200,
        "bg_asset":       "bg_hard.png",
        "label":          "🔥 Hard – Lava Castle",
    },
}

#: Display/cycle order for the level-select screen.
LEVEL_ORDER: list[str] = ["Easy", "Medium", "Hard"]

# ── Menu ───────────────────────────────────────────────────────────────────────
MENU_ITEMS:  list[str]       = ["Start", "Continue", "Level", "Sound", "Exit"]
SOUND_LABEL: dict[bool, str] = {True: "Sound: ON 🔊", False: "Sound: OFF 🔇"}
