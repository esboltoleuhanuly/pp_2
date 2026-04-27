import pygame
from datetime import datetime
import tools

pygame.init()

WIDTH, HEIGHT = 800, 600
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Pro")

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(BLACK)

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
hint_font = pygame.font.SysFont("Arial", 16) # Font specifically for the hint overlay

# State
draw_color = WHITE
mode = 'pencil' 
thicknesses = [2, 5, 10]
curr_thick_idx = 1
is_drawing = False
start_pos, last_pos = None, None

# Text state
text_string, text_pos, is_typing = "", None, False

def main():
    global draw_color, mode, start_pos, is_drawing, curr_thick_idx, last_pos
    global text_string, text_pos, is_typing
    
    running = True
    while running:
        thick = thicknesses[curr_thick_idx]
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                # Color shortcuts
                if event.key == pygame.K_r: draw_color = (255, 0, 0)
                if event.key == pygame.K_g: draw_color = (0, 255, 0)
                if event.key == pygame.K_b: draw_color = (0, 0, 255)
                if event.key == pygame.K_w: draw_color = WHITE
                
                # Sizes (Fixed index out of bounds bug)
                if event.key == pygame.K_1: curr_thick_idx = 0
                if event.key == pygame.K_2: curr_thick_idx = 1
                if event.key == pygame.K_3: curr_thick_idx = 2
                
                # Modes
                if event.key == pygame.K_p: mode = 'pencil'
                if event.key == pygame.K_l: mode = 'line'
                if event.key == pygame.K_f: mode = 'fill'
                if event.key == pygame.K_t: mode = 'text'
                if event.key == pygame.K_e: mode = 'eraser'
                
                # Shapes
                if event.key == pygame.K_F1: mode = 'rectangle'
                if event.key == pygame.K_F2: mode = 'square'
                if event.key == pygame.K_F3: mode = 'right_triangle'
                if event.key == pygame.K_F4: mode = 'equilateral_triangle'
                if event.key == pygame.K_F5: mode = 'rhombus'
                if event.key == pygame.K_F6: mode = 'circle'

                # Save by Date and Time
                if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    date_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                    pygame.image.save(canvas, f"paint_{date_str}.png")

                # Text typing
                if is_typing:
                    if event.key == pygame.K_RETURN:
                        canvas.blit(font.render(text_string, True, draw_color), text_pos)
                        is_typing = False
                    elif event.key == pygame.K_BACKSPACE:
                        text_string = text_string[:-1]
                    else:
                        text_string += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if mode == 'fill':
                    tools.flood_fill(canvas, mouse_pos, draw_color)
                elif mode == 'text':
                    is_typing, text_pos, text_string = True, mouse_pos, ""
                else:
                    is_drawing, start_pos, last_pos = True, mouse_pos, mouse_pos
            
            if event.type == pygame.MOUSEBUTTONUP:
                if is_drawing and start_pos:
                    if mode == 'line':
                        pygame.draw.line(canvas, draw_color, start_pos, mouse_pos, thick)
                    elif mode == 'rectangle':
                        r_data = (start_pos[0], start_pos[1], mouse_pos[0]-start_pos[0], mouse_pos[1]-start_pos[1])
                        pygame.draw.rect(canvas, draw_color, r_data, thick)
                    elif mode == 'circle':
                        rad = int(pygame.math.Vector2(start_pos).distance_to(mouse_pos))
                        pygame.draw.circle(canvas, draw_color, start_pos, rad, thick)
                    elif mode == 'square':
                        s = max(abs(mouse_pos[0]-start_pos[0]), abs(mouse_pos[1]-start_pos[1]))
                        pygame.draw.rect(canvas, draw_color, (start_pos[0], start_pos[1], s, s), thick)
                    elif mode == 'right_triangle':
                        pygame.draw.polygon(canvas, draw_color, [(start_pos[0], start_pos[1]), (start_pos[0], mouse_pos[1]), (mouse_pos[0], mouse_pos[1])], thick)
                    elif mode == 'equilateral_triangle':
                        pygame.draw.polygon(canvas, draw_color, tools.get_equilateral_points(start_pos, mouse_pos), thick)
                    elif mode == 'rhombus':
                        pygame.draw.polygon(canvas, draw_color, tools.get_rhombus_points(start_pos, mouse_pos), thick)
                is_drawing = False

        # Pencil/Eraser with interpolation
        if is_drawing and mode in ['pencil', 'eraser']:
            clr = BLACK if mode == 'eraser' else draw_color
            t = 20 if mode == 'eraser' else thick
            pygame.draw.line(canvas, clr, last_pos, mouse_pos, t)
            pygame.draw.circle(canvas, clr, mouse_pos, t // 2)
            last_pos = mouse_pos

        screen.blit(canvas, (0, 0))
        
        # Live Previews
        if is_drawing and start_pos:
            if mode == 'line':
                pygame.draw.line(screen, draw_color, start_pos, mouse_pos, thick)
            elif mode == 'rectangle':
                r_data = (start_pos[0], start_pos[1], mouse_pos[0]-start_pos[0], mouse_pos[1]-start_pos[1])
                pygame.draw.rect(screen, draw_color, r_data, thick)
            elif mode == 'circle':
                rad = int(pygame.math.Vector2(start_pos).distance_to(mouse_pos))
                pygame.draw.circle(screen, draw_color, start_pos, rad, thick)
            elif mode == 'square':
                s = max(abs(mouse_pos[0]-start_pos[0]), abs(mouse_pos[1]-start_pos[1]))
                pygame.draw.rect(screen, draw_color, (start_pos[0], start_pos[1], s, s), thick)
            elif mode == 'right_triangle':
                pygame.draw.polygon(screen, draw_color, [(start_pos[0], start_pos[1]), (start_pos[0], mouse_pos[1]), (mouse_pos[0], mouse_pos[1])], thick)
            elif mode == 'equilateral_triangle':
                pygame.draw.polygon(screen, draw_color, tools.get_equilateral_points(start_pos, mouse_pos), thick)
            elif mode == 'rhombus':
                pygame.draw.polygon(screen, draw_color, tools.get_rhombus_points(start_pos, mouse_pos), thick)

        if is_typing:
            screen.blit(font.render(text_string + "|", True, draw_color), text_pos)
            
        # Draw Hint Overlay
        hints = [
            f"Current Mode: {mode.upper()}",
            "Tools: P(encil) L(ine) F(ill) T(ext) E(raser)",
            "Shapes: F1(Rect) F2(Sq) F3(RTri) F4(ETri) F5(Rhom) F6(Circ)",
            "Colors: R(ed) G(reen) B(lue) W(hite)",
            "Sizes: 1(Small) 2(Med) 3(Large)",
            "Save: Ctrl + S"
        ]
        
        overlay = pygame.Surface((450, 130))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        screen.blit(overlay, (10, 10))
        
        for i, text in enumerate(hints):
            # Highlight the current mode line in a different color
            color = (100, 255, 100) if i == 0 else WHITE
            txt_surf = hint_font.render(text, True, color)
            screen.blit(txt_surf, (20, 15 + i * 20))
        
        pygame.display.flip()
        clock.tick(120)

    pygame.quit()

if __name__ == "__main__":
    main()