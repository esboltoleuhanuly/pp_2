# main.py — screen state machine + all four screens
#
# Screens:  main_menu → game → game_over
#                    ↓         ↓
#              leaderboard   menu
#              settings

import pygame
import json
import os
import sys

from config import *
import db
from game import Game


SETTINGS_FILE    = 'settings.json'
DEFAULT_SETTINGS = {
    'snake_color':  list(GREEN),
    'grid_overlay': False,
    'sound':        False,
}


# ── settings I/O ─────────────────────────────────────────────────────────────

def load_settings() -> dict:
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return dict(DEFAULT_SETTINGS)


def save_settings(settings: dict):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=2)


# ── UI primitives ─────────────────────────────────────────────────────────────

def draw_button(surface, rect: pygame.Rect, text: str, font,
                active: bool = False):
    bg = DARK_GREEN if active else DARK_GRAY
    pygame.draw.rect(surface, bg,    rect, border_radius=6)
    pygame.draw.rect(surface, WHITE, rect, 2, border_radius=6)
    txt  = font.render(text, True, WHITE)
    surface.blit(txt, txt.get_rect(center=rect.center))


def draw_centered(surface, text: str, font, color, y: int):
    surf = font.render(text, True, color)
    surface.blit(surf, ((WIDTH - surf.get_width()) // 2, y))


# ── Screen: Main Menu ─────────────────────────────────────────────────────────

def screen_main_menu(screen, clock, font, small_font,
                     settings, initial_username: str = ''):
    """
    Returns (action, username, player_id)
    action ∈ {'play', 'leaderboard', 'settings'}
    """
    username     = initial_username
    input_active = True
    db_ok        = db.init_db()
    error_msg    = ''

    # button layout
    btn_play = pygame.Rect(WIDTH // 2 - 85, 225, 170, 42)
    btn_lb   = pygame.Rect(WIDTH // 2 - 85, 278, 170, 42)
    btn_set  = pygame.Rect(WIDTH // 2 - 85, 331, 170, 42)
    btn_quit = pygame.Rect(WIDTH // 2 - 85, HEIGHT - 48, 170, 38)

    while True:
        screen.fill(BLACK)
        draw_centered(screen, 'SNAKE',      font,       GREEN,      28)
        draw_centered(screen, 'TSIS 4',     small_font, GRAY,       62)

        # ── username input ──
        draw_centered(screen, 'Username:', small_font, LIGHT_GRAY, 100)
        box = pygame.Rect(WIDTH // 2 - 105, 122, 210, 34)
        pygame.draw.rect(screen, DARK_GRAY, box, border_radius=4)
        border_col = CYAN if input_active else GRAY
        pygame.draw.rect(screen, border_col, box, 2, border_radius=4)
        caret = '|' if input_active and (pygame.time.get_ticks() // 500) % 2 == 0 else ' '
        u_surf = small_font.render(username + caret, True, WHITE)
        screen.blit(u_surf, (box.x + 7, box.y + 7))

        if error_msg:
            draw_centered(screen, error_msg, small_font, RED, 163)

        if not db_ok:
            draw_centered(screen, '(DB offline — scores not saved)',
                          small_font, ORANGE, 185)

        draw_button(screen, btn_play, 'Play',        font)
        draw_button(screen, btn_lb,  'Leaderboard',  font)
        draw_button(screen, btn_set, 'Settings',     font)
        draw_button(screen, btn_quit,'Quit',         font)

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if box.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False

                def _try_play():
                    nonlocal error_msg
                    if not username.strip():
                        error_msg = 'Please enter a username!'
                        return None, None
                    pid = db.get_or_create_player(username.strip()) if db_ok else None
                    return username.strip(), pid

                if btn_play.collidepoint(event.pos):
                    u, pid = _try_play()
                    if u:
                        return 'play', u, pid
                if btn_lb.collidepoint(event.pos):
                    return 'leaderboard', username.strip(), None
                if btn_set.collidepoint(event.pos):
                    return 'settings', username.strip(), None
                if btn_quit.collidepoint(event.pos):
                    pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        if not username.strip():
                            error_msg = 'Please enter a username!'
                        else:
                            pid = db.get_or_create_player(username.strip()) if db_ok else None
                            return 'play', username.strip(), pid
                    elif event.key == pygame.K_BACKSPACE:
                        username  = username[:-1]
                        error_msg = ''
                    elif event.unicode.isprintable() and len(username) < 20:
                        username += event.unicode
                        error_msg = ''
                else:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()


# ── Screen: Game Over ─────────────────────────────────────────────────────────

def screen_game_over(screen, clock, font, small_font,
                     score: int, level: int, personal_best: int):
    """Returns 'retry' or 'menu'."""
    btn_retry = pygame.Rect(WIDTH // 2 - 95, 275, 180, 44)
    btn_menu  = pygame.Rect(WIDTH // 2 - 95, 330, 180, 44)

    while True:
        screen.fill(BLACK)
        draw_centered(screen, 'GAME OVER',               font,       RED,   70)
        draw_centered(screen, f'Score : {score}',        font,       WHITE, 140)
        draw_centered(screen, f'Level  : {level}',       font,       WHITE, 178)
        draw_centered(screen, f'Personal best: {personal_best}',
                      small_font, GOLD, 220)
        draw_centered(screen, 'R — retry   |   ESC — menu',
                      small_font, GRAY, 248)
        draw_button(screen, btn_retry, 'Retry',     font)
        draw_button(screen, btn_menu,  'Main Menu', font)

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_retry.collidepoint(event.pos): return 'retry'
                if btn_menu.collidepoint(event.pos):  return 'menu'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:      return 'retry'
                if event.key == pygame.K_ESCAPE: return 'menu'


# ── Screen: Leaderboard ───────────────────────────────────────────────────────

def screen_leaderboard(screen, clock, font, small_font):
    """Fetch top-10 from DB and display. Returns when Back is pressed."""
    rows     = db.get_leaderboard()
    btn_back = pygame.Rect(WIDTH // 2 - 65, HEIGHT - 48, 130, 36)

    col_x    = [12, 38, 195, 270, 345]

    while True:
        screen.fill(BLACK)
        draw_centered(screen, 'LEADERBOARD', font, GOLD, 10)

        # header row
        for label, x in zip(['#', 'Username', 'Score', 'Level', 'Date'], col_x):
            screen.blit(small_font.render(label, True, LIGHT_GRAY), (x, 48))
        pygame.draw.line(screen, GRAY, (8, 68), (WIDTH - 8, 68), 1)

        if not rows:
            draw_centered(screen, 'No records yet.', small_font, GRAY, 100)
        else:
            for rank, (uname, sc, lv, date) in enumerate(rows, 1):
                y   = 72 + (rank - 1) * 24
                col = GOLD if rank == 1 else WHITE
                for val, x in zip([str(rank), uname, str(sc), str(lv), str(date)],
                                   col_x):
                    screen.blit(small_font.render(val, True, col), (x, y))

        draw_button(screen, btn_back, 'Back', font)
        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.collidepoint(event.pos): return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return


# ── Screen: Settings ─────────────────────────────────────────────────────────

def screen_settings(screen, clock, font, small_font, settings: dict) -> dict:
    """Let user tweak settings. Saves to JSON and returns updated dict."""
    local       = dict(settings)
    color_names = list(SNAKE_COLORS.keys())

    # find index of current colour
    cur_idx = 0
    for i, name in enumerate(color_names):
        if list(SNAKE_COLORS[name]) == local.get('snake_color', list(GREEN)):
            cur_idx = i; break

    btn_save    = pygame.Rect(WIDTH // 2 - 85, HEIGHT - 52, 170, 40)
    arrow_l     = pygame.Rect(WIDTH // 2 - 108, 98, 34, 30)
    arrow_r     = pygame.Rect(WIDTH // 2 +  74, 98, 34, 30)
    color_box   = pygame.Rect(WIDTH // 2 -  70, 98, 140, 30)
    btn_grid    = pygame.Rect(WIDTH // 2 -  44, 182, 88, 32)
    btn_sound   = pygame.Rect(WIDTH // 2 -  44, 252, 88, 32)

    while True:
        screen.fill(BLACK)
        draw_centered(screen, 'SETTINGS', font, WHITE, 18)

        # ── snake colour ──
        draw_centered(screen, 'Snake Colour:', small_font, LIGHT_GRAY, 72)
        draw_button(screen, arrow_l, '<', small_font)
        draw_button(screen, arrow_r, '>', small_font)
        cname = color_names[cur_idx]
        pygame.draw.rect(screen, SNAKE_COLORS[cname], color_box, border_radius=4)
        t = small_font.render(cname, True, BLACK)
        screen.blit(t, t.get_rect(center=color_box.center))

        # ── grid toggle ──
        draw_centered(screen, 'Grid Overlay:', small_font, LIGHT_GRAY, 158)
        draw_button(screen, btn_grid,
                    'ON' if local['grid_overlay'] else 'OFF',
                    small_font, active=local['grid_overlay'])

        # ── sound toggle ──
        draw_centered(screen, 'Sound:', small_font, LIGHT_GRAY, 228)
        draw_button(screen, btn_sound,
                    'ON' if local['sound'] else 'OFF',
                    small_font, active=local['sound'])

        if local['sound']:
            draw_centered(screen, '(sound effects not yet implemented)',
                          small_font, GRAY, 292)

        draw_button(screen, btn_save, 'Save & Back', font)
        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if arrow_l.collidepoint(event.pos):
                    cur_idx = (cur_idx - 1) % len(color_names)
                if arrow_r.collidepoint(event.pos):
                    cur_idx = (cur_idx + 1) % len(color_names)
                if btn_grid.collidepoint(event.pos):
                    local['grid_overlay'] = not local['grid_overlay']
                if btn_sound.collidepoint(event.pos):
                    local['sound'] = not local['sound']
                if btn_save.collidepoint(event.pos):
                    local['snake_color'] = list(SNAKE_COLORS[color_names[cur_idx]])
                    save_settings(local)
                    return local

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    local['snake_color'] = list(SNAKE_COLORS[color_names[cur_idx]])
                    save_settings(local)
                    return local


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    pygame.init()
    screen     = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake — TSIS 4')
    clock      = pygame.time.Clock()
    font       = pygame.font.SysFont('Arial', 24, bold=True)
    small_font = pygame.font.SysFont('Arial', 18)

    settings  = load_settings()
    state     = 'menu'
    username  = ''
    player_id = None

    while True:
        # ── main menu ──
        if state == 'menu':
            action, username, player_id = screen_main_menu(
                screen, clock, font, small_font, settings, username
            )
            state = action   # 'play' | 'leaderboard' | 'settings'

        # ── gameplay ──
        elif state == 'play':
            pb           = db.get_personal_best(player_id) if player_id else 0
            g            = Game(screen, clock, font, small_font, settings, pb)
            score, level = g.run()

            if player_id:
                db.save_session(player_id, score, level)
            new_pb = max(pb, score)

            action = screen_game_over(
                screen, clock, font, small_font, score, level, new_pb
            )
            state = 'play' if action == 'retry' else 'menu'

        # ── leaderboard ──
        elif state == 'leaderboard':
            screen_leaderboard(screen, clock, font, small_font)
            state = 'menu'

        # ── settings ──
        elif state == 'settings':
            settings = screen_settings(screen, clock, font, small_font, settings)
            state    = 'menu'


if __name__ == '__main__':
    main()