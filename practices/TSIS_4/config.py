# config.py — shared constants and colours

WIDTH,  HEIGHT     = 600, 400
BLOCK_SIZE         = 20
FPS                = 10

# ── palette ──────────────────────────────────────────────────────────────────
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
GREEN      = (0,   200, 0)
DARK_GREEN = (0,   120, 0)
RED        = (220, 50,  50)
DARK_RED   = (139, 0,   0)
GOLD       = (255, 215, 0)
ORANGE     = (255, 140, 0)
BLUE       = (30,  144, 255)
CYAN       = (0,   220, 220)
PURPLE     = (160, 32,  240)
GRAY       = (120, 120, 120)
DARK_GRAY  = (40,  40,  40)
LIGHT_GRAY = (180, 180, 180)

# ── snake colour presets ──────────────────────────────────────────────────────
SNAKE_COLORS = {
    'Green':  (0,   200, 0),
    'Cyan':   (0,   220, 220),
    'Yellow': (255, 255, 0),
    'Orange': (255, 140, 0),
    'Purple': (160, 32,  240),
}

# ── power-up palette & labels ─────────────────────────────────────────────────
POWERUP_COLORS  = {'speed': BLUE, 'slow': PURPLE, 'shield': CYAN}
POWERUP_LABELS  = {'speed': 'SPEED+', 'slow': 'SLOW', 'shield': 'SHIELD'}