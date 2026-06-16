# Mario Flappy Bird 🍄

A Super Mario–themed **Flappy Bird** remake built with **Python + pygame**.

---

## Project Structure

```
mario_flappy/
│
├── main.py               ← Entry point & game loop / screen state-machine
├── constants.py          ← All constants, colours, level config
├── exceptions.py         ← Custom exception hierarchy
├── entities.py           ← Bird and Pipe sprite classes (extend pygame.Rect)
├── state.py              ← GameState (mutable session data)
├── physics.py            ← Pipe spawning, gravity, collision detection
├── renderer.py           ← In-game frame drawing (gameplay + game-over)
├── menu.py               ← Main menu + level-select screen
├── assets.py             ← Asset loading & score persistence helpers
│
├── generate_assets.py    ← PIL script – generates all PNG files (run once)
│
├── assets/
│   ├── mario.png         ← Player sprite
│   ├── top_pipe.png      ← Top (downward) pipe
│   ├── bottom_pipe.png   ← Bottom (upward) pipe
│   ├── bg_easy.png       ← 🌿 Grass World background
│   ├── bg_medium.png     ← 🌑 Cave World background
│   └── bg_hard.png       ← 🔥 Lava Castle background
│
└── mario_scores.txt      ← Auto-created JSON high-score file
```

---

## Module Responsibilities

| File | Responsibility |
|---|---|
| `main.py` | pygame init, asset loading, event loop, screen state-machine |
| `constants.py` | Screen size, FPS, colours, LEVEL_CONFIG, MENU_ITEMS |
| `exceptions.py` | `MarioFlappyError`, `AssetNotFoundError`, `InvalidLevelError`, `SaveFileCorruptError` |
| `entities.py` | `Bird(pygame.Rect)` and `Pipe(pygame.Rect)` data classes |
| `state.py` | `GameState` – velocity, score, pipe list, game_over flag |
| `physics.py` | `create_pipes()`, `update_physics()` – pure logic, no rendering |
| `renderer.py` | `draw_frame()`, `draw_game_over()`, `make_level_tag()` |
| `menu.py` | `Menu` class + `draw_level_select()` standalone function |
| `assets.py` | `asset_path()`, `load_surface()`, `load_scores()`, `save_scores()` |

---

## Requirements

```
Python >= 3.10
pygame >= 2.x
Pillow  (PIL) – asset generation only, not needed to run the game
```

```bash
pip install pygame pillow
```

---

## Quick Start

```bash
# Step 1 – generate PNG assets (only needed once)
python generate_assets.py

# Step 2 – launch the game
python main.py
```

---

## Controls

| Key | Action |
|---|---|
| `↑ Arrow` / `Space` / `X` | Jump (in-game) |
| `↑ / ↓ Arrow` | Navigate menu |
| `Enter` / `Space` | Confirm selection |
| `ESC` | Back to menu (pauses game; saves it for Continue) |

---

## Levels

| Level | Gravity | Speed | Gap |
|---|---|---|---|
| 🌿 Easy | 0.25 | −2 px/frame | 220 px |
| 🌑 Medium | 0.35 | −3 px/frame | 180 px |
| 🔥 Hard | 0.50 | −4 px/frame | 140 px |
