import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Practice 11")

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((0, 0, 0))

clock = pygame.time.Clock()

draw_color = (255, 255, 255)
# New modes: 'square', 'right_triangle', 'equilateral_triangle', 'rhombus'
mode = 'brush' 
start_pos = None
is_drawing = False

def get_rhombus_points(start, end):
    x1, y1 = start
    x2, y2 = end
    return [(x1 + (x2-x1)//2, y1), (x2, y1 + (y2-y1)//2), 
            (x1 + (x2-x1)//2, y2), (x1, y1 + (y2-y1)//2)]

def get_equilateral_points(start, end):
    x1, y1 = start
    x2, y2 = end
    side = x2 - x1
    height = side * math.sqrt(3) / 2
    return [(x1, y1), (x2, y1), (x1 + side/2, y1 - height)]

def main():
    global draw_color, mode, start_pos, is_drawing
    
    running = True
    while running:
        pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: draw_color = (255, 0, 0)
                if event.key == pygame.K_g: draw_color = (0, 255, 0)
                if event.key == pygame.K_b: draw_color = (0, 0, 255)
                if event.key == pygame.K_w: draw_color = (255, 255, 255)
                if event.key == pygame.K_e: mode = 'eraser'
                if event.key == pygame.K_s: mode = 'brush'
                # Task Mapping
                if event.key == pygame.K_1: mode = 'square'
                if event.key == pygame.K_2: mode = 'right_triangle'
                if event.key == pygame.K_3: mode = 'equilateral_triangle'
                if event.key == pygame.K_4: mode = 'rhombus'

            if event.type == pygame.MOUSEBUTTONDOWN:
                is_drawing = True
                start_pos = pos
            
            if event.type == pygame.MOUSEBUTTONUP:
                is_drawing = False
                if start_pos:
                    x, y = start_pos
                    dx, dy = pos[0]-x, pos[1]-y
                    
                    if mode == 'square':
                        side = max(abs(dx), abs(dy))
                        pygame.draw.rect(canvas, draw_color, (x, y, side, side), 2)
                    elif mode == 'right_triangle':
                        pygame.draw.polygon(canvas, draw_color, [(x, y), (x, pos[1]), (pos[0], pos[1])], 2)
                    elif mode == 'equilateral_triangle':
                        pygame.draw.polygon(canvas, draw_color, get_equilateral_points(start_pos, pos), 2)
                    elif mode == 'rhombus':
                        pygame.draw.polygon(canvas, draw_color, get_rhombus_points(start_pos, pos), 2)
                start_pos = None

        if is_drawing:
            if mode == 'brush':
                pygame.draw.circle(canvas, draw_color, pos, 5)
            elif mode == 'eraser':
                pygame.draw.circle(canvas, (0, 0, 0), pos, 20)

        screen.blit(canvas, (0, 0))
        
        # PREVIEWS (Drawing only on screen, not canvas)
        if is_drawing and start_pos:
            x, y = start_pos
            if mode == 'square':
                side = max(abs(pos[0]-x), abs(pos[1]-y))
                pygame.draw.rect(screen, draw_color, (x, y, side, side), 2)
            elif mode == 'right_triangle':
                pygame.draw.polygon(screen, draw_color, [(x, y), (x, pos[1]), (pos[0], pos[1])], 2)
            elif mode == 'equilateral_triangle':
                pygame.draw.polygon(screen, draw_color, get_equilateral_points(start_pos, pos), 2)
            elif mode == 'rhombus':
                pygame.draw.polygon(screen, draw_color, get_rhombus_points(start_pos, pos), 2)

        pygame.display.flip()
        clock.tick(120)

    pygame.quit()

main()