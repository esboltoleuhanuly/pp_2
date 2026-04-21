import pygame
import random
import time

# Initialize Pygame
pygame.init()

# 1. Settings and Constants
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
FPS = 10 

# Colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0) # Color for high-weight food
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Setup Screen and Clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Practice 11")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)

def game_loop():
    snake = [[100, 60], [80, 60], [60, 60]]
    direction = 'RIGHT'
    
    # --- New Food Logic Variables ---
    def generate_food():
        # Task 1: Random weights
        weight = random.randint(1, 3) 
        pos = [random.randrange(0, WIDTH, BLOCK_SIZE), 
               random.randrange(0, HEIGHT, BLOCK_SIZE)]
        # Task 2: Disappearing timer (5 seconds from now)
        expiration = time.time() + 5 
        return pos, weight, expiration

    food_pos, food_weight, food_timer = generate_food()
    
    score = 0
    level = 1
    current_speed = FPS
    
    running = True
    while running:
        # Task 2: Check if food expired
        if time.time() > food_timer:
            food_pos, food_weight, food_timer = generate_food()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN': direction = 'UP'
                if event.key == pygame.K_DOWN and direction != 'UP': direction = 'DOWN'
                if event.key == pygame.K_LEFT and direction != 'RIGHT': direction = 'LEFT'
                if event.key == pygame.K_RIGHT and direction != 'LEFT': direction = 'RIGHT'

        head = list(snake[0])
        if direction == 'UP': head[1] -= BLOCK_SIZE
        if direction == 'DOWN': head[1] += BLOCK_SIZE
        if direction == 'LEFT': head[0] -= BLOCK_SIZE
        if direction == 'RIGHT': head[0] += BLOCK_SIZE
        
        # Border/Self Collision
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT or head in snake:
            running = False
            
        snake.insert(0, head)

        # Task 1: Food Logic with weights
        if head == food_pos:
            score += food_weight # Increase score by weight
            
            # Level and speed logic (increase every 5 points)
            if score // 5 >= level:
                level += 1
                current_speed += 2
            
            # Generate new food and reset timer
            while True:
                food_pos, food_weight, food_timer = generate_food()
                if food_pos not in snake:
                    break
        else:
            snake.pop()

        # --- Drawing ---
        screen.fill(BLACK)
        
        for pos in snake:
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw Food (Color changes based on weight)
        food_color = RED if food_weight == 1 else GOLD
        pygame.draw.rect(screen, food_color, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw UI and Timer
        time_left = max(0, int(food_timer - time.time()))
        score_text = font.render(f"Score: {score}  Lvl: {level}  Timer: {time_left}s", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(current_speed)

game_loop()
pygame.quit()