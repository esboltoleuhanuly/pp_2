import pygame
from clock import MickeyClock

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Mickey Clock")
mickey = MickeyClock()
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    mickey.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()