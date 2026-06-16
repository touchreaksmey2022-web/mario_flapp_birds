"""
menu.py
=======
Menu rendering and keyboard-navigation for the main menu and the
level-select sub-screen.

Classes
-------
Menu            – main menu (Start / Continue / Level / Sound / Exit)

Functions
---------
draw_level_select(...)  – full-screen level-picker overlay

Notes
-----
  Neither ``Menu`` nor ``draw_level_select`` mutate game state directly.
  They return action strings which ``main.py`` interprets and acts upon.
"""

import pygame

from constants import (
    GAME_WIDTH, GAME_HEIGHT,
    WHITE, YELLOW, GOLD,
    MENU_ITEMS, SOUND_LABEL,
    LEVEL_CONFIG, LEVEL_ORDER,
)


class Menu:
    """
    Full-screen main menu renderer and keyboard handler.

    The menu displays five items (Start, Continue, Level, Sound, Exit)
    with a gold highlight bar on the currently focused item.  Keyboard
    navigation uses the Up/Down arrow keys; Enter or Space confirms.

    Arguments
    ---------
    window   : pygame.Surface
        Display surface used as the render target.
    font_big : pygame.font.Font
        Large font for the "MARIO FLAPPY" title.
    font_med : pygame.font.Font
        Medium font for menu items and footer info.

    Attributes
    ----------
    cursor : int
        Index into ``MENU_ITEMS`` for the currently highlighted entry.

    Notes
    -----
      Re-use the same ``Menu`` instance across the lifetime of the process
      so the cursor position is preserved when the player returns from
      gameplay.
    """

    def __init__(
        self,
        window:   pygame.Surface,
        font_big: pygame.font.Font,
        font_med: pygame.font.Font,
    ) -> None:
        self.window:   pygame.Surface    = window
        self.font_big: pygame.font.Font  = font_big
        self.font_med: pygame.font.Font  = font_med
        self.cursor:   int               = 0

    # ── Drawing ────────────────────────────────────────────────────────────────

    def draw(
        self,
        bg:             pygame.Surface,
        current_level:  str,
        sound_on:       bool,
        high_scores:    dict[str, int],
        has_saved_game: bool,
    ) -> None:
        """
        Render the main menu over *bg*.

        Arguments
        ---------
        bg             : background surface (blitted first).
        current_level  : active level name shown in the footer.
        sound_on       : controls the Sound item label.
        high_scores    : per-level best scores shown in the footer.
        has_saved_game : if ``False``, Continue shows a ``(no save)`` hint.
        """
        self.window.blit(bg, (0, 0))

        # Semi-transparent backing panel
        panel = pygame.Surface((280, 420), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 170))
        self.window.blit(panel, (40, 90))

        # ── Title ─────────────────────────────────────────────────────────────
        title = self.font_big.render("MARIO FLAPPY", True, GOLD)
        self.window.blit(title, (GAME_WIDTH // 2 - title.get_width() // 2, 100))

        # ── Menu items ────────────────────────────────────────────────────────
        for i, item in enumerate(MENU_ITEMS):
            label = self._item_label(item, sound_on, has_saved_game)
            colour = YELLOW if i == self.cursor else WHITE
            surf   = self.font_med.render(label, True, colour)

            item_y = 180 + i * 52

            if i == self.cursor:
                bar_w = surf.get_width() + 20
                bar_h = surf.get_height() + 4
                bar   = pygame.Surface((bar_w, bar_h), pygame.SRCALPHA)
                bar.fill((255, 220, 0, 60))
                self.window.blit(bar, (GAME_WIDTH // 2 - bar_w // 2, item_y - 2))

            self.window.blit(surf, (GAME_WIDTH // 2 - surf.get_width() // 2, item_y))

        # ── Footer ────────────────────────────────────────────────────────────
        lvl_surf = self.font_med.render(f"Level: {current_level}", True, (180, 255, 180))
        hi_surf  = self.font_med.render(
            f"Best: {high_scores.get(current_level, 0)}", True, (255, 200, 150)
        )
        self.window.blit(lvl_surf, (GAME_WIDTH // 2 - lvl_surf.get_width() // 2, 455))
        self.window.blit(hi_surf,  (GAME_WIDTH // 2 - hi_surf.get_width()  // 2, 485))

    # ── Input ──────────────────────────────────────────────────────────────────

    def handle_key(self, key: int) -> str | None:
        """
        Process a single keypress and optionally return an action string.

        Arguments
        ---------
        key : int
            A ``pygame.K_*`` constant from the ``KEYDOWN`` event.

        Returns
        -------
        str | None
            One of the ``MENU_ITEMS`` strings when the player confirms a
            selection (Enter or Space); ``None`` for navigation-only keys.

        Notes
        -----
          The cursor wraps around at both ends of the item list.
        """
        if key == pygame.K_UP:
            self.cursor = (self.cursor - 1) % len(MENU_ITEMS)
        elif key == pygame.K_DOWN:
            self.cursor = (self.cursor + 1) % len(MENU_ITEMS)
        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            return MENU_ITEMS[self.cursor]
        return None

    # ── Private ────────────────────────────────────────────────────────────────

    @staticmethod
    def _item_label(item: str, sound_on: bool, has_saved_game: bool) -> str:
        """
        Resolve the display label for a menu item.

        Arguments
        ---------
        item           : str   – raw item name from ``MENU_ITEMS``
        sound_on       : bool  – current sound toggle state
        has_saved_game : bool  – whether a paused game can be continued

        Returns
        -------
        str  – the string to render on screen
        """
        if item == "Sound":
            return SOUND_LABEL[sound_on]
        if item == "Continue" and not has_saved_game:
            return "Continue  (no save)"
        return item


# ── Level-select screen (standalone function) ──────────────────────────────────

def draw_level_select(
    window:        pygame.Surface,
    current_level: str,
    cursor:        int,
    font_big:      pygame.font.Font,
    font_med:      pygame.font.Font,
    bg:            pygame.Surface,
) -> None:
    """
    Render the full-screen level-select overlay.

    The three levels are listed vertically; the active level is marked with
    a check-mark (✓) and the highlighted item is drawn in yellow.

    Arguments
    ---------
    window        : render target.
    current_level : the level currently set in the game (shown with ✓).
    cursor        : index into ``LEVEL_ORDER`` for the highlighted row.
    font_big      : title font.
    font_med      : item / hint font.
    bg            : background surface drawn behind the dark overlay.

    Notes
    -----
      Navigation (Up/Down) and confirmation (Enter/Space) are handled by
      the caller in ``main.py``; this function is purely presentational.
    """
    window.blit(bg, (0, 0))

    overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    window.blit(overlay, (0, 0))

    title = font_big.render("Select Level", True, GOLD)
    window.blit(title, (GAME_WIDTH // 2 - title.get_width() // 2, 140))

    for i, lvl in enumerate(LEVEL_ORDER):
        label  = LEVEL_CONFIG[lvl]["label"]
        if lvl == current_level:
            label += "  ✓"
        colour = YELLOW if i == cursor else WHITE
        surf   = font_med.render(label, True, colour)
        window.blit(surf, (GAME_WIDTH // 2 - surf.get_width() // 2, 230 + i * 70))

    hint = font_med.render("ENTER to confirm   ESC to back", True, (180, 180, 180))
    window.blit(hint, (GAME_WIDTH // 2 - hint.get_width() // 2, 460))
