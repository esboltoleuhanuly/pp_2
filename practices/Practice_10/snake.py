import pygame
import random

# Initialize Pygame
pygame.init()

# 1. Settings and Constants
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
FPS = 10  # Starting speed

# Colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Setup Screen and Clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Practice 10")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)

def game_loop():
    # Initial snake position (list of coordinates)
    snake = [[100, 60], [80, 60], [60, 60]]
    direction = 'RIGHT'
    
    # 2. Food generation (Grid-aligned)
    food_x = random.randrange(0, WIDTH, BLOCK_SIZE)
    food_y = random.randrange(0, HEIGHT, BLOCK_SIZE)
    food_pos = [food_x, food_y]
    
    score = 0
    level = 1
    current_speed = FPS
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            # Directional controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN': direction = 'UP'
                if event.key == pygame.K_DOWN and direction != 'UP': direction = 'DOWN'
                if event.key == pygame.K_LEFT and direction != 'RIGHT': direction = 'LEFT'
                if event.key == pygame.K_RIGHT and direction != 'LEFT': direction = 'RIGHT'

        # 3. Calculate new head position
        head = list(snake[0])
        if direction == 'UP': head[1] -= BLOCK_SIZE
        if direction == 'DOWN': head[1] += BLOCK_SIZE
        if direction == 'LEFT': head[0] -= BLOCK_SIZE
        if direction == 'RIGHT': head[0] += BLOCK_SIZE
        
        # 4. Checking for border (wall) collision
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            running = False
            
        # Check for self-collision
        if head in snake:
            running = False

        # Add new head to snake
        snake.insert(0, head)

        # 5. Food Logic (Eating the "Apple")
        if head == food_pos:
            score += 1
            # 6. Increase Level and Speed (every 3 foods)
            if score % 3 == 0:
                level += 1
                current_speed += 2
            
            # Generate new food that doesn't land on the snake
            while True:
                food_pos = [random.randrange(0, WIDTH, BLOCK_SIZE), 
                            random.randrange(0, HEIGHT, BLOCK_SIZE)]
                if food_pos not in snake:
                    break
        else:
            # Remove the last part of the tail if no food eaten
            snake.pop()

        # --- Drawing ---
        screen.fill(BLACK)
        
        # Draw Snake
        for pos in snake:
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw Food
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))
        
        # 7. Add counter to score and level
        score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(current_speed)

# Run the game
game_loop()
pygame.quit()