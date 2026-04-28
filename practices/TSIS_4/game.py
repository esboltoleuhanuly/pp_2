# game.py — snake gameplay (extends Practice 11 logic)

import pygame
import random
import time

from config import *


class Game:
    """
    Encapsulates one full snake session.
    Call .run() → returns (score, level) when the session ends.
    """

    def __init__(self, screen, clock, font, small_font, settings, personal_best: int):
        self.screen        = screen
        self.clock         = clock
        self.font          = font
        self.small_font    = small_font
        self.settings      = settings
        self.personal_best = personal_best
        self.snake_color   = tuple(settings.get('snake_color', list(GREEN)))

    # ── random-placement helpers ──────────────────────────────────────────────

    def _rand_pos(self, snake: list, blocked: list) -> list:
        """Random grid-aligned position not in snake or blocked list."""
        while True:
            pos = [
                random.randrange(0, WIDTH,  BLOCK_SIZE),
                random.randrange(0, HEIGHT, BLOCK_SIZE),
            ]
            if pos not in snake and pos not in blocked:
                return pos

    def _new_food(self, snake, blocked):
        """(pos, weight, expiry_time)  — weight 1-3, expires in 5 s."""
        weight     = random.randint(1, 3)
        pos        = self._rand_pos(snake, blocked)
        expiration = time.time() + 5
        return pos, weight, expiration

    def _new_poison(self, snake, blocked):
        return self._rand_pos(snake, blocked)

    def _new_powerup(self, snake, blocked):
        """(pos, kind, field_expiry_ticks)  — disappears from field after 8 s."""
        kind   = random.choice(['speed', 'slow', 'shield'])
        pos    = self._rand_pos(snake, blocked)
        expiry = pygame.time.get_ticks() + 8_000
        return pos, kind, expiry

    def _new_obstacles(self, snake: list, static_blocked: list, level: int) -> list:
        """
        Generate wall blocks starting at level 3.
        Count grows by 3 per level (capped at 20).
        Blocks are never placed within 3 cells of the snake head.
        """
        count     = min((level - 2) * 3, 20)
        obstacles = []
        head      = snake[0]
        attempts  = 0
        while len(obstacles) < count and attempts < 2_000:
            attempts += 1
            pos = [
                random.randrange(0, WIDTH,  BLOCK_SIZE),
                random.randrange(0, HEIGHT, BLOCK_SIZE),
            ]
            near_head = (abs(pos[0] - head[0]) <= BLOCK_SIZE * 3 and
                         abs(pos[1] - head[1]) <= BLOCK_SIZE * 3)
            if (pos not in snake and
                    pos not in static_blocked and
                    pos not in obstacles and
                    not near_head):
                obstacles.append(pos)
        return obstacles

    # ── drawing helpers ───────────────────────────────────────────────────────

    def _draw_grid(self):
        for x in range(0, WIDTH, BLOCK_SIZE):
            pygame.draw.line(self.screen, DARK_GRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, BLOCK_SIZE):
            pygame.draw.line(self.screen, DARK_GRAY, (0, y), (WIDTH, y))

    def _draw_hud(self, score, level, food_timer,
                  pu_active, pu_type, pu_end_ms, shield_active):
        food_left = max(0, int(food_timer - time.time()))
        hud = self.font.render(
            f"Score:{score}  Lv:{level}  Food:{food_left}s  PB:{self.personal_best}",
            True, WHITE
        )
        self.screen.blit(hud, (5, 5))

        if pu_active and pu_type:
            secs  = max(0, (pu_end_ms - pygame.time.get_ticks()) // 1_000)
            label = POWERUP_LABELS.get(pu_type, pu_type)
            pu_surf = self.small_font.render(
                f"[{label} {secs}s]", True, POWERUP_COLORS.get(pu_type, WHITE)
            )
            self.screen.blit(pu_surf, (5, 32))
        elif shield_active:
            self.screen.blit(
                self.small_font.render("[SHIELD active]", True, CYAN), (5, 32)
            )

    # ── main loop ─────────────────────────────────────────────────────────────

    def run(self):
        # ── state ──
        snake     = [[100, 60], [80, 60], [60, 60]]
        direction = 'RIGHT'
        nxt_dir   = 'RIGHT'
        obstacles = []

        # food (Practice 11 — weighted + timer)
        food_pos, food_weight, food_timer = self._new_food(snake, [])

        # poison food (Task 3.2)
        poison_pos = self._new_poison(snake, [food_pos])

        # power-up on field (Task 3.3)
        pu_pos        = None   # position on the grid
        pu_kind       = None   # 'speed' | 'slow' | 'shield'
        pu_field_exp  = None   # ticks until it disappears from field

        # active power-up effect
        pu_active     = False
        active_pu     = None
        pu_effect_end = 0      # ticks

        shield_active = False  # shield stays until triggered

        score         = 0
        level         = 1
        base_speed    = FPS
        current_speed = FPS

        # first power-up spawns 5–10 s after game start
        next_pu_spawn = pygame.time.get_ticks() + random.randint(5_000, 10_000)

        running = True
        while running:
            now_ms  = pygame.time.get_ticks()
            now_sec = time.time()

            # ── timers ──
            # food expires
            if now_sec > food_timer:
                blocked = [poison_pos] + obstacles + ([pu_pos] if pu_pos else [])
                food_pos, food_weight, food_timer = self._new_food(snake, blocked)

            # power-up disappears from field
            if pu_pos and now_ms > pu_field_exp:
                pu_pos = pu_kind = pu_field_exp = None

            # power-up effect ends
            if pu_active and now_ms > pu_effect_end:
                pu_active = False
                if active_pu in ('speed', 'slow'):
                    current_speed = base_speed
                active_pu = None

            # spawn new power-up if field is empty
            if pu_pos is None and now_ms >= next_pu_spawn:
                blocked      = [food_pos, poison_pos] + obstacles
                pu_pos, pu_kind, pu_field_exp = self._new_powerup(snake, blocked)
                next_pu_spawn = now_ms + random.randint(10_000, 20_000)

            # ── events ──
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); exit()
                if event.type == pygame.KEYDOWN:
                    k = event.key
                    if   k == pygame.K_UP    and direction != 'DOWN':  nxt_dir = 'UP'
                    elif k == pygame.K_DOWN  and direction != 'UP':    nxt_dir = 'DOWN'
                    elif k == pygame.K_LEFT  and direction != 'RIGHT': nxt_dir = 'LEFT'
                    elif k == pygame.K_RIGHT and direction != 'LEFT':  nxt_dir = 'RIGHT'
                    elif k == pygame.K_ESCAPE:
                        running = False

            if not running:
                break

            direction = nxt_dir

            # ── move ──
            head = list(snake[0])
            if   direction == 'UP':    head[1] -= BLOCK_SIZE
            elif direction == 'DOWN':  head[1] += BLOCK_SIZE
            elif direction == 'LEFT':  head[0] -= BLOCK_SIZE
            elif direction == 'RIGHT': head[0] += BLOCK_SIZE

            # ── collision ──
            wall_hit     = not (0 <= head[0] < WIDTH and 0 <= head[1] < HEIGHT)
            self_hit     = head in snake
            obstacle_hit = head in obstacles

            if obstacle_hit:                              # obstacles always kill
                running = False; break

            if wall_hit or self_hit:
                if shield_active:                         # shield absorbs one hit
                    shield_active = False
                    if wall_hit:                          # wrap-around
                        head[0] %= WIDTH
                        head[1] %= HEIGHT
                    # self-hit: just keep the new position; overlap resolves naturally
                else:
                    running = False; break

            # ── grow / shrink ──
            snake.insert(0, head)
            grew = False

            # — food —
            if head == food_pos:
                grew   = True
                score += food_weight

                # level-up every 5 points
                new_level = score // 5 + 1
                if new_level > level:
                    level      = new_level
                    base_speed += 2
                    if not pu_active or active_pu not in ('speed', 'slow'):
                        current_speed = base_speed
                    # obstacles start at level 3
                    if level >= 3:
                        static = [food_pos, poison_pos] + ([pu_pos] if pu_pos else [])
                        obstacles = self._new_obstacles(snake, static, level)

                blocked = [poison_pos] + obstacles + ([pu_pos] if pu_pos else [])
                food_pos, food_weight, food_timer = self._new_food(snake, blocked)

            # — poison —
            if head == poison_pos:
                # shorten by 2 extra (tail will be popped normally below if not grew)
                for _ in range(2):
                    if len(snake) > 1:
                        snake.pop()
                blocked    = [food_pos] + obstacles + ([pu_pos] if pu_pos else [])
                poison_pos = self._new_poison(snake, blocked)

            # — power-up pickup —
            if pu_pos and head == pu_pos:
                pu_active     = True
                active_pu     = pu_kind
                pu_effect_end = now_ms + 5_000
                pu_pos = pu_kind = pu_field_exp = None

                if   active_pu == 'speed':  current_speed = base_speed + 5
                elif active_pu == 'slow':   current_speed = max(2, base_speed - 4)
                elif active_pu == 'shield': shield_active = True

            # normal tail removal
            if not grew and len(snake) > 1:
                snake.pop()

            # game over if too short after poison
            if len(snake) <= 1:
                running = False; break

            # ── draw ──
            self.screen.fill(BLACK)

            if self.settings.get('grid_overlay', False):
                self._draw_grid()

            for obs in obstacles:
                pygame.draw.rect(self.screen, GRAY,
                                 pygame.Rect(obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE))

            for seg in snake:
                col = CYAN if shield_active else self.snake_color
                pygame.draw.rect(self.screen, col,
                                 pygame.Rect(seg[0], seg[1], BLOCK_SIZE, BLOCK_SIZE))

            # food: red (1pt) → orange (2pt) → gold (3pt)
            f_col = RED if food_weight == 1 else ORANGE if food_weight == 2 else GOLD
            pygame.draw.rect(self.screen, f_col,
                             pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))

            # poison (dark red square)
            pygame.draw.rect(self.screen, DARK_RED,
                             pygame.Rect(poison_pos[0], poison_pos[1], BLOCK_SIZE, BLOCK_SIZE))

            # power-up on field
            if pu_pos:
                pygame.draw.rect(self.screen, POWERUP_COLORS.get(pu_kind, WHITE),
                                 pygame.Rect(pu_pos[0], pu_pos[1], BLOCK_SIZE, BLOCK_SIZE))
                label = self.small_font.render(
                    POWERUP_LABELS.get(pu_kind, '?')[0], True, BLACK
                )
                self.screen.blit(label, (pu_pos[0] + 3, pu_pos[1] + 2))

            self._draw_hud(score, level, food_timer,
                           pu_active, active_pu, pu_effect_end, shield_active)
            pygame.display.flip()
            self.clock.tick(current_speed)

        return score, level