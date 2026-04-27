import pygame
import sys
from persistence import load_leaderboard, add_leaderboard_entry, save_settings

# ─── Colors ───────────────────────────────────────────────────────────────────
WHITE      = (255, 255, 255)
BLACK      = (0,   0,   0  )
DARK_GRAY  = (25,  25,  30 )
GRAY       = (50,  50,  60 )
LIGHT_GRAY = (180, 180, 180)
GOLD       = (218, 165, 32 )
RED        = (200, 40,  40 )
GREEN_BTN  = (30,  110, 30 )
GREEN_HOV  = (50,  150, 50 )
RED_BTN    = (110, 30,  30 )
RED_HOV    = (150, 50,  50 )
BLUE_BTN   = (30,  60,  140)
BLUE_HOV   = (50,  90,  180)
CYAN       = (0,   210, 255)
MAGENTA    = (200, 0,   200)
YELLOW     = (255, 220, 0  )

SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 600


# ─── Button ───────────────────────────────────────────────────────────────────
class Button:
    def __init__(self, x, y, w, h, text,
                 color=GRAY, hover=(90, 90, 100), text_color=WHITE, font_size=20):
        self.rect       = pygame.Rect(x, y, w, h)
        self.text       = text
        self.color      = color
        self.hover      = hover
        self.text_color = text_color
        self.font       = pygame.font.SysFont("Verdana", font_size, bold=True)

    def draw(self, surf):
        col = self.hover if self.rect.collidepoint(pygame.mouse.get_pos()) else self.color
        pygame.draw.rect(surf, col,   self.rect, border_radius=9)
        pygame.draw.rect(surf, WHITE, self.rect, 2, border_radius=9)
        lbl = self.font.render(self.text, True, self.text_color)
        surf.blit(lbl, lbl.get_rect(center=self.rect.center))

    def clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(event.pos))


# ─── Helpers ──────────────────────────────────────────────────────────────────
def _title(surf, text, y=55, color=GOLD, size=36):
    f   = pygame.font.SysFont("Verdana", size, bold=True)
    lbl = f.render(text, True, color)
    surf.blit(lbl, lbl.get_rect(centerx=SCREEN_WIDTH // 2, y=y))


def _text(surf, text, y, color=WHITE, size=18, bold=False):
    f   = pygame.font.SysFont("Verdana", size, bold=bold)
    lbl = f.render(text, True, color)
    surf.blit(lbl, lbl.get_rect(centerx=SCREEN_WIDTH // 2, y=y))
    return lbl.get_width()


def _quit_check(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()


# ─── Username Entry ───────────────────────────────────────────────────────────
def get_username(screen):
    clock = pygame.time.Clock()
    font  = pygame.font.SysFont("Verdana", 22)
    name  = ""

    while True:
        screen.fill(DARK_GRAY)
        _title(screen, "RACER", y=70)
        _text(screen, "Enter your name:", y=180, size=20)

        box = pygame.Rect(70, 220, 260, 46)
        pygame.draw.rect(screen, GRAY, box, border_radius=8)
        pygame.draw.rect(screen, CYAN, box, 2, border_radius=8)
        cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""
        lbl = font.render(name + cursor, True, CYAN)
        screen.blit(lbl, lbl.get_rect(center=box.center))

        _text(screen, "Press ENTER to continue", y=285, color=LIGHT_GRAY, size=14)

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            _quit_check(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    return name.strip()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 15 and event.unicode.isprintable():
                    name += event.unicode


# ─── Game launcher (imported here to avoid circular) ─────────────────────────
def _launch_game(screen, settings, username):
    from racer import Game
    game   = Game(screen, settings, username)
    result = game.run()
    if result is None:
        pygame.quit()
        sys.exit()
    score, distance, coins = result
    add_leaderboard_entry(username, score, distance)
    game_over_screen(screen, settings, username, score, distance, coins)


# ─── Main Menu ────────────────────────────────────────────────────────────────
def main_menu(settings):
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Racer – TSIS 3")
    clock  = pygame.time.Clock()

    CX = SCREEN_WIDTH // 2
    btn_play = Button(CX-110, 200, 220, 52, "▶  PLAY",
                      color=GREEN_BTN, hover=GREEN_HOV)
    btn_lb   = Button(CX-110, 268, 220, 52, "🏆  LEADERBOARD",
                      color=BLUE_BTN, hover=BLUE_HOV, font_size=17)
    btn_set  = Button(CX-110, 336, 220, 52, "⚙  SETTINGS")
    btn_quit = Button(CX-110, 404, 220, 52, "✕  QUIT",
                      color=RED_BTN, hover=RED_HOV)
    buttons = [btn_play, btn_lb, btn_set, btn_quit]

    sf = pygame.font.SysFont("Verdana", 13)

    while True:
        screen.fill(DARK_GRAY)

        # Decorative road lines (static)
        for lx in [30, 194, 358]:
            pygame.draw.line(screen, GRAY, (lx, 0), (lx, SCREEN_HEIGHT), 2)

        _title(screen, "🏎  RACER", y=90, size=40)

        diff_surf = sf.render(
            f"Difficulty: {settings.get('difficulty','normal').upper()}   "
            f"Car: {settings.get('car_color','blue').upper()}",
            True, LIGHT_GRAY)
        screen.blit(diff_surf, diff_surf.get_rect(centerx=CX, y=158))

        for b in buttons:
            b.draw(screen)

        # Controls hint
        hint = sf.render("← → to steer   ESC to pause", True, GRAY)
        screen.blit(hint, hint.get_rect(centerx=CX, y=490))

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            _quit_check(event)
            if btn_play.clicked(event):
                username = get_username(screen)
                _launch_game(screen, settings, username)
            if btn_lb.clicked(event):
                leaderboard_screen(screen)
            if btn_set.clicked(event):
                settings = settings_screen(screen, settings)
                # Update difficulty label on button
                btn_play.text = "▶  PLAY"
            if btn_quit.clicked(event):
                pygame.quit()
                sys.exit()


# ─── Game Over Screen ─────────────────────────────────────────────────────────
def game_over_screen(screen, settings, username, score, distance, coins):
    clock = pygame.time.Clock()
    CX    = SCREEN_WIDTH // 2

    btn_retry = Button(50, 450, 130, 50, "RETRY",
                       color=GREEN_BTN, hover=GREEN_HOV)
    btn_menu  = Button(220, 450, 130, 50, "MENU")

    while True:
        screen.fill(DARK_GRAY)
        _title(screen, "GAME OVER", y=60, color=RED, size=34)

        rows = [
            (f"Player: {username}",    WHITE,  130),
            (f"Score:  {score}",       GOLD,   190),
            (f"Distance: {distance}m", CYAN,   245),
            (f"Coins collected: {coins}", YELLOW, 300),
        ]
        for txt, col, y in rows:
            _text(screen, txt, y=y, color=col, size=20)

        # Score breakdown box
        pygame.draw.rect(screen, GRAY, (40, 120, SCREEN_WIDTH - 80, 220), border_radius=10)
        pygame.draw.rect(screen, GOLD, (40, 120, SCREEN_WIDTH - 80, 220), 2, border_radius=10)

        btn_retry.draw(screen)
        btn_menu.draw(screen)

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            _quit_check(event)
            if btn_retry.clicked(event):
                _launch_game(screen, settings, username)
                return
            if btn_menu.clicked(event):
                return


# ─── Leaderboard Screen ───────────────────────────────────────────────────────
def leaderboard_screen(screen):
    clock   = pygame.time.Clock()
    entries = load_leaderboard()
    CX      = SCREEN_WIDTH // 2

    btn_back = Button(CX - 70, 545, 140, 44, "← BACK")

    row_font = pygame.font.SysFont("Verdana", 15)
    hdr_font = pygame.font.SysFont("Verdana", 14, bold=True)

    MEDAL = [GOLD, (192, 192, 192), (176, 141, 87)]

    while True:
        screen.fill(DARK_GRAY)
        _title(screen, "🏆  LEADERBOARD", y=25, size=28)

        # Header row
        header_rect = pygame.Rect(20, 75, SCREEN_WIDTH - 40, 26)
        pygame.draw.rect(screen, GRAY, header_rect, border_radius=4)
        hdr = hdr_font.render(
            f"{'#':<3}  {'Name':<13} {'Score':>6}  {'Dist':>6}", True, LIGHT_GRAY)
        screen.blit(hdr, (28, 79))

        if not entries:
            _text(screen, "No scores yet — play a game!", y=270, color=LIGHT_GRAY, size=16)
        else:
            for i, e in enumerate(entries[:10]):
                col  = MEDAL[i] if i < 3 else WHITE
                bg   = (40, 40, 50) if i % 2 == 0 else (35, 35, 45)
                row_rect = pygame.Rect(20, 104 + i * 38, SCREEN_WIDTH - 40, 34)
                pygame.draw.rect(screen, bg, row_rect, border_radius=4)
                if i < 3:
                    pygame.draw.rect(screen, col, row_rect, 1, border_radius=4)
                txt = f"{i+1:<3}  {e['name'][:12]:<13} {e['score']:>6}  {e['distance']:>5}m"
                lbl = row_font.render(txt, True, col)
                screen.blit(lbl, (28, 112 + i * 38))

        btn_back.draw(screen)
        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            _quit_check(event)
            if btn_back.clicked(event):
                return


# ─── Settings Screen ──────────────────────────────────────────────────────────
def settings_screen(screen, settings):
    clock  = pygame.time.Clock()
    local  = settings.copy()
    CX     = SCREEN_WIDTH // 2

    COLORS = ["blue", "red", "green"]
    DIFFS  = ["easy", "normal", "hard"]

    def _make_buttons():
        sound_lbl = "Sound: ON" if local.get("sound", True) else "Sound: OFF"
        color_lbl = f"Car Color: {local.get('car_color','blue').upper()}"
        diff_lbl  = f"Difficulty: {local.get('difficulty','normal').upper()}"
        return [
            Button(CX-120, 160, 240, 52, sound_lbl),
            Button(CX-120, 228, 240, 52, color_lbl),
            Button(CX-120, 296, 240, 52, diff_lbl),
            Button(CX-120, 390, 240, 52, "✔  SAVE & BACK",
                   color=GREEN_BTN, hover=GREEN_HOV),
        ]

    buttons = _make_buttons()
    sf = pygame.font.SysFont("Verdana", 13)

    while True:
        screen.fill(DARK_GRAY)
        _title(screen, "⚙  SETTINGS", y=60)

        # Labels
        for lbl_txt, ly in [("Toggle sound on/off", 142),
                             ("Choose your car colour", 210),
                             ("Choose difficulty", 278)]:
            l = sf.render(lbl_txt, True, LIGHT_GRAY)
            screen.blit(l, (CX - l.get_width()//2, ly))

        # Car colour preview swatch
        SWATCH = {"blue": (50,100,255), "red": (220,50,50), "green": (50,200,50)}
        col_name = local.get("car_color", "blue")
        pygame.draw.rect(screen, SWATCH[col_name], (CX + 85, 235, 26, 38), border_radius=4)

        for b in buttons:
            b.draw(screen)

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            _quit_check(event)

            if buttons[0].clicked(event):   # sound
                local["sound"] = not local.get("sound", True)
                buttons = _make_buttons()

            elif buttons[1].clicked(event): # car color
                idx = COLORS.index(local.get("car_color", "blue"))
                local["car_color"] = COLORS[(idx + 1) % len(COLORS)]
                buttons = _make_buttons()

            elif buttons[2].clicked(event): # difficulty
                idx = DIFFS.index(local.get("difficulty", "normal"))
                local["difficulty"] = DIFFS[(idx + 1) % len(DIFFS)]
                buttons = _make_buttons()

            elif buttons[3].clicked(event): # save
                save_settings(local)
                return local