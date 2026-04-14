import pygame

pygame.init()

# Window setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lag-Free Paint")

# Create a persistent surface (the canvas) to draw on
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((0, 0, 0))

clock = pygame.time.Clock()

# State variables
draw_color = (255, 255, 255)
mode = 'brush' # brush, rect, circle, eraser
start_pos = None
is_drawing = False

def main():
    global draw_color, mode, start_pos, is_drawing
    
    running = True
    while running:
        pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Key bindings for color and mode
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: draw_color = (255, 0, 0)
                if event.key == pygame.K_g: draw_color = (0, 255, 0)
                if event.key == pygame.K_b: draw_color = (0, 0, 255)
                if event.key == pygame.K_w: draw_color = (255, 255, 255)
                if event.key == pygame.K_e: mode = 'eraser'
                if event.key == pygame.K_s: mode = 'brush'
                if event.key == pygame.K_1: mode = 'rect'
                if event.key == pygame.K_2: mode = 'circle'

            # Mouse Logic
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_drawing = True
                start_pos = pos
            
            if event.type == pygame.MOUSEBUTTONUP:
                is_drawing = False
                # Finalize shapes on the CANVAS
                if mode == 'rect' and start_pos:
                    width = pos[0] - start_pos[0]
                    height = pos[1] - start_pos[1]
                    pygame.draw.rect(canvas, draw_color, (start_pos[0], start_pos[1], width, height), 2)
                elif mode == 'circle' and start_pos:
                    radius = int(((pos[0]-start_pos[0])**2 + (pos[1]-start_pos[1])**2)**0.5)
                    pygame.draw.circle(canvas, draw_color, start_pos, radius, 2)
                start_pos = None

        # Continuous drawing for Brush and Eraser (directly to canvas)
        if is_drawing:
            if mode == 'brush':
                pygame.draw.circle(canvas, draw_color, pos, 5)
            elif mode == 'eraser':
                pygame.draw.circle(canvas, (0, 0, 0), pos, 20)

        # --- REFRESH SCREEN ---
        # 1. First, draw the saved canvas
        screen.blit(canvas, (0, 0))
        
        # 2. Draw a "preview" of the shape if currently dragging (only on screen, not canvas)
        if is_drawing and start_pos:
            if mode == 'rect':
                pygame.draw.rect(screen, draw_color, (start_pos[0], start_pos[1], pos[0]-start_pos[0], pos[1]-start_pos[1]), 2)
            elif mode == 'circle':
                radius = int(((pos[0]-start_pos[0])**2 + (pos[1]-start_pos[1])**2)**0.5)
                pygame.draw.circle(screen, draw_color, start_pos, radius, 2)

        pygame.display.flip()
        clock.tick(120) # High FPS for smoothness

    pygame.quit()

main()