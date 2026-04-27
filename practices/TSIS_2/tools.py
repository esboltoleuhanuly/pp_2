import math
import pygame

def get_rhombus_points(start, end):
    x1, y1 = start
    x2, y2 = end
    return [
        (x1 + (x2 - x1) // 2, y1), 
        (x2, y1 + (y2 - y1) // 2), 
        (x1 + (x2 - x1) // 2, y2), 
        (x1, y1 + (y2 - y1) // 2)
    ]

def get_equilateral_points(start, end):
    x1, y1 = start
    x2, y2 = end
    side = x2 - x1
    height = side * math.sqrt(3) / 2
    return [(x1, y1), (x2, y1), (x1 + side / 2, y1 - height)]

def flood_fill(surface, start_pos, fill_color):
    target_color = surface.get_at(start_pos)
    if target_color == fill_color:
        return
    
    stack = [start_pos]
    width, height = surface.get_size()
    
    while stack:
        x, y = stack.pop()
        if surface.get_at((x, y)) == target_color:
            surface.set_at((x, y), fill_color)
            if x > 0: stack.append((x - 1, y))
            if x < width - 1: stack.append((x + 1, y))
            if y > 0: stack.append((x, y - 1))
            if y < height - 1: stack.append((x, y + 1))