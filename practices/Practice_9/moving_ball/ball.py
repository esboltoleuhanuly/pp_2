import pygame

class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self, dx, dy, screen_width, screen_height):
        # Boundary Check: Only move if the ball stays inside the screen
        if (self.radius <= self.x + dx <= screen_width - self.radius and 
            self.radius <= self.y + dy <= screen_height - self.radius):
            self.x += dx
            self.y += dy