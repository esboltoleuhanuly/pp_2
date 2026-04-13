import pygame, datetime, math, os

class MickeyClock:
    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), "images", "main_clock.png")
        self.bg = pygame.transform.scale(pygame.image.load(path), (800, 800))
        self.center = (400, 400)

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        t = datetime.datetime.now()
        # Draw Seconds (Red) and Minutes (Black)
        self.draw_hand(screen, t.second, 280, (255, 0, 0), 3)
        self.draw_hand(screen, t.minute, 200, (0, 0, 0), 7)

    def draw_hand(self, screen, val, length, color, width):
        angle = math.radians(val * 6 - 90)
        end = (self.center[0] + length * math.cos(angle), 
               self.center[1] + length * math.sin(angle))
        pygame.draw.line(screen, color, self.center, end, width)