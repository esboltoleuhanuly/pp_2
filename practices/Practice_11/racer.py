import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0  # Total weight earned
COINS_COLLECTED = 0 # Count of coins earned
N = 5 # Increase speed every N coins collected

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GOLD = (218, 165, 32) # Color for heavier coins
RED = (255, 0, 0)
GRAY = (50, 50, 50)

# Create Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont("Verdana", 20)
clock = pygame.time.Clock()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 70))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        # Enemy speed is controlled by the global SPEED variable
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # TASK 1: Randomly generating coins with different weights
        self.weight = random.randint(1, 5) 
        self.image = pygame.Surface((20, 20))
        
        # Visual feedback: heavier coins are darker/gold
        if self.weight > 3:
            self.image.fill(GOLD)
        else:
            self.image.fill(YELLOW)
            
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            self.kill() # Remove coin if it goes off screen

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[pygame.K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[pygame.K_RIGHT]:
                self.rect.move_ip(5, 0)

# Setup Groups
P1 = Player()
E1 = Enemy()

enemies = pygame.sprite.Group()
enemies.add(E1)

coins_group = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# Road line variable
line_y = 0

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Logic to keep at least one coin on screen
    if len(coins_group) < 1:
        new_coin = Coin()
        coins_group.add(new_coin)
        all_sprites.add(new_coin)

    # Draw Road
    screen.fill(GRAY)
    
    # Draw Moving Road Lines
    line_y += SPEED
    if line_y > 100:
        line_y = 0
    for y in range(-100, SCREEN_HEIGHT, 100):
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH//2 - 5, y + line_y, 10, 50))

    # Move and Draw all entities
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()

    collided_coin = pygame.sprite.spritecollideany(P1, coins_group)
    if collided_coin:
        SCORE += collided_coin.weight # Add the random weight to total score
        COINS_COLLECTED += 1
        collided_coin.kill() # Remove collected coin
        
        # TASK 2: Increase the speed of Enemy when the player earns N coins
        if COINS_COLLECTED % N == 0:
            SPEED += 1

    # Check for collision with enemy cars
    if pygame.sprite.spritecollideany(P1, enemies):
        print(f"Game Over! Final Score: {SCORE}")
        running = False

    # UI Overlay
    score_text = font.render(f"Score: {SCORE}", True, WHITE)
    speed_text = font.render(f"Speed: {SPEED}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH - 120, 10))
    screen.blit(speed_text, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()