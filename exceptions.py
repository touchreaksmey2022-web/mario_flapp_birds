"""
exceptions.py
=============
Custom exception hierarchy for Mario Flappy Bird.

All game-specific errors derive from ``MarioFlappyError`` so callers can
catch the whole family with a single ``except MarioFlappyError`` clause if
they prefer coarse-grained handling.

Exception Tree
--------------
MarioFlappyError
├── AssetNotFoundError   – a required PNG/ICO file is absent from assets/
├── InvalidLevelError    – caller supplied an unrecognised level name
└── SaveFileCorruptError – mario_scores.txt exists but cannot be parsed

Notes
-----
  Prefer raising these over bare built-ins so error messages carry enough
  context for the player (or developer) to self-diagnose the problem.
"""


class MarioFlappyError(Exception):
    """Base class for all Mario Flappy Bird errors."""


class AssetNotFoundError(MarioFlappyError, FileNotFoundError):
    """
    Raised when a required game asset file is missing.

    Arguments
    ---------
    name     : str  – the filename that could not be found
    asset_dir: str  – the directory that was searched

    Example
    -------
    >>> raise AssetNotFoundError("mario.png", "/path/to/assets")
    AssetNotFoundError: Asset 'mario.png' not found in '/path/to/assets'.
    Run generate_assets.py to recreate all assets.
    """

    def __init__(self, name: str, asset_dir: str) -> None:
        self.name      = name
        self.asset_dir = asset_dir
        super().__init__(
            f"Asset '{name}' not found in '{asset_dir}'.\n"
            "Run generate_assets.py to recreate all assets."
        )


class InvalidLevelError(MarioFlappyError, ValueError):
    """
    Raised when an unrecognised level name is requested.

    Arguments
    ---------
    name  : str       – the bad level name supplied by the caller
    valid : list[str] – the accepted level names

    Example
    -------
    >>> raise InvalidLevelError("Insane", ["Easy", "Medium", "Hard"])
    InvalidLevelError: Unknown level 'Insane'. Valid options: ['Easy', 'Medium', 'Hard']
    """

    def __init__(self, name: str, valid: list[str]) -> None:
        self.name  = name
        self.valid = valid
        super().__init__(
            f"Unknown level '{name}'. Valid options: {valid}"
        )


class SaveFileCorruptError(MarioFlappyError):
    """
    Raised when the high-score file exists but cannot be parsed.

    Arguments
    ---------
    path  : str       – absolute path to the corrupt file
    cause : Exception – the underlying parse error

    Example
    -------
    >>> raise SaveFileCorruptError("/path/mario_scores.txt", json.JSONDecodeError(...))
    SaveFileCorruptError: Cannot parse score file '/path/mario_scores.txt': ...
    """

    def __init__(self, path: str, cause: Exception) -> None:
        self.path  = path
        self.cause = cause
        super().__init__(
            f"Cannot parse score file '{path}': {cause}"
        )
