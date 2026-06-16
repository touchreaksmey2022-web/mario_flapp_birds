"""
assets.py
=========
Asset loading utilities and high-score persistence helpers.

All file I/O (images, JSON scores) is centralised here so the rest of the
codebase never needs to know where files live or how they are stored.

Functions
---------
asset_path(name)          – resolve and validate an asset filepath
load_surface(name, size)  – load a pygame Surface from the assets folder
load_scores()             – read high scores from mario_scores.txt
save_scores(scores)       – write high scores to mario_scores.txt

Notes
-----
  ``load_surface`` must be called **after** ``pygame.init()`` because it
  calls ``pygame.image.load`` and ``.convert_alpha()``.
"""

import json
import os

import pygame

from constants  import ASSET_DIR, SCORE_FILE, LEVEL_ORDER
from exceptions import AssetNotFoundError, SaveFileCorruptError


# ── Path helpers ───────────────────────────────────────────────────────────────

def asset_path(name: str) -> str:
    """
    Resolve and validate the absolute path to an asset file.

    Arguments
    ---------
    name : str
        Filename inside the ``assets/`` directory (e.g. ``'mario.png'``).

    Returns
    -------
    str
        Absolute path to the file.

    Raises
    ------
    AssetNotFoundError
        If the file does not exist on disk.

    Example
    -------
    >>> path = asset_path("mario.png")
    >>> path.endswith("mario.png")
    True
    """
    path = os.path.join(ASSET_DIR, name)
    if not os.path.isfile(path):
        raise AssetNotFoundError(name, ASSET_DIR)
    return path


# ── Surface loader ─────────────────────────────────────────────────────────────

def load_surface(
    name: str,
    size: tuple[int, int] | None = None,
) -> pygame.Surface:
    """
    Load an image asset as a pygame Surface, optionally scaling it.

    Arguments
    ---------
    name : str
        Filename inside the ``assets/`` directory.
    size : tuple[int, int] | None
        If provided, the surface is scaled to ``(width, height)`` after
        loading.  Pass ``None`` to keep the original size.

    Returns
    -------
    pygame.Surface
        RGBA surface ready for blitting.

    Raises
    ------
    AssetNotFoundError
        Propagated from ``asset_path()`` if the file is missing.

    Notes
    -----
      Requires ``pygame.display.set_mode()`` to have been called first so
      that ``convert_alpha()`` can determine the pixel format.

    Example
    -------
    >>> surf = load_surface("mario.png", (34, 40))
    >>> surf.get_size()
    (34, 40)
    """
    path = asset_path(name)
    surf = pygame.image.load(path).convert_alpha()
    if size is not None:
        surf = pygame.transform.scale(surf, size)
    return surf


# ── Score persistence ──────────────────────────────────────────────────────────

def load_scores() -> dict[str, int]:
    """
    Read per-level high scores from ``mario_scores.txt``.

    Returns
    -------
    dict[str, int]
        Mapping of level name → best score.  Any level absent from the
        file defaults to ``0``.

    Raises
    ------
    SaveFileCorruptError
        If the file exists but cannot be parsed as JSON or the values
        cannot be cast to ``int``.

    Notes
    -----
      If the score file does not exist yet, a zeroed default dict is
      returned silently (no exception).

    Example
    -------
    >>> scores = load_scores()
    >>> isinstance(scores["Easy"], int)
    True
    """
    defaults: dict[str, int] = {lvl: 0 for lvl in LEVEL_ORDER}
    if not os.path.isfile(SCORE_FILE):
        return defaults
    try:
        with open(SCORE_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        for lvl in LEVEL_ORDER:
            defaults[lvl] = int(data.get(lvl, 0))
        return defaults
    except (json.JSONDecodeError, ValueError, KeyError) as exc:
        raise SaveFileCorruptError(SCORE_FILE, exc) from exc


def save_scores(scores: dict[str, int]) -> None:
    """
    Persist high scores to ``mario_scores.txt`` as formatted JSON.

    Arguments
    ---------
    scores : dict[str, int]
        Current scores mapping to write.  Extra keys beyond ``LEVEL_ORDER``
        are written as-is and will be ignored on next load.

    Notes
    -----
      Writes atomically-ish: the file is opened in write mode so a partial
      write replaces the entire file.  For a production game, a temp-file +
      rename pattern would be safer.

    Example
    -------
    >>> save_scores({"Easy": 10, "Medium": 5, "Hard": 0})
    """
    with open(SCORE_FILE, "w", encoding="utf-8") as fh:
        json.dump(scores, fh, indent=2)
