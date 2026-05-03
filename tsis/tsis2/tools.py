"""
tools.py – Reusable tools, geometry helpers, flood fill, and Toolbar UI
for the TSIS 2 Paint application.
"""

import pygame
import math

# ──────────────────────────────────────────────
# CONSTANTS
# ──────────────────────────────────────────────
SCREEN_W  = 900
SCREEN_H  = 650
TOOLBAR_W = 160
CANVAS_X  = TOOLBAR_W
CANVAS_W  = SCREEN_W - TOOLBAR_W
CANVAS_H  = SCREEN_H

# Colours
WHITE       = (255, 255, 255)
BLACK       = (0,   0,   0)
BG_TOOLBAR  = (40,  42,  54)
BG_CANVAS   = (255, 255, 255)
HIGHLIGHT   = (80, 140, 255)
TEXT_COLOUR = (220, 220, 220)

# Selectable drawing colours (palette)
PALETTE = [
    (0,   0,   0),
    (220, 40,  40),
    (30,  120, 255),
    (50,  200, 80),
    (255, 220, 0),
    (255, 140, 0),
    (180, 60,  200),
    (0,   200, 200),
    (255, 105, 180),
    (139, 90,  43),
    (128, 128, 128),
    (255, 255, 255),
]

# Brush size levels — switched with keyboard keys 1 / 2 / 3
BRUSH_SIZES = [2, 5, 10]

# Tool IDs
TOOL_PENCIL     = "pencil"
TOOL_LINE       = "line"
TOOL_RECT       = "rect"
TOOL_SQUARE     = "square"
TOOL_CIRCLE     = "circle"
TOOL_RTRIANGLE  = "right_tri"
TOOL_EQTRIANGLE = "eq_tri"
TOOL_RHOMBUS    = "rhombus"
TOOL_FILL       = "fill"
TOOL_ERASER     = "eraser"
TOOL_TEXT       = "text"

# Display labels shown on toolbar buttons
TOOL_LABELS = {
    TOOL_PENCIL:     "✏ Pencil",
    TOOL_LINE:       "╱ Line",
    TOOL_RECT:       "▭ Rectangle",
    TOOL_SQUARE:     "■ Square",
    TOOL_CIRCLE:     "○ Circle",
    TOOL_RTRIANGLE:  "◺ R-Triangle",
    TOOL_EQTRIANGLE: "△ Eq-Triangle",
    TOOL_RHOMBUS:    "◇ Rhombus",
    TOOL_FILL:       "🪣 Fill",
    TOOL_ERASER:     "⬜ Eraser",
    TOOL_TEXT:       "T  Text",
}

# Top-to-bottom order of tool buttons in the toolbar
TOOL_ORDER = [
    TOOL_PENCIL, TOOL_LINE,
    TOOL_RECT, TOOL_SQUARE,
    TOOL_CIRCLE,
    TOOL_RTRIANGLE, TOOL_EQTRIANGLE,
    TOOL_RHOMBUS,
    TOOL_FILL, TOOL_ERASER,
    TOOL_TEXT,
]

# ──────────────────────────────────────────────
# GEOMETRY HELPERS
# ──────────────────────────────────────────────

def points_for_right_triangle(x1, y1, x2, y2):
    """
    Right-angle triangle with the 90° corner at bottom-left.
    Legs are axis-aligned.
    """
    return [(x1, y1), (x1, y2), (x2, y2)]


def points_for_equilateral_triangle(x1, y1, x2, y2):
    """
    Equilateral triangle whose base spans x1→x2 at the lower y,
    with the apex centred above.
    """
    bx1  = min(x1, x2);  bx2 = max(x1, x2)
    by   = max(y1, y2)
    cx   = (bx1 + bx2) / 2
    side = bx2 - bx1
    ay   = by - side * math.sqrt(3) / 2
    return [(cx, ay), (bx1, by), (bx2, by)]


def points_for_rhombus(x1, y1, x2, y2):
    """
    Rhombus (diamond) inscribed in the bounding box (x1,y1)→(x2,y2).
    Its four vertices are the midpoints of each edge of the bounding box.
    """
    lx = min(x1, x2);  rx = max(x1, x2)
    ty = min(y1, y2);  by = max(y1, y2)
    cx = (lx + rx) / 2
    cy = (ty + by) / 2
    return [(cx, ty), (rx, cy), (cx, by), (lx, cy)]


# ──────────────────────────────────────────────
# FLOOD FILL
# ──────────────────────────────────────────────

def flood_fill(surface, pos, fill_colour):
    """
    Iterative flood fill starting at pixel `pos` on `surface`.
    Replaces all connected pixels of the original colour with `fill_colour`.
    """
    target = surface.get_at(pos)[:3]   # original colour (ignore alpha)
    if target == fill_colour:
        return                          # already the right colour — nothing to do

    width, height = surface.get_size()
    stack   = [pos]
    visited = set()

    while stack:
        x, y = stack.pop()
        if (x, y) in visited:
            continue
        if not (0 <= x < width and 0 <= y < height):
            continue
        if surface.get_at((x, y))[:3] != target:
            continue
        surface.set_at((x, y), fill_colour)
        visited.add((x, y))
        stack += [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]


# ──────────────────────────────────────────────
# TOOLBAR UI COMPONENT
# ──────────────────────────────────────────────

class Toolbar:
    """Renders the left-side toolbar: tool buttons, colour palette, size picker, clear button."""

    BTN_H   = 34
    BTN_PAD = 4
    SEC_GAP = 10

    def __init__(self, font, small_font):
        self.font       = font
        self.small_font = small_font

        # ── Tool buttons ──
        self.tool_rects = {}
        y = 10
        for tool in TOOL_ORDER:
            self.tool_rects[tool] = pygame.Rect(6, y, TOOLBAR_W - 12, self.BTN_H)
            y += self.BTN_H + self.BTN_PAD
        self.tool_section_bottom = y + self.SEC_GAP

        # ── Palette swatches (4 per row) ──
        self.palette_rects = []
        SWATCH = 28
        px, py = 8, self.tool_section_bottom + 24
        for i, col in enumerate(PALETTE):
            r = pygame.Rect(
                px + (i % 4) * (SWATCH + 4),
                py + (i // 4) * (SWATCH + 4),
                SWATCH, SWATCH
            )
            self.palette_rects.append((r, col))
        self.palette_bottom = py + (len(PALETTE) // 4 + 1) * (SWATCH + 4) + self.SEC_GAP

        # ── Size buttons ──
        self.size_rects = []
        sx, sy = 10, self.palette_bottom + 24
        for i, sz in enumerate(BRUSH_SIZES):
            self.size_rects.append((pygame.Rect(sx + i * 44, sy, 38, 30), sz))

        # ── Clear button ──
        self.clear_rect = pygame.Rect(10, sy + 44, TOOLBAR_W - 20, 32)

    # ── Drawing ──────────────────────────────

    def draw(self, surface, active_tool, active_colour, active_size):
        """Render the full toolbar onto `surface`."""
        # Background + divider line
        pygame.draw.rect(surface, BG_TOOLBAR, (0, 0, TOOLBAR_W, SCREEN_H))
        pygame.draw.line(surface, HIGHLIGHT, (TOOLBAR_W - 1, 0), (TOOLBAR_W - 1, SCREEN_H), 2)

        # Section header: TOOLS
        self._header(surface, "TOOLS", 2)

        # Tool buttons
        for tool, rect in self.tool_rects.items():
            col = HIGHLIGHT if tool == active_tool else (60, 63, 78)
            pygame.draw.rect(surface, col, rect, border_radius=5)
            txt = self.small_font.render(TOOL_LABELS[tool], True, WHITE)
            surface.blit(txt, txt.get_rect(center=rect.center))

        # Section header: COLOUR
        self._header(surface, "COLOUR", self.tool_section_bottom + 6)

        # Palette swatches
        for rect, col in self.palette_rects:
            pygame.draw.rect(surface, col, rect, border_radius=4)
            border_col = WHITE if col == active_colour else (100, 100, 100)
            border_w   = 3     if col == active_colour else 1
            pygame.draw.rect(surface, border_col, rect, border_w, border_radius=4)

        # Section header: SIZE (1/2/3)
        self._header(surface, "SIZE  (1/2/3)", self.palette_bottom + 6)

        # Size buttons
        for rect, sz in self.size_rects:
            col = HIGHLIGHT if sz == active_size else (60, 63, 78)
            pygame.draw.rect(surface, col, rect, border_radius=4)
            pygame.draw.circle(surface, WHITE, rect.center, min(sz // 2 + 2, 10))
            lbl = self.small_font.render(str(sz), True, TEXT_COLOUR)
            surface.blit(lbl, (rect.x + 2, rect.y + 2))

        # Clear button
        pygame.draw.rect(surface, (180, 50, 50), self.clear_rect, border_radius=6)
        ct = self.small_font.render("🗑 Clear", True, WHITE)
        surface.blit(ct, ct.get_rect(center=self.clear_rect.center))

    def _header(self, surface, text, y):
        """Helper: render a centred section label."""
        surf = self.small_font.render(text, True, TEXT_COLOUR)
        surface.blit(surf, (TOOLBAR_W // 2 - surf.get_width() // 2, y))

    # ── Click handling ────────────────────────

    def handle_click(self, pos, active_tool, active_colour, active_size):
        """
        Test whether a mouse click hit any toolbar element.
        Returns (new_tool, new_colour, new_size, clear_requested).
        """
        new_tool   = active_tool
        new_colour = active_colour
        new_size   = active_size
        clear      = False

        for tool, rect in self.tool_rects.items():
            if rect.collidepoint(pos):
                new_tool = tool

        for rect, col in self.palette_rects:
            if rect.collidepoint(pos):
                new_colour = col

        for rect, sz in self.size_rects:
            if rect.collidepoint(pos):
                new_size = sz

        if self.clear_rect.collidepoint(pos):
            clear = True

        return new_tool, new_colour, new_size, clear