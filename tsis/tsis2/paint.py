"""
paint.py – Main entry point for the TSIS 2 Paint application.

Run:
    python paint.py

Keyboard shortcuts:
    1 / 2 / 3   — brush size (2 px / 5 px / 10 px)
    Ctrl+S       — save canvas as timestamped .png
    Delete       — clear canvas
    Escape       — quit
"""

import pygame
import sys
import math
from datetime import datetime

# Import everything we need from tools.py
from tools import (
    # constants
    SCREEN_W, SCREEN_H, TOOLBAR_W, CANVAS_X, CANVAS_W, CANVAS_H,
    WHITE, BLACK, BG_CANVAS, HIGHLIGHT, TEXT_COLOUR,
    BRUSH_SIZES, TOOL_LABELS,
    # tool IDs
    TOOL_PENCIL, TOOL_LINE, TOOL_RECT, TOOL_SQUARE, TOOL_CIRCLE,
    TOOL_RTRIANGLE, TOOL_EQTRIANGLE, TOOL_RHOMBUS,
    TOOL_FILL, TOOL_ERASER, TOOL_TEXT,
    # helpers
    points_for_right_triangle, points_for_equilateral_triangle,
    points_for_rhombus, flood_fill,
    # UI
    Toolbar,
)


class PaintApp:
    """The main Paint application: event loop, drawing logic, and rendering."""

    def __init__(self):
        pygame.init()
        self.screen     = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Paint – TSIS 2")
        self.clock      = pygame.time.Clock()

        # Fonts
        self.font       = pygame.font.SysFont("arial", 18, bold=True)
        self.small_font = pygame.font.SysFont("arial", 13)
        self.text_font  = pygame.font.SysFont("arial", 22)   # used by text tool

        # Canvas — the persistent drawing surface
        self.canvas = pygame.Surface((CANVAS_W, CANVAS_H))
        self.canvas.fill(BG_CANVAS)

        # Toolbar UI component (defined in tools.py)
        self.toolbar = Toolbar(self.font, self.small_font)

        # Active settings
        self.active_tool   = TOOL_PENCIL
        self.active_colour = BLACK
        self.active_size   = BRUSH_SIZES[1]   # start on medium (5 px)

        # Mouse / drawing state
        self.drawing   = False   # True while left mouse button is held
        self.start_pos = None    # canvas-coords where the drag started
        self.last_pos  = None    # previous point for pencil/eraser strokes

        # Text tool state
        self.text_active = False   # True while user is typing
        self.text_pos    = None    # canvas coords of the text anchor
        self.text_buffer = ""      # characters typed so far

        # On-screen save notification
        self._notification     = ""
        self._notification_ttl = 0   # countdown in frames

        self.running = True

    # ── Coordinate helpers ────────────────────

    def to_canvas(self, pos):
        """Convert screen coordinates to canvas coordinates."""
        return (pos[0] - CANVAS_X, pos[1])

    def on_canvas(self, pos):
        """Return True if the screen position is over the canvas (not the toolbar)."""
        return pos[0] >= CANVAS_X

    # ── Save canvas ───────────────────────────

    def _save_canvas(self):
        """Save the current canvas as a timestamped PNG file (triggered by Ctrl+S)."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename  = f"canvas_{timestamp}.png"
        pygame.image.save(self.canvas, filename)
        print(f"[Saved] {filename}")
        self._notification     = f"Saved: {filename}"
        self._notification_ttl = 120   # show for ~2 seconds at 60 fps

    # ── Main loop ─────────────────────────────

    def run(self):
        while self.running:
            self.clock.tick(60)
            self._handle_events()
            self._draw()
        pygame.quit()
        sys.exit()

    # ── Event handling ────────────────────────

    def _handle_events(self):
        for event in pygame.event.get():

            # ── Quit ──
            if event.type == pygame.QUIT:
                self.running = False

            # ── Keyboard ──
            elif event.type == pygame.KEYDOWN:

                # While the text tool is active, all keys go to the text buffer
                if self.text_active:
                    self._handle_text_key(event)
                    continue

                if event.key == pygame.K_ESCAPE:
                    self.running = False

                elif event.key == pygame.K_DELETE:
                    # Delete key clears the canvas
                    self.canvas.fill(BG_CANVAS)

                elif event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL):
                    # Ctrl+S → save canvas as PNG
                    self._save_canvas()

                # Brush size shortcuts: 1, 2, 3
                elif event.key == pygame.K_1:
                    self.active_size = BRUSH_SIZES[0]   # 2 px  (small)
                elif event.key == pygame.K_2:
                    self.active_size = BRUSH_SIZES[1]   # 5 px  (medium)
                elif event.key == pygame.K_3:
                    self.active_size = BRUSH_SIZES[2]   # 10 px (large)

            # ── Mouse button DOWN ──
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos

                # If text tool is typing and user clicks somewhere else → commit the text
                if self.text_active:
                    self._commit_text()

                if not self.on_canvas(pos):
                    # Click inside toolbar → delegate to Toolbar
                    self.active_tool, self.active_colour, self.active_size, clear = \
                        self.toolbar.handle_click(
                            pos, self.active_tool, self.active_colour, self.active_size)
                    if clear:
                        self.canvas.fill(BG_CANVAS)
                else:
                    cp = self.to_canvas(pos)

                    if self.active_tool == TOOL_TEXT:
                        # Start a text-entry session at the clicked canvas position
                        self.text_pos    = cp
                        self.text_buffer = ""
                        self.text_active = True

                    elif self.active_tool == TOOL_FILL:
                        # Flood fill is applied immediately on click
                        flood_fill(self.canvas, cp, self.active_colour)

                    else:
                        # Begin a shape or freehand stroke
                        self.drawing   = True
                        self.start_pos = cp
                        self.last_pos  = cp

                        # Pencil / eraser: draw an initial dot at the click point
                        if self.active_tool in (TOOL_PENCIL, TOOL_ERASER):
                            colour = WHITE if self.active_tool == TOOL_ERASER else self.active_colour
                            pygame.draw.circle(self.canvas, colour, cp, self.active_size // 2)

            # ── Mouse MOTION (while button held) ──
            elif event.type == pygame.MOUSEMOTION and self.drawing:
                pos = event.pos
                if self.on_canvas(pos):
                    cp = self.to_canvas(pos)
                    if self.active_tool in (TOOL_PENCIL, TOOL_ERASER):
                        # Connect previous point to current for a smooth stroke
                        colour = WHITE if self.active_tool == TOOL_ERASER else self.active_colour
                        pygame.draw.line(self.canvas, colour, self.last_pos, cp, self.active_size)
                        self.last_pos = cp
                    # Shape tools: preview is drawn in _draw(); nothing committed yet

            # ── Mouse button UP ──
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.drawing and self.on_canvas(event.pos):
                    # Commit the shape to the canvas
                    self._commit_shape(self.start_pos, self.to_canvas(event.pos))
                self.drawing   = False
                self.start_pos = None

    # ── Text tool helpers ─────────────────────

    def _handle_text_key(self, event):
        """Handle a keypress while the text tool is active."""
        if event.key == pygame.K_RETURN:
            self._commit_text()                         # Enter → commit
        elif event.key == pygame.K_ESCAPE:
            self.text_active = False                    # Esc → cancel
            self.text_buffer = ""
            self.text_pos    = None
        elif event.key == pygame.K_BACKSPACE:
            self.text_buffer = self.text_buffer[:-1]    # delete last character
        elif event.unicode and event.unicode.isprintable():
            self.text_buffer += event.unicode           # append typed character

    def _commit_text(self):
        """Render the typed text permanently onto the canvas."""
        if self.text_buffer and self.text_pos:
            surf = self.text_font.render(self.text_buffer, True, self.active_colour)
            self.canvas.blit(surf, self.text_pos)
        # Reset text state
        self.text_active = False
        self.text_buffer = ""
        self.text_pos    = None

    # ── Shape commitment ──────────────────────

    def _commit_shape(self, p1, p2):
        """
        Draw the final shape from p1 to p2 onto the canvas.
        Called when the mouse button is released.
        """
        x1, y1 = p1;  x2, y2 = p2
        col  = self.active_colour
        w    = self.active_size
        tool = self.active_tool

        if tool == TOOL_LINE:
            pygame.draw.line(self.canvas, col, p1, p2, w)

        elif tool == TOOL_RECT:
            rx = min(x1, x2);  ry = min(y1, y2)
            pygame.draw.rect(self.canvas, col, (rx, ry, abs(x2-x1), abs(y2-y1)), w)

        elif tool == TOOL_SQUARE:
            side = min(abs(x2-x1), abs(y2-y1))
            sx   = x1 if x2 >= x1 else x1 - side
            sy   = y1 if y2 >= y1 else y1 - side
            pygame.draw.rect(self.canvas, col, (sx, sy, side, side), w)

        elif tool == TOOL_CIRCLE:
            cx  = (x1+x2) // 2;  cy = (y1+y2) // 2
            rad = max(1, int(math.hypot(x2-x1, y2-y1) / 2))
            pygame.draw.circle(self.canvas, col, (cx, cy), rad, w)

        elif tool == TOOL_RTRIANGLE:
            pts = [(int(px), int(py))
                   for px, py in points_for_right_triangle(x1, y1, x2, y2)]
            pygame.draw.polygon(self.canvas, col, pts, w)

        elif tool == TOOL_EQTRIANGLE:
            pts = [(int(px), int(py))
                   for px, py in points_for_equilateral_triangle(x1, y1, x2, y2)]
            pygame.draw.polygon(self.canvas, col, pts, w)

        elif tool == TOOL_RHOMBUS:
            pts = [(int(px), int(py))
                   for px, py in points_for_rhombus(x1, y1, x2, y2)]
            pygame.draw.polygon(self.canvas, col, pts, w)

    # ── Live shape preview while dragging ────

    def _draw_preview(self, surface, p1, p2):
        """
        Draw a ghost preview of the shape onto the screen surface
        (NOT onto self.canvas, so it leaves no permanent mark).
        """
        def sc(pt):
            """Shift canvas coords → screen coords."""
            return (pt[0] + CANVAS_X, pt[1])

        x1, y1 = p1;  x2, y2 = p2
        col  = self.active_colour
        w    = self.active_size
        tool = self.active_tool

        if tool == TOOL_LINE:
            pygame.draw.line(surface, col, sc(p1), sc(p2), w)

        elif tool == TOOL_RECT:
            rx = min(x1, x2) + CANVAS_X;  ry = min(y1, y2)
            pygame.draw.rect(surface, col, (rx, ry, abs(x2-x1), abs(y2-y1)), w)

        elif tool == TOOL_SQUARE:
            side = min(abs(x2-x1), abs(y2-y1))
            sx   = (x1 if x2 >= x1 else x1 - side) + CANVAS_X
            sy   = y1 if y2 >= y1 else y1 - side
            pygame.draw.rect(surface, col, (sx, sy, side, side), w)

        elif tool == TOOL_CIRCLE:
            cx  = (x1+x2) // 2 + CANVAS_X;  cy = (y1+y2) // 2
            rad = max(1, int(math.hypot(x2-x1, y2-y1) / 2))
            pygame.draw.circle(surface, col, (cx, cy), rad, w)

        elif tool == TOOL_RTRIANGLE:
            pts = [(int(px)+CANVAS_X, int(py))
                   for px, py in points_for_right_triangle(x1, y1, x2, y2)]
            pygame.draw.polygon(surface, col, pts, w)

        elif tool == TOOL_EQTRIANGLE:
            pts = [(int(px)+CANVAS_X, int(py))
                   for px, py in points_for_equilateral_triangle(x1, y1, x2, y2)]
            pygame.draw.polygon(surface, col, pts, w)

        elif tool == TOOL_RHOMBUS:
            pts = [(int(px)+CANVAS_X, int(py))
                   for px, py in points_for_rhombus(x1, y1, x2, y2)]
            pygame.draw.polygon(surface, col, pts, w)

    # ── Rendering ────────────────────────────

    def _draw(self):
        self.screen.fill(BLACK)

        # Blit canvas onto screen (right of toolbar)
        self.screen.blit(self.canvas, (CANVAS_X, 0))

        # Shape drag preview (not for pencil / eraser / fill / text)
        if self.drawing and self.start_pos and self.active_tool not in (
                TOOL_PENCIL, TOOL_ERASER, TOOL_FILL, TOOL_TEXT):
            mouse_canvas = self.to_canvas(pygame.mouse.get_pos())
            self._draw_preview(self.screen, self.start_pos, mouse_canvas)

        # Text tool live preview with blinking cursor
        if self.text_active and self.text_pos:
            cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""
            preview = self.text_font.render(self.text_buffer + cursor, True, self.active_colour)
            self.screen.blit(preview, (self.text_pos[0] + CANVAS_X, self.text_pos[1]))

        # Toolbar (drawn last so it sits on top of everything)
        self.toolbar.draw(self.screen, self.active_tool, self.active_colour, self.active_size)

        # Status bar at the very bottom
        mx, my   = pygame.mouse.get_pos()
        cx, cy   = self.to_canvas((mx, my))
        tool_lbl = TOOL_LABELS.get(self.active_tool, "")
        status   = self.small_font.render(
            f"{tool_lbl}  ({cx},{cy})  sz:{self.active_size}  [1/2/3=size  Ctrl+S=save]",
            True, TEXT_COLOUR)
        pygame.draw.rect(self.screen, (25, 25, 35), (0, SCREEN_H - 18, SCREEN_W, 18))
        self.screen.blit(status, (CANVAS_X + 4, SCREEN_H - 16))

        # Save notification (green flash in top-left of canvas)
        if self._notification_ttl > 0:
            self._notification_ttl -= 1
            notif = self.font.render(self._notification, True, (50, 220, 100))
            self.screen.blit(notif, (CANVAS_X + 10, 10))

        pygame.display.flip()


# ──────────────────────────────────────────────
# ENTRY POINT
# ──────────────────────────────────────────────
if __name__ == "__main__":
    app = PaintApp()
    app.run()