"""
ui.py – All non-gameplay Pygame screens.

Screens:
  UsernameScreen   – ask the player for a name before the game starts
  MainMenuScreen   – Play / Leaderboard / Settings / Quit
  SettingsScreen   – sound toggle, car colour, difficulty
  GameOverScreen   – score summary + Retry / Main Menu
  LeaderboardScreen– top-10 table + Back
"""

import pygame
from persistence import load_leaderboard, save_settings

# ── Shared colours ────────────────────────────────────────────────────────────
BLACK   = (0,   0,   0)
WHITE   = (255, 255, 255)
GREY    = (160, 160, 160)
DARK    = (30,  30,  40)
ACCENT  = (255, 200, 0)       # gold / yellow accent
RED     = (220, 50,  50)
GREEN   = (50,  200, 80)
BLUE    = (50,  130, 255)

# Car colour options shown in settings
CAR_COLOUR_OPTIONS = {
    "red":    (220, 50,  50),
    "blue":   (50,  130, 255),
    "green":  (50,  200, 80),
    "yellow": (240, 200, 30),
}

DIFFICULTY_OPTIONS = ["easy", "normal", "hard"]


# ── Helper: draw a simple button ──────────────────────────────────────────────

def draw_button(surface, font, text, rect, bg, fg=BLACK, border=None, radius=8):
    """Draw a filled rounded-rect button and return True if it's hovered."""
    mx, my = pygame.mouse.get_pos()
    hovered = rect.collidepoint(mx, my)
    colour  = tuple(min(c + 30, 255) for c in bg) if hovered else bg
    pygame.draw.rect(surface, colour, rect, border_radius=radius)
    if border:
        pygame.draw.rect(surface, border, rect, 2, border_radius=radius)
    lbl = font.render(text, True, fg)
    surface.blit(lbl, lbl.get_rect(center=rect.center))
    return hovered


def draw_title(surface, font, text, y, colour=ACCENT):
    lbl = font.render(text, True, colour)
    surface.blit(lbl, lbl.get_rect(centerx=surface.get_width() // 2, y=y))


# ── Username Screen ───────────────────────────────────────────────────────────

class UsernameScreen:
    """Simple text-input screen to collect the player's name."""

    def __init__(self, screen):
        self.screen  = screen
        self.W, self.H = screen.get_size()
        self.font    = pygame.font.SysFont("consolas", 32, bold=True)
        self.title_f = pygame.font.SysFont("consolas", 48, bold=True)
        self.small_f = pygame.font.SysFont("consolas", 20)
        self.name    = ""
        self.done    = False

    def run(self):
        """Block until the user enters a name and presses Enter. Returns the name string."""
        clock = pygame.time.Clock()
        while not self.done:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.name.strip():
                        self.done = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    elif len(self.name) < 16 and event.unicode.isprintable():
                        self.name += event.unicode
            self._draw()
        return self.name.strip()

    def _draw(self):
        self.screen.fill(DARK)
        draw_title(self.screen, self.title_f, "RACER", self.H // 4)
        draw_title(self.screen, self.font, "Enter your name:", self.H // 2 - 60, WHITE)

        # Input box
        box = pygame.Rect(self.W // 2 - 180, self.H // 2 - 10, 360, 50)
        pygame.draw.rect(self.screen, WHITE, box, border_radius=6)
        name_surf = self.font.render(self.name + "|", True, BLACK)
        self.screen.blit(name_surf, name_surf.get_rect(center=box.center))

        hint = self.small_f.render("Press Enter to continue", True, GREY)
        self.screen.blit(hint, hint.get_rect(centerx=self.W // 2, y=self.H // 2 + 70))
        pygame.display.flip()


# ── Main Menu ─────────────────────────────────────────────────────────────────

class MainMenuScreen:
    """Main menu with Play / Leaderboard / Settings / Quit buttons."""

    # Return codes
    PLAY        = "play"
    LEADERBOARD = "leaderboard"
    SETTINGS    = "settings"
    QUIT        = "quit"

    def __init__(self, screen):
        self.screen  = screen
        self.W, self.H = screen.get_size()
        self.title_f = pygame.font.SysFont("consolas", 56, bold=True)
        self.btn_f   = pygame.font.SysFont("consolas", 28, bold=True)
        self.sub_f   = pygame.font.SysFont("consolas", 18)

    def run(self):
        clock = pygame.time.Clock()
        btn_w, btn_h = 280, 54
        cx = self.W // 2

        buttons = [
            (pygame.Rect(cx - btn_w // 2, 260, btn_w, btn_h), "▶  PLAY",        self.PLAY,        GREEN,  BLACK),
            (pygame.Rect(cx - btn_w // 2, 330, btn_w, btn_h), "🏆  LEADERBOARD", self.LEADERBOARD, ACCENT, BLACK),
            (pygame.Rect(cx - btn_w // 2, 400, btn_w, btn_h), "⚙  SETTINGS",    self.SETTINGS,    BLUE,   WHITE),
            (pygame.Rect(cx - btn_w // 2, 470, btn_w, btn_h), "✕  QUIT",         self.QUIT,        RED,    WHITE),
        ]

        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return self.QUIT
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for rect, _, action, _, _ in buttons:
                        if rect.collidepoint(event.pos):
                            return action

            self.screen.fill(DARK)
            # Road stripes decorative background
            for i in range(0, self.H, 40):
                pygame.draw.rect(self.screen, (40, 42, 52), (0, i, self.W, 18))

            draw_title(self.screen, self.title_f, "🏎  RACER", 140)
            sub = self.sub_f.render("TSIS 3  –  Advanced Edition", True, GREY)
            self.screen.blit(sub, sub.get_rect(centerx=cx, y=210))

            for rect, label, _, bg, fg in buttons:
                draw_button(self.screen, self.btn_f, label, rect, bg, fg, border=WHITE)

            pygame.display.flip()


# ── Settings Screen ───────────────────────────────────────────────────────────

class SettingsScreen:
    """Toggle sound, pick car colour, pick difficulty. Saves on exit."""

    BACK = "back"

    def __init__(self, screen, settings):
        self.screen   = screen
        self.settings = settings   # dict reference — mutations are visible to caller
        self.W, self.H = screen.get_size()
        self.title_f  = pygame.font.SysFont("consolas", 42, bold=True)
        self.label_f  = pygame.font.SysFont("consolas", 26, bold=True)
        self.btn_f    = pygame.font.SysFont("consolas", 22, bold=True)

    def run(self):
        clock = pygame.time.Clock()
        back_rect = pygame.Rect(self.W // 2 - 120, self.H - 80, 240, 48)

        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos

                    # Sound toggle
                    if self._sound_rect().collidepoint(pos):
                        self.settings["sound"] = not self.settings["sound"]
                        save_settings(self.settings)

                    # Car colour buttons
                    for name, rect in self._colour_rects():
                        if rect.collidepoint(pos):
                            self.settings["car_color"] = name
                            save_settings(self.settings)

                    # Difficulty buttons
                    for diff, rect in self._diff_rects():
                        if rect.collidepoint(pos):
                            self.settings["difficulty"] = diff
                            save_settings(self.settings)

                    if back_rect.collidepoint(pos):
                        return self.BACK

            self._draw(back_rect)

    # ── Layout helpers ─────────────────────

    def _sound_rect(self):
        return pygame.Rect(self.W // 2 + 10, 180, 160, 40)

    def _colour_rects(self):
        rects = []
        names = list(CAR_COLOUR_OPTIONS.keys())
        for i, name in enumerate(names):
            r = pygame.Rect(80 + i * 130, 290, 110, 40)
            rects.append((name, r))
        return rects

    def _diff_rects(self):
        rects = []
        for i, diff in enumerate(DIFFICULTY_OPTIONS):
            r = pygame.Rect(80 + i * 200, 390, 170, 40)
            rects.append((diff, r))
        return rects

    def _draw(self, back_rect):
        self.screen.fill(DARK)
        draw_title(self.screen, self.title_f, "⚙  SETTINGS", 60)

        # ── Sound ──
        sound_lbl = self.label_f.render("Sound:", True, WHITE)
        self.screen.blit(sound_lbl, (80, 188))
        sound_state = "ON" if self.settings["sound"] else "OFF"
        sound_col   = GREEN if self.settings["sound"] else RED
        draw_button(self.screen, self.btn_f, sound_state,
                    self._sound_rect(), sound_col, WHITE, border=WHITE)

        # ── Car colour ──
        col_lbl = self.label_f.render("Car colour:", True, WHITE)
        self.screen.blit(col_lbl, (80, 255))
        for name, rect in self._colour_rects():
            active = self.settings["car_color"] == name
            bg = CAR_COLOUR_OPTIONS[name]
            border = WHITE if active else GREY
            pygame.draw.rect(self.screen, bg, rect, border_radius=6)
            pygame.draw.rect(self.screen, border, rect, 3 if active else 1, border_radius=6)
            lbl = self.btn_f.render(name.capitalize(), True, WHITE)
            self.screen.blit(lbl, lbl.get_rect(center=rect.center))

        # ── Difficulty ──
        diff_lbl = self.label_f.render("Difficulty:", True, WHITE)
        self.screen.blit(diff_lbl, (80, 358))
        for diff, rect in self._diff_rects():
            active = self.settings["difficulty"] == diff
            bg = ACCENT if active else (60, 63, 80)
            fg = BLACK  if active else WHITE
            draw_button(self.screen, self.btn_f, diff.capitalize(),
                        rect, bg, fg, border=WHITE)

        # ── Back button ──
        draw_button(self.screen, self.btn_f, "← Back", back_rect, (80, 80, 100), WHITE, border=WHITE)

        pygame.display.flip()


# ── Game Over Screen ──────────────────────────────────────────────────────────

class GameOverScreen:
    """Show final stats; player chooses Retry or Main Menu."""

    RETRY = "retry"
    MENU  = "menu"

    def __init__(self, screen):
        self.screen  = screen
        self.W, self.H = screen.get_size()
        self.title_f = pygame.font.SysFont("consolas", 52, bold=True)
        self.stat_f  = pygame.font.SysFont("consolas", 28)
        self.btn_f   = pygame.font.SysFont("consolas", 26, bold=True)

    def run(self, score, distance, coins, username):
        clock = pygame.time.Clock()
        cx = self.W // 2
        retry_rect = pygame.Rect(cx - 260, 430, 230, 52)
        menu_rect  = pygame.Rect(cx + 30,  430, 230, 52)

        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if retry_rect.collidepoint(event.pos):
                        return self.RETRY
                    if menu_rect.collidepoint(event.pos):
                        return self.MENU

            self.screen.fill(DARK)
            draw_title(self.screen, self.title_f, "GAME  OVER", 80, RED)

            stats = [
                (f"Player:    {username}",  WHITE),
                (f"Score:     {score}",     ACCENT),
                (f"Distance:  {distance} m", GREEN),
                (f"Coins:     {coins}",     (255, 220, 80)),
            ]
            for i, (text, col) in enumerate(stats):
                lbl = self.stat_f.render(text, True, col)
                self.screen.blit(lbl, lbl.get_rect(centerx=cx, y=220 + i * 48))

            draw_button(self.screen, self.btn_f, "↺  Retry",    retry_rect, GREEN,  BLACK, border=WHITE)
            draw_button(self.screen, self.btn_f, "⌂  Main Menu", menu_rect,  BLUE,   WHITE, border=WHITE)

            pygame.display.flip()


# ── Leaderboard Screen ────────────────────────────────────────────────────────

class LeaderboardScreen:
    """Display the top-10 entries from leaderboard.json."""

    BACK = "back"

    def __init__(self, screen):
        self.screen  = screen
        self.W, self.H = screen.get_size()
        self.title_f = pygame.font.SysFont("consolas", 42, bold=True)
        self.row_f   = pygame.font.SysFont("consolas", 22)
        self.head_f  = pygame.font.SysFont("consolas", 22, bold=True)
        self.btn_f   = pygame.font.SysFont("consolas", 24, bold=True)

    def run(self):
        clock  = pygame.time.Clock()
        back_r = pygame.Rect(self.W // 2 - 110, self.H - 72, 220, 46)
        entries = load_leaderboard()

        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_r.collidepoint(event.pos):
                        return self.BACK

            self.screen.fill(DARK)
            draw_title(self.screen, self.title_f, "🏆  LEADERBOARD", 40)

            # Header row
            cx = self.W // 2
            cols = [80, 200, 380, 520, 650]
            headers = ["#", "NAME", "SCORE", "DIST(m)", "COINS"]
            for x, h in zip(cols, headers):
                lbl = self.head_f.render(h, True, ACCENT)
                self.screen.blit(lbl, (x, 115))

            # Separator
            pygame.draw.line(self.screen, GREY, (60, 142), (self.W - 60, 142), 1)

            # Data rows
            for i, entry in enumerate(entries[:10]):
                y   = 155 + i * 36
                row_col = WHITE if i % 2 == 0 else GREY
                vals = [
                    str(i + 1),
                    entry.get("name",     "-")[:12],
                    str(entry.get("score",    0)),
                    str(entry.get("distance", 0)),
                    str(entry.get("coins",    0)),
                ]
                for x, val in zip(cols, vals):
                    lbl = self.row_f.render(val, True, row_col)
                    self.screen.blit(lbl, (x, y))

            if not entries:
                empty = self.row_f.render("No scores yet — play the game!", True, GREY)
                self.screen.blit(empty, empty.get_rect(centerx=cx, y=200))

            draw_button(self.screen, self.btn_f, "← Back", back_r, (80, 80, 100), WHITE, border=WHITE)
            pygame.display.flip()