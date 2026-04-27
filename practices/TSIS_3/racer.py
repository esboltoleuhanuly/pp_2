import pygame
import random
import sys

# ─── Colors ───────────────────────────────────────────────────────────────────
WHITE      = (255, 255, 255)
BLACK      = (0,   0,   0  )
YELLOW     = (255, 220, 0  )
GOLD       = (218, 165, 32 )
RED        = (220, 50,  50 )
GRAY       = (50,  50,  50 )
DARK_GRAY  = (30,  30,  30 )
ROAD_COLOR = (60,  60,  60 )
CYAN       = (0,   210, 255)
MAGENTA    = (210, 0,   210)
GREEN      = (50,  200, 50 )
ORANGE     = (255, 140, 0  )
LIGHT_BLUE = (135, 206, 235)
LIGHT_GRAY = (180, 180, 180)
PURPLE     = (120, 0,   180)
OIL_COLOR  = (30,  20,  80,  180)

SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 600

ROAD_LEFT   = 30
ROAD_RIGHT  = SCREEN_WIDTH - 30
ROAD_WIDTH  = ROAD_RIGHT - ROAD_LEFT
LANE_CENTERS = [80, 200, 320]
LANE_WIDTH   = 120          # width of each driving lane in pixels

CAR_COLORS = {
    "blue":  (50,  100, 255),
    "red":   (220, 50,  50 ),
    "green": (50,  200, 50 ),
}

DIFFICULTY = {
    "easy":   {"base_speed": 3, "coin_threshold": 7, "max_enemies": 1,
                "obs_interval": 5500, "pu_interval": 8000},
    "normal": {"base_speed": 5, "coin_threshold": 5, "max_enemies": 2,
                "obs_interval": 3500, "pu_interval": 10000},
    "hard":   {"base_speed": 7, "coin_threshold": 3, "max_enemies": 3,
                "obs_interval": 2000, "pu_interval": 12000},
}

INVINCIBILITY_MS = 500   # ms of brief invincibility after a hit (not god-mode)
TOTAL_DISTANCE   = 5000  # units to complete a run


# ─── Helper: draw a mini car surface ──────────────────────────────────────────
def _make_car_surf(w, h, body_color, window_color=LIGHT_BLUE):
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    # body
    pygame.draw.rect(surf, body_color, (4, 8, w - 8, h - 12), border_radius=4)
    # windshield
    pygame.draw.rect(surf, window_color, (7, 12, w - 14, 14), border_radius=2)
    # wheels
    for wx, wy in [(0, 10), (w - 8, 10), (0, h - 24), (w - 8, h - 24)]:
        pygame.draw.rect(surf, BLACK, (wx, wy, 8, 14), border_radius=3)
    return surf


# ─── Player ───────────────────────────────────────────────────────────────────
class Player(pygame.sprite.Sprite):
    MOVE_SPEED = 5

    def __init__(self, color_name="blue"):
        super().__init__()
        self.color_name   = color_name
        self.body_color   = CAR_COLORS.get(color_name, CAR_COLORS["blue"])
        self.health       = 3
        self.shield       = False
        self.nitro        = False
        self.nitro_end    = 0
        self.hit_time     = 0          # invincibility start
        self._rebuild_image()
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, 520))

    def _rebuild_image(self):
        base = _make_car_surf(40, 60, self.body_color)
        if self.shield:
            pygame.draw.rect(base, CYAN, base.get_rect(), 3, border_radius=4)
        if self.nitro:
            # draw exhaust flames at bottom
            for fx in [8, 28]:
                pygame.draw.polygon(base, ORANGE, [(fx, 60), (fx + 6, 60), (fx + 3, 72)])
        self.image = base

    def update(self):
        now = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        spd = self.MOVE_SPEED
        if self.nitro:
            spd = int(spd * 1.7)
        if now > self.nitro_end and self.nitro:
            self.nitro = False
            self._rebuild_image()

        if keys[pygame.K_LEFT]  and self.rect.left  > ROAD_LEFT:
            self.rect.move_ip(-spd, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < ROAD_RIGHT:
            self.rect.move_ip( spd, 0)

        # Flicker every 80 ms during brief post-hit invincibility.
        # Nitro does NOT grant invincibility — only a hit triggers it.
        invincible = self.hit_time > 0 and (now - self.hit_time < INVINCIBILITY_MS)
        self.image.set_alpha(60 if (invincible and (now // 80) % 2 == 0) else 255)

    def activate_powerup(self, kind):
        """Replace current powerup effect with the new one."""
        self.nitro  = False
        self.shield = False
        if kind == "nitro":
            self.nitro     = True
            self.nitro_end = pygame.time.get_ticks() + 4000
        elif kind == "shield":
            self.shield = True
        elif kind == "repair":
            self.health = min(3, self.health + 1)
        self._rebuild_image()

    def take_hit(self):
        """Returns True if the player is now dead."""
        now = pygame.time.get_ticks()
        if now - self.hit_time < INVINCIBILITY_MS:
            return False          # still invincible
        if self.shield:
            self.shield = False
            self._rebuild_image()
            self.hit_time = now
            return False
        self.health  -= 1
        self.hit_time = now
        self._rebuild_image()
        return self.health <= 0

    def slow_down(self, ms=2000):
        """Oil-spill slow: temporarily reduce move speed via a flag."""
        self._slow_end = pygame.time.get_ticks() + ms

    def is_slowed(self):
        return pygame.time.get_ticks() < getattr(self, "_slow_end", 0)

    def nitro_remaining(self):
        if not self.nitro:
            return 0
        return max(0, (self.nitro_end - pygame.time.get_ticks()) / 1000)

    def powerup_hud(self):
        if self.nitro:
            return f"NITRO  {self.nitro_remaining():.1f}s", CYAN
        if self.shield:
            return "SHIELD  active", MAGENTA
        return None, None


# ─── Traffic car ──────────────────────────────────────────────────────────────
class TrafficCar(pygame.sprite.Sprite):
    _COLORS = [(180, 30,  30), (200, 100, 0), (120, 0, 120), (0, 120, 120), (80, 80, 160)]

    def __init__(self, speed, player_rect=None):
        super().__init__()
        self.speed = speed
        color = random.choice(self._COLORS)
        self.image = _make_car_surf(40, 68, color)
        self.rect  = self.image.get_rect()
        self._safe_place(player_rect)

    def _safe_place(self, avoid):
        for _ in range(20):
            x = random.choice(LANE_CENTERS)
            y = random.randint(-350, -60)
            self.rect.center = (x, y)
            if avoid is None or not self.rect.inflate(30, 30).colliderect(avoid):
                return
        self.rect.center = (random.choice(LANE_CENTERS), -200)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT + 20:
            self.kill()


# ─── Coin ─────────────────────────────────────────────────────────────────────
class Coin(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.weight = random.randint(1, 5)
        color = GOLD if self.weight > 3 else YELLOW
        self.image = pygame.Surface((22, 22), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (11, 11), 11)
        pygame.draw.circle(self.image, (max(color[0]-40,0), max(color[1]-40,0), 0), (11, 11), 6)
        # weight label
        f = pygame.font.SysFont("Verdana", 9, bold=True)
        lbl = f.render(str(self.weight), True, BLACK)
        self.image.blit(lbl, lbl.get_rect(center=(11, 11)))
        self.rect  = self.image.get_rect()
        self.speed = speed
        x = random.choice(LANE_CENTERS) + random.randint(-18, 18)
        self.rect.center = (x, random.randint(-400, -30))

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# ─── Power-Up ─────────────────────────────────────────────────────────────────
POWERUP_CFG = {
    "nitro":  {"color": CYAN,    "letter": "N", "tc": BLACK},
    "shield": {"color": MAGENTA, "letter": "S", "tc": WHITE},
    "repair": {"color": GREEN,   "letter": "R", "tc": WHITE},
}

class PowerUp(pygame.sprite.Sprite):
    LIFETIME = 8000

    def __init__(self, speed, kind=None):
        super().__init__()
        self.kind  = kind or random.choice(list(POWERUP_CFG))
        cfg        = POWERUP_CFG[self.kind]
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(self.image, cfg["color"], (0, 0, 32, 32), border_radius=8)
        pygame.draw.rect(self.image, WHITE,        (0, 0, 32, 32), 2, border_radius=8)
        f   = pygame.font.SysFont("Verdana", 18, bold=True)
        lbl = f.render(cfg["letter"], True, cfg["tc"])
        self.image.blit(lbl, lbl.get_rect(center=(16, 16)))
        self.rect       = self.image.get_rect()
        self.speed      = speed
        self.spawn_tick = pygame.time.get_ticks()
        x = random.choice(LANE_CENTERS)
        self.rect.center = (x, random.randint(-300, -60))

    def update(self):
        self.rect.move_ip(0, self.speed)
        expired = pygame.time.get_ticks() - self.spawn_tick > self.LIFETIME
        if self.rect.top > SCREEN_HEIGHT or expired:
            self.kill()


# ─── Obstacle ─────────────────────────────────────────────────────────────────
class Obstacle(pygame.sprite.Sprite):
    """pothole | oil_spill | barrier"""

    def __init__(self, speed, kind=None):
        super().__init__()
        self.kind  = kind or random.choice(["pothole", "oil_spill", "barrier"])
        self.speed = speed

        if self.kind == "pothole":
            self.image = pygame.Surface((38, 22), pygame.SRCALPHA)
            pygame.draw.ellipse(self.image, DARK_GRAY, (0, 0, 38, 22))
            pygame.draw.ellipse(self.image, BLACK,     (5, 4, 28, 14))

        elif self.kind == "oil_spill":
            self.image = pygame.Surface((62, 32), pygame.SRCALPHA)
            s = pygame.Surface((62, 32), pygame.SRCALPHA)
            pygame.draw.ellipse(s, (30, 20, 90, 160), (0, 0, 62, 32))
            # iridescent shimmer
            pygame.draw.ellipse(s, (80, 40, 180, 80), (10, 6, 30, 14))
            self.image = s

        elif self.kind == "barrier":
            self.image = pygame.Surface((90, 22), pygame.SRCALPHA)
            pygame.draw.rect(self.image, ORANGE, (0, 0, 90, 22), border_radius=4)
            for bx in range(0, 90, 18):
                pygame.draw.rect(self.image, BLACK, (bx, 0, 9, 22))

        self.rect = self.image.get_rect()
        lane = random.choice(LANE_CENTERS)
        self.rect.center = (lane, random.randint(-350, -50))

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# ─── Lane Hazard (slow zone strip) ────────────────────────────────────────────
class LaneHazard(pygame.sprite.Sprite):
    """A coloured band across one lane that slows the player."""

    def __init__(self, speed):
        super().__init__()
        self.speed = speed
        self.image = pygame.Surface((LANE_WIDTH - 10, 28), pygame.SRCALPHA)
        # orange-tinted slow strip
        pygame.draw.rect(self.image, (200, 120, 0, 160), (0, 0, LANE_WIDTH - 10, 28), border_radius=4)
        f   = pygame.font.SysFont("Verdana", 10, bold=True)
        lbl = f.render("SLOW", True, WHITE)
        self.image.blit(lbl, lbl.get_rect(center=((LANE_WIDTH - 10)//2, 14)))
        self.rect = self.image.get_rect()
        lane = random.choice(LANE_CENTERS)
        self.rect.center = (lane, random.randint(-400, -60))

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# ─── Nitro Strip (road event) ─────────────────────────────────────────────────
class NitroStrip(pygame.sprite.Sprite):
    """Full-width cyan dashes: gives a 3-second nitro boost on contact."""

    def __init__(self, speed):
        super().__init__()
        self.speed = speed
        w = ROAD_WIDTH - 10
        self.image = pygame.Surface((w, 20), pygame.SRCALPHA)
        for ix in range(0, w, 22):
            pygame.draw.rect(self.image, CYAN, (ix, 0, 16, 20), border_radius=3)
        f   = pygame.font.SysFont("Verdana", 9, bold=True)
        lbl = f.render("NITRO STRIP", True, BLACK)
        self.image.blit(lbl, lbl.get_rect(center=(w // 2, 10)))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, random.randint(-400, -60))

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# ─── Game class ───────────────────────────────────────────────────────────────
class Game:
    def __init__(self, screen, settings, username):
        self.screen   = screen
        self.settings = settings
        self.username = username
        self.clock    = pygame.time.Clock()
        self.font     = pygame.font.SysFont("Verdana", 18)
        self.sfont    = pygame.font.SysFont("Verdana", 14)

        # Difficulty config
        diff     = settings.get("difficulty", "normal")
        cfg      = DIFFICULTY[diff]
        self.enemy_speed     = cfg["base_speed"]
        self.coin_threshold  = cfg["coin_threshold"]
        self.max_enemies     = cfg["max_enemies"]
        self.obs_interval    = cfg["obs_interval"]
        self.pu_interval     = cfg["pu_interval"]

        # Player
        self.player = Player(settings.get("car_color", "blue"))

        # Sprite groups
        self.all_sprites  = pygame.sprite.Group()
        self.enemies      = pygame.sprite.Group()
        self.coins_grp    = pygame.sprite.Group()
        self.powerups_grp = pygame.sprite.Group()
        self.obstacles_grp= pygame.sprite.Group()
        self.hazards_grp  = pygame.sprite.Group()
        self.events_grp   = pygame.sprite.Group()

        self.all_sprites.add(self.player)

        for _ in range(self.max_enemies):
            self._spawn_enemy()

        # Scoring
        self.score       = 0
        self.coins_count = 0
        self.distance    = 0.0
        self.pu_bonus    = 0

        # Road animation
        self.line_y = 0

        # Timers
        now = pygame.time.get_ticks()
        self.t_obstacle = now
        self.t_powerup  = now
        self.t_event    = now
        self.t_hazard   = now
        self.hazard_interval = 7000

    # ── Spawners ──────────────────────────────────────────────────────────────
    def _spawn_enemy(self):
        e = TrafficCar(self.enemy_speed, self.player.rect)
        self.enemies.add(e)
        self.all_sprites.add(e)

    def _spawn_coin(self):
        c = Coin(self.enemy_speed)
        self.coins_grp.add(c)
        self.all_sprites.add(c)

    def _spawn_obstacle(self):
        o = Obstacle(self.enemy_speed)
        self.obstacles_grp.add(o)
        self.all_sprites.add(o)

    def _spawn_powerup(self):
        if len(self.powerups_grp) == 0:   # only one on-screen at a time
            p = PowerUp(self.enemy_speed)
            self.powerups_grp.add(p)
            self.all_sprites.add(p)

    def _spawn_nitro_strip(self):
        ns = NitroStrip(self.enemy_speed)
        self.events_grp.add(ns)
        self.all_sprites.add(ns)

    def _spawn_hazard(self):
        h = LaneHazard(self.enemy_speed)
        self.hazards_grp.add(h)
        self.all_sprites.add(h)

    # ── Drawing ───────────────────────────────────────────────────────────────
    def _draw_road(self):
        self.screen.fill(GRAY)
        pygame.draw.rect(self.screen, ROAD_COLOR,
                         (ROAD_LEFT, 0, ROAD_WIDTH, SCREEN_HEIGHT))

        # Moving lane dashes
        self.line_y = (self.line_y + self.enemy_speed) % 100
        for y in range(-100, SCREEN_HEIGHT, 100):
            cy = y + self.line_y
            # Centre divider
            pygame.draw.rect(self.screen, WHITE,
                             (SCREEN_WIDTH // 2 - 4, cy, 8, 50))
            # Outer lane guides (lighter)
            for lx in [SCREEN_WIDTH // 4, 3 * SCREEN_WIDTH // 4]:
                pygame.draw.rect(self.screen, LIGHT_GRAY,
                                 (lx - 3, cy, 6, 40))

        # Road edges
        pygame.draw.rect(self.screen, WHITE, (ROAD_LEFT,     0, 4, SCREEN_HEIGHT))
        pygame.draw.rect(self.screen, WHITE, (ROAD_RIGHT - 4, 0, 4, SCREEN_HEIGHT))

    def _draw_hud(self):
        # Health hearts
        for i in range(self.player.health):
            pygame.draw.polygon(self.screen, RED,
                [(10 + i*24 + 6,  10),
                 (10 + i*24,      16),
                 (10 + i*24 + 6,  24),
                 (10 + i*24 + 12, 16)])

        # Score (top-right)
        sc = self.font.render(f"Score: {self.score}", True, GOLD)
        self.screen.blit(sc, (SCREEN_WIDTH - sc.get_width() - 8, 8))

        # Speed (below hearts)
        spd = self.sfont.render(f"Speed: {self.enemy_speed}", True, WHITE)
        self.screen.blit(spd, (8, 36))

        # Coins
        coins = self.sfont.render(f"Coins: {self.coins_count}", True, YELLOW)
        self.screen.blit(coins, (8, 56))

        # Distance bar
        dist_pct = min(self.distance / TOTAL_DISTANCE, 1.0)
        bar_x, bar_y, bar_w, bar_h = SCREEN_WIDTH // 2 - 60, 8, 120, 10
        pygame.draw.rect(self.screen, DARK_GRAY, (bar_x, bar_y, bar_w, bar_h), border_radius=4)
        pygame.draw.rect(self.screen, GREEN,
                         (bar_x, bar_y, int(bar_w * dist_pct), bar_h), border_radius=4)
        dist_lbl = self.sfont.render(f"{int(self.distance)}/{TOTAL_DISTANCE}m", True, LIGHT_GRAY)
        self.screen.blit(dist_lbl, dist_lbl.get_rect(centerx=SCREEN_WIDTH // 2, y=22))

        # Active power-up indicator
        pu_txt, pu_col = self.player.powerup_hud()
        if pu_txt:
            pu_surf = self.font.render(pu_txt, True, pu_col)
            pygame.draw.rect(self.screen, (0, 0, 0, 140),
                             pu_surf.get_rect(centerx=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT - 40)
                             .inflate(14, 6), border_radius=6)
            self.screen.blit(pu_surf,
                             pu_surf.get_rect(centerx=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT - 40))

        # Player name top-center
        name_surf = self.sfont.render(self.username, True, LIGHT_GRAY)
        self.screen.blit(name_surf, name_surf.get_rect(centerx=SCREEN_WIDTH // 2, y=38))

    # ── Main loop ─────────────────────────────────────────────────────────────
    def run(self):
        """Returns (score, distance, coins) or None on quit."""
        result = None
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    result = (self.score, int(self.distance), self.coins_count)
                    running = False

            now = pygame.time.get_ticks()

            # ── Timed spawning ──────────────────────────────────────────────
            if len(self.coins_grp) < 2:
                self._spawn_coin()
            if len(self.enemies) < self.max_enemies:
                self._spawn_enemy()
            if now - self.t_obstacle > self.obs_interval:
                self._spawn_obstacle()
                self.t_obstacle = now
            if now - self.t_powerup > self.pu_interval:
                self._spawn_powerup()
                self.t_powerup = now
            if now - self.t_event > 15000:
                self._spawn_nitro_strip()
                self.t_event = now
            if now - self.t_hazard > self.hazard_interval:
                self._spawn_hazard()
                self.t_hazard = now

            # ── Draw road ───────────────────────────────────────────────────
            self._draw_road()

            # ── Update + draw all sprites ───────────────────────────────────
            # Remove player from group update to avoid double-move
            non_player = [s for s in self.all_sprites if s is not self.player]
            for s in non_player:
                s.update()

            # Player update (handles own input + nitro expiry)
            self.player.update()

            # Draw
            self.all_sprites.draw(self.screen)

            # ── Distance / score ────────────────────────────────────────────
            self.distance += self.enemy_speed * 0.05
            self.score = int(
                self.coins_count * 10
                + self.distance * 2
                + self.pu_bonus
            )

            # ── Coin collection ─────────────────────────────────────────────
            hit_coin = pygame.sprite.spritecollideany(self.player, self.coins_grp)
            if hit_coin:
                self.pu_bonus   += hit_coin.weight * 5
                self.coins_count += 1
                hit_coin.kill()
                if self.coins_count % self.coin_threshold == 0:
                    self.enemy_speed += 1
                    # Scale difficulty
                    if self.coins_count % (self.coin_threshold * 3) == 0:
                        self.max_enemies    = min(self.max_enemies + 1, 6)
                        self.obs_interval   = max(1200, self.obs_interval - 250)
                        self.hazard_interval= max(3000, self.hazard_interval - 500)

            # ── Power-up collection ─────────────────────────────────────────
            hit_pu = pygame.sprite.spritecollideany(self.player, self.powerups_grp)
            if hit_pu:
                self.player.activate_powerup(hit_pu.kind)
                self.pu_bonus += 50
                hit_pu.kill()

            # ── Nitro strip ─────────────────────────────────────────────────
            hit_ev = pygame.sprite.spritecollideany(self.player, self.events_grp)
            if hit_ev:
                self.player.nitro     = True
                self.player.nitro_end = now + 3000
                self.pu_bonus        += 20
                hit_ev.kill()   # remove strip so it doesn't re-trigger every frame

            # ── Lane hazard (slow) ──────────────────────────────────────────
            hit_hz = pygame.sprite.spritecollideany(self.player, self.hazards_grp)
            if hit_hz:
                self.player.slow_down(2000)

            # ── Obstacle collision ──────────────────────────────────────────
            hit_obs = pygame.sprite.spritecollideany(self.player, self.obstacles_grp)
            if hit_obs:
                if hit_obs.kind == "oil_spill":
                    self.player.slow_down(2500)
                else:
                    dead = self.player.take_hit()
                    hit_obs.kill()
                    if dead:
                        result  = (self.score, int(self.distance), self.coins_count)
                        running = False

            # ── Enemy collision ─────────────────────────────────────────────
            if pygame.sprite.spritecollideany(self.player, self.enemies):
                dead = self.player.take_hit()
                if dead:
                    result  = (self.score, int(self.distance), self.coins_count)
                    running = False

            # ── Finish line ─────────────────────────────────────────────────
            if self.distance >= TOTAL_DISTANCE:
                self.pu_bonus += 500    # completion bonus
                self.score = int(
                    self.coins_count * 10 + self.distance * 2 + self.pu_bonus
                )
                result  = (self.score, int(self.distance), self.coins_count)
                running = False

            self._draw_hud()
            pygame.display.update()
            self.clock.tick(60)

        return result