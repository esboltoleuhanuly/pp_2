"""
TSIS 3 – Racer Game
Run with:  python main.py
Requires:  pip install pygame
"""

import pygame
import sys
from persistence import load_settings
from ui import main_menu


def main():
    pygame.init()
    settings = load_settings()
    main_menu(settings)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()