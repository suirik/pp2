"""
racer.py – Core gameplay for the TSIS 3 Racer game.

Contains:
  RacerGame  – the main game-loop class; call .run() to play one session.

Features (TSIS 3):
  • Lane hazards: oil spills, speed bumps (slow zones), nitro strips
  • Dynamic traffic cars (enemy vehicles)
  • Road obstacles: barriers and potholes
  • Three power-ups: Nitro, Shield, Repair
  • Weighted coins (value 1 / 3 / 5)
  • Difficulty scaling (traffic density, obstacle frequency)
  • Score = coins × value + distance bonus + power-up bonuses
  • Distance meter shown on screen
  • Safe spawn logic — nothing spawns on top of the player
"""

import pygame
import random
import math

# ── Colours ───────────────────────────────────────────────────────────────────
BLACK        = (0,   0,   0)
WHITE        = (255, 255, 255)
GREY         = (160, 160, 160)
DARK_GREY    = (50,  50,  50)
ROAD_COL     = (60,  60,  60)
LINE_COL     = (230, 230, 230)
GRASS_COL    = (34,  139, 34)
RED          = (220, 50,  50)
GREEN        = (50,  200, 80)
BLUE         = (50,  130, 255)
YELLOW       = (255, 220, 0)
ORANGE       = (255, 140, 0)
PURPLE       = (180, 60,  200)
CYAN         = (0,   200, 200)
DARK_BLUE    = (20,  40,  100)

# Car colour map (matches settings)
CAR_COLOURS = {
    "red":    (220, 50,  50),
    "blue":   (50,  130, 255),
    "green":  (50,  200, 80),
    "yellow": (240, 200, 30),
}

# ── Screen & road geometry ────────────────────────────────────────────────────
SCREEN_W = 800
SCREEN_H = 600
ROAD_X   = 120          # left edge of the road
ROAD_W   = 560          # width of the road
NUM_LANES = 4
LANE_W   = ROAD_W // NUM_LANES

# ── Difficulty tables ─────────────────────────────────────────────────────────
DIFF_PARAMS = {
    "easy":   {"base_speed": 4, "enemy_interval": 140, "obstacle_interval": 200, "coin_interval": 60},
    "normal": {"base_speed": 6, "enemy_interval": 100, "obstacle_interval": 140, "coin_interval": 50},
    "hard":   {"base_speed": 8, "enemy_interval":  70, "obstacle_interval":  90, "coin_interval": 40},
}

# ── Spawn intervals for power-ups ─────────────────────────────────────────────
POWERUP_INTERVAL = 300   # frames between power-up spawns


# ── Helper: lane centre x ─────────────────────────────────────────────────────
def lane_x(lane_idx):
    """Return the centre x-coordinate of the given lane (0-indexed)."""
    return ROAD_X + lane_idx * LANE_W + LANE_W // 2


# ── Sprite base ───────────────────────────────────────────────────────────────

class RoadSprite:
    """Minimal axis-aligned rectangle entity."""
    def __init__(self, x, y, w, h, colour):
        self.rect   = pygame.Rect(x - w // 2, y, w, h)
        self.colour = colour
        self.alive  = True

    def update(self, scroll_speed):
        """Move downward with the road scroll."""
        self.rect.y += scroll_speed
        if self.rect.top > SCREEN_H:
            self.alive = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect, border_radius=4)


# ── Player car ────────────────────────────────────────────────────────────────

class Player:
    W, H = 40, 70

    def __init__(self, colour):
        self.colour   = colour
        self.lane     = 1                        # current lane index (0–3)
        self.x        = float(lane_x(self.lane))
        self.y        = SCREEN_H - 130
        self.rect     = pygame.Rect(0, 0, self.W, self.H)
        self._sync_rect()

        # Power-up state
        self.shield_active = False
        self.nitro_active  = False
        self.nitro_timer   = 0       # frames remaining
        self.nitro_boost   = 0       # extra scroll speed

    def _sync_rect(self):
        self.rect.centerx = int(self.x)
        self.rect.y       = self.y

    def move(self, direction, road_x, road_right):
        """Move left (-1) or right (+1) one lane."""
        self.lane = max(0, min(NUM_LANES - 1, self.lane + direction))
        target_x  = float(lane_x(self.lane))
        self.x    = target_x        # instant snap; smooth lerp optional
        self._sync_rect()

    def update(self):
        """Tick nitro timer."""
        if self.nitro_active:
            self.nitro_timer -= 1
            if self.nitro_timer <= 0:
                self.nitro_active = False
                self.nitro_boost  = 0

    def draw(self, surface):
        # Car body
        pygame.draw.rect(surface, self.colour, self.rect, border_radius=6)
        # Windshield
        ws = pygame.Rect(self.rect.x + 6, self.rect.y + 8, self.W - 12, 20)
        pygame.draw.rect(surface, CYAN, ws, border_radius=3)
        # Wheels
        for wx, wy in [(self.rect.left - 6, self.rect.y + 8),
                       (self.rect.right,     self.rect.y + 8),
                       (self.rect.left - 6,  self.rect.bottom - 24),
                       (self.rect.right,      self.rect.bottom - 24)]:
            pygame.draw.rect(surface, BLACK, (wx, wy, 8, 16), border_radius=3)
        # Shield aura
        if self.shield_active:
            pygame.draw.ellipse(surface, CYAN,
                                self.rect.inflate(20, 20), 3)
        # Nitro flame
        if self.nitro_active:
            for i in range(3):
                fx = self.rect.centerx + random.randint(-8, 8)
                fy = self.rect.bottom + random.randint(4, 18)
                pygame.draw.circle(surface, ORANGE, (fx, fy), random.randint(4, 8))


# ── Enemy car ─────────────────────────────────────────────────────────────────

class EnemyCar(RoadSprite):
    W, H = 40, 70
    COLOURS = [(180, 30, 30), (30, 90, 180), (80, 160, 80), (140, 60, 180)]

    def __init__(self, lane):
        colour = random.choice(self.COLOURS)
        super().__init__(lane_x(lane), -self.H, self.W, self.H, colour)
        self.lane = lane

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect, border_radius=6)
        ws = pygame.Rect(self.rect.x + 6, self.rect.y + 8, self.W - 12, 20)
        pygame.draw.rect(surface, (150, 220, 255), ws, border_radius=3)
        # Rear lights
        for lx in [self.rect.left + 4, self.rect.right - 12]:
            pygame.draw.rect(surface, RED, (lx, self.rect.bottom - 14, 8, 10), border_radius=2)


# ── Coin ──────────────────────────────────────────────────────────────────────

class Coin(RoadSprite):
    """Weighted coin: value 1 (gold), 3 (silver-blue), or 5 (purple)."""

    WEIGHT_PROPS = {
        1: {"colour": (255, 215, 0),   "radius": 10, "prob": 0.60},
        3: {"colour": (150, 200, 255), "radius": 12, "prob": 0.30},
        5: {"colour": (220, 130, 255), "radius": 14, "prob": 0.10},
    }

    def __init__(self, lane):
        # Pick weight by probability
        roll = random.random()
        cumulative = 0
        self.value = 1
        for w, props in self.WEIGHT_PROPS.items():
            cumulative += props["prob"]
            if roll <= cumulative:
                self.value = w
                break
        props  = self.WEIGHT_PROPS[self.value]
        self.radius = props["radius"]
        # Use parent's rect as a stand-in; draw circle separately
        super().__init__(lane_x(lane), -self.radius * 2,
                         self.radius * 2, self.radius * 2, props["colour"])

    def draw(self, surface):
        cx = self.rect.centerx
        cy = self.rect.centery
        pygame.draw.circle(surface, self.colour, (cx, cy), self.radius)
        pygame.draw.circle(surface, WHITE, (cx, cy), self.radius, 2)
        # Value label
        fnt = pygame.font.SysFont("consolas", 12, bold=True)
        lbl = fnt.render(str(self.value), True, BLACK)
        surface.blit(lbl, lbl.get_rect(center=(cx, cy)))


# ── Road obstacle ─────────────────────────────────────────────────────────────

class Obstacle(RoadSprite):
    """Barrier or pothole — collision ends the run (unless shield active)."""

    TYPES = {
        "barrier": {"colour": (220, 60,  60),  "w": 50, "h": 18},
        "pothole": {"colour": (30,  30,  30),  "w": 44, "h": 28},
    }

    def __init__(self, lane):
        kind   = random.choice(list(self.TYPES.keys()))
        props  = self.TYPES[kind]
        super().__init__(lane_x(lane), -props["h"], props["w"], props["h"], props["colour"])
        self.kind = kind

    def draw(self, surface):
        if self.kind == "barrier":
            pygame.draw.rect(surface, self.colour, self.rect, border_radius=4)
            # Hazard stripes
            stripe_w = 10
            for i in range(self.rect.width // stripe_w):
                if i % 2 == 0:
                    sx = self.rect.x + i * stripe_w
                    pygame.draw.rect(surface, YELLOW,
                                     (sx, self.rect.y, stripe_w, self.rect.height))
        else:
            # Pothole — dark ellipse
            pygame.draw.ellipse(surface, self.colour, self.rect)
            pygame.draw.ellipse(surface, (10, 10, 10), self.rect.inflate(-8, -8))


# ── Lane hazards (static overlays) ────────────────────────────────────────────

class LaneHazard(RoadSprite):
    """
    Oil spill (slows player) or slow-zone (blue).
    These are wide, tile vertically, and scroll with the road.
    """

    TYPES = {
        "oil":   {"colour": (20, 20, 80, 160),   "effect": "slow",  "h": 60},
        "nitro": {"colour": (0,  220, 180, 140),  "effect": "boost", "h": 50},
    }

    def __init__(self, lane, kind="oil"):
        props = self.TYPES[kind]
        # Lane-wide hazard
        super().__init__(lane_x(lane), -props["h"], LANE_W - 4, props["h"], props["colour"][:3])
        self.kind   = kind
        self.effect = props["effect"]
        self.alpha  = props["colour"][3] if len(props["colour"]) == 4 else 200

    def draw(self, surface):
        # Draw as semi-transparent overlay using a temp surface
        s = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        s.fill((*self.colour, self.alpha))
        surface.blit(s, self.rect.topleft)
        lbl_fnt = pygame.font.SysFont("consolas", 11, bold=True)
        icon = "🛢 OIL" if self.kind == "oil" else "⚡ BOOST"
        lbl  = lbl_fnt.render(icon, True, WHITE)
        surface.blit(lbl, lbl.get_rect(center=self.rect.center))


# ── Power-up ──────────────────────────────────────────────────────────────────

class PowerUp(RoadSprite):
    """
    Collectible power-up.  Types: nitro, shield, repair.
    Disappears after POWERUP_INTERVAL frames if uncollected.
    """

    PROPS = {
        "nitro":  {"colour": ORANGE,  "label": "⚡N", "w": 34, "h": 34},
        "shield": {"colour": CYAN,    "label": "🛡S", "w": 34, "h": 34},
        "repair": {"colour": GREEN,   "label": "🔧R", "w": 34, "h": 34},
    }

    def __init__(self, lane, kind):
        props = self.PROPS[kind]
        super().__init__(lane_x(lane), -props["h"], props["w"], props["h"], props["colour"])
        self.kind  = kind
        self.ttl   = POWERUP_INTERVAL     # frames until it disappears

    def update(self, scroll_speed):
        super().update(scroll_speed)
        self.ttl -= 1
        if self.ttl <= 0:
            self.alive = False

    def draw(self, surface):
        # Glowing background
        pygame.draw.rect(surface, self.colour, self.rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=8)
        fnt = pygame.font.SysFont("consolas", 14, bold=True)
        lbl = fnt.render(self.PROPS[self.kind]["label"], True, BLACK)
        surface.blit(lbl, lbl.get_rect(center=self.rect.center))


# ── HUD ───────────────────────────────────────────────────────────────────────

class HUD:
    """Renders all on-screen info (coins, score, distance, level, power-up)."""

    def __init__(self, screen):
        self.screen  = screen
        self.font    = pygame.font.SysFont("consolas", 22, bold=True)
        self.small_f = pygame.font.SysFont("consolas", 16)

    def draw(self, coins, score, distance, level, active_powerup, powerup_timer):
        W = self.screen.get_width()

        # Top-left: score + level
        self._text(f"Score: {score}", 10, 10, YELLOW)
        self._text(f"Level: {level}", 10, 36, WHITE)

        # Top-right: coins
        self._text(f"Coins: {coins}", W - 150, 10, (255, 215, 0))

        # Distance (centered top)
        self._text(f"{distance} m", W // 2 - 40, 10, GREEN)

        # Active power-up (bottom-left)
        if active_powerup:
            secs = max(0, powerup_timer // 60)
            label = f"[{active_powerup.upper()}]  {secs}s" if secs > 0 else f"[{active_powerup.upper()}]"
            col = {"nitro": ORANGE, "shield": CYAN, "repair": GREEN}.get(active_powerup, WHITE)
            self._text(label, 10, SCREEN_H - 36, col)

    def _text(self, txt, x, y, colour):
        lbl = self.font.render(txt, True, colour)
        self.screen.blit(lbl, (x, y))


# ── Road renderer ─────────────────────────────────────────────────────────────

class Road:
    """Scrolling road with lane markings."""

    STRIPE_H    = 60
    STRIPE_GAP  = 40

    def __init__(self):
        self.offset = 0     # vertical scroll offset

    def update(self, speed):
        self.offset = (self.offset + speed) % (self.STRIPE_H + self.STRIPE_GAP)

    def draw(self, surface):
        # Grass on sides
        surface.fill(GRASS_COL)
        # Road surface
        pygame.draw.rect(surface, ROAD_COL, (ROAD_X, 0, ROAD_W, SCREEN_H))
        # Road edges
        pygame.draw.rect(surface, WHITE, (ROAD_X, 0, 4, SCREEN_H))
        pygame.draw.rect(surface, WHITE, (ROAD_X + ROAD_W - 4, 0, 4, SCREEN_H))
        # Lane dividers (dashed)
        for lane in range(1, NUM_LANES):
            lx = ROAD_X + lane * LANE_W
            y  = -self.STRIPE_GAP + self.offset
            while y < SCREEN_H:
                pygame.draw.rect(surface, LINE_COL, (lx - 2, y, 4, self.STRIPE_H))
                y += self.STRIPE_H + self.STRIPE_GAP


# ── Main game class ───────────────────────────────────────────────────────────

class RacerGame:
    """
    One complete game session.
    Call run() → returns (score, distance, coins) when the session ends.
    """

    def __init__(self, screen, settings, username):
        self.screen   = screen
        self.settings = settings
        self.username = username
        self.clock    = pygame.time.Clock()

        diff = settings.get("difficulty", "normal")
        p    = DIFF_PARAMS.get(diff, DIFF_PARAMS["normal"])
        self.base_speed         = p["base_speed"]
        self.enemy_interval     = p["enemy_interval"]
        self.obstacle_interval  = p["obstacle_interval"]
        self.coin_interval      = p["coin_interval"]

        car_colour = CAR_COLOURS.get(settings.get("car_color", "red"), RED)

        self.road    = Road()
        self.player  = Player(car_colour)
        self.hud     = HUD(screen)

        # Entity lists
        self.enemies   = []
        self.coins     = []
        self.obstacles = []
        self.hazards   = []
        self.powerups  = []

        # Counters
        self.score         = 0
        self.coin_count    = 0   # number of coins (for display)
        self.distance      = 0   # in metres (incremented each frame)
        self.level         = 1
        self.scroll_speed  = float(self.base_speed)

        # Power-up tracking (only one active at a time)
        self.active_powerup  = None   # "nitro" | "shield" | "repair" | None
        self.powerup_timer   = 0

        # Spawn timers
        self._enemy_timer    = 0
        self._coin_timer     = 0
        self._obstacle_timer = 0
        self._hazard_timer   = 0
        self._powerup_timer  = 0

        self.running = True

    # ── Speed helper ─────────────────────────────────────────────────────────

    def _current_speed(self):
        boost = self.player.nitro_boost if self.player.nitro_active else 0
        return self.scroll_speed + boost

    # ── Safe spawn check ──────────────────────────────────────────────────────

    def _safe_lane(self, excluded_lane=None):
        """Pick a random lane that isn't currently occupied near the top."""
        lanes = list(range(NUM_LANES))
        if excluded_lane is not None:
            lanes = [l for l in lanes if l != excluded_lane]
        random.shuffle(lanes)
        for lane in lanes:
            lx = lane_x(lane)
            # Check nothing is in the top 120 px of that lane
            candidate = pygame.Rect(lx - 25, 0, 50, 120)
            occupied = any(
                candidate.colliderect(e.rect)
                for e in self.enemies + self.obstacles
            )
            if not occupied:
                return lane
        return random.randint(0, NUM_LANES - 1)   # fallback

    # ── Difficulty scaling ────────────────────────────────────────────────────

    def _update_difficulty(self):
        """Level up every 500 m; increase speed and spawn rates."""
        new_level = 1 + self.distance // 500
        if new_level > self.level:
            self.level        = new_level
            self.scroll_speed = self.base_speed + (self.level - 1) * 0.8
            self.enemy_interval    = max(30, self.enemy_interval    - 5 * (self.level - 1))
            self.obstacle_interval = max(50, self.obstacle_interval - 8 * (self.level - 1))

    # ── Power-up activation ───────────────────────────────────────────────────

    def _activate_powerup(self, kind):
        """Apply the effect of a collected power-up."""
        if kind == "nitro":
            self.player.nitro_active = True
            self.player.nitro_timer  = 60 * 4   # 4 seconds
            self.player.nitro_boost  = 4
            self.active_powerup      = "nitro"
            self.powerup_timer       = 60 * 4
        elif kind == "shield":
            self.player.shield_active = True
            self.active_powerup       = "shield"
            self.powerup_timer        = 0        # infinite until hit
        elif kind == "repair":
            # Repair: clear one obstacle near the player
            near = [o for o in self.obstacles
                    if abs(o.rect.centery - self.player.rect.centery) < 200]
            if near:
                near[0].alive = False
            self.active_powerup  = "repair"
            self.powerup_timer   = 60            # show "REPAIR" for 1 s

    # ── Main loop ─────────────────────────────────────────────────────────────

    def run(self):
        while self.running:
            self.clock.tick(60)
            self._handle_events()
            self._update()
            self._draw()
        return self.score, self.distance, self.coin_count

    # ── Events ────────────────────────────────────────────────────────────────

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    self.player.move(-1, ROAD_X, ROAD_X + ROAD_W)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.player.move(1, ROAD_X, ROAD_X + ROAD_W)
                elif event.key == pygame.K_ESCAPE:
                    self.running = False   # abort run (treated as game over)

    # ── Update ────────────────────────────────────────────────────────────────

    def _update(self):
        speed = self._current_speed()

        # Distance in metres (1 frame ≈ 0.1 m at base speed 6)
        self.distance += int(speed * 10) // 60 + (1 if random.random() < 0.5 else 0)

        self._update_difficulty()
        self.road.update(speed)
        self.player.update()

        # ── Spawn timers ──
        self._enemy_timer    += 1
        self._coin_timer     += 1
        self._obstacle_timer += 1
        self._hazard_timer   += 1
        self._powerup_timer  += 1

        if self._enemy_timer >= self.enemy_interval:
            self._enemy_timer = 0
            lane = self._safe_lane()
            self.enemies.append(EnemyCar(lane))

        if self._coin_timer >= self.coin_interval:
            self._coin_timer = 0
            lane = random.randint(0, NUM_LANES - 1)
            self.coins.append(Coin(lane))

        if self._obstacle_timer >= self.obstacle_interval:
            self._obstacle_timer = 0
            lane = self._safe_lane()
            self.obstacles.append(Obstacle(lane))

        if self._hazard_timer >= 180:
            self._hazard_timer = 0
            lane = random.randint(0, NUM_LANES - 1)
            kind = random.choice(["oil", "nitro"])
            self.hazards.append(LaneHazard(lane, kind))

        if self._powerup_timer >= POWERUP_INTERVAL:
            self._powerup_timer = 0
            lane = random.randint(0, NUM_LANES - 1)
            kind = random.choice(["nitro", "shield", "repair"])
            self.powerups.append(PowerUp(lane, kind))

        # ── Update entities ──
        for lst in (self.enemies, self.coins, self.obstacles, self.hazards, self.powerups):
            for obj in lst:
                obj.update(speed)

        # ── Prune dead entities ──
        for attr in ("enemies", "coins", "obstacles", "hazards", "powerups"):
            setattr(self, attr, [o for o in getattr(self, attr) if o.alive])

        # ── Power-up timer display countdown ──
        if self.powerup_timer > 0:
            self.powerup_timer -= 1
            if self.powerup_timer == 0 and self.active_powerup != "shield":
                self.active_powerup = None

        # ── Collision: coins ──
        for coin in self.coins[:]:
            if self.player.rect.colliderect(coin.rect):
                self.coin_count += 1
                self.score      += coin.value * 10
                coin.alive = False

        # ── Collision: power-ups ──
        for pu in self.powerups[:]:
            if self.player.rect.colliderect(pu.rect):
                self._activate_powerup(pu.kind)
                pu.alive = False

        # ── Collision: obstacles ──
        for obs in self.obstacles[:]:
            if self.player.rect.colliderect(obs.rect):
                if self.player.shield_active:
                    self.player.shield_active = False
                    self.active_powerup       = None
                    obs.alive = False
                else:
                    self.running = False   # game over
                    return

        # ── Collision: enemy cars ──
        for enemy in self.enemies[:]:
            if self.player.rect.colliderect(enemy.rect):
                if self.player.shield_active:
                    self.player.shield_active = False
                    self.active_powerup       = None
                    enemy.alive = False
                else:
                    self.running = False
                    return

        # ── Lane hazards ──
        for hz in self.hazards:
            if self.player.rect.colliderect(hz.rect):
                if hz.effect == "slow":
                    # Momentarily halve the effective speed via clamping
                    self.scroll_speed = max(2, self.scroll_speed * 0.98)
                elif hz.effect == "boost" and not self.player.nitro_active:
                    self._activate_powerup("nitro")

        # ── Score: distance bonus (every 100 m) ──
        if self.distance > 0 and self.distance % 100 == 0:
            self.score += 50

    # ── Draw ──────────────────────────────────────────────────────────────────

    def _draw(self):
        self.road.draw(self.screen)

        for lst in (self.hazards, self.coins, self.obstacles, self.powerups, self.enemies):
            for obj in lst:
                obj.draw(self.screen)

        self.player.draw(self.screen)

        self.hud.draw(
            self.coin_count, self.score, self.distance,
            self.level, self.active_powerup, self.powerup_timer
        )

        pygame.display.flip()