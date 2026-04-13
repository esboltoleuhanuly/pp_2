import pygame
from player import MusicPlayer

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("KBTU Music Player")

# Initialize player - it looks for the 'music' folder inside music_player/
player = MusicPlayer("music")

running = True
while running:
    screen.fill((50, 50, 50))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p: # P for Play
                player.play()
            elif event.key == pygame.K_s: # S for Stop
                player.stop()
            elif event.key == pygame.K_n: # N for Next
                player.next()
            elif event.key == pygame.K_b: # B for Back/Previous
                player.previous()

    pygame.display.flip()

pygame.quit()