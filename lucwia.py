import pygame
import numpy as np

screen, clock = None, None

def init(size = (600, 600), title = "Sketch"):
    global screen, clock

    if screen != None: return

    pygame.init()
    screen = pygame.display.set_mode(size)
    set_title(title)
    clock = pygame.time.Clock()

def quit():
    global screen, clock
    
    screen = None
    clock = None

    pygame.quit()

def set_title(title):
    pygame.display.set_caption(title)

def should_close():
    return screen == None

def update():
    if screen == None: return

    if pygame.event.peek(pygame.QUIT):
        quit()
        return 0

    pygame.display.flip()
    return clock.tick(60) * 0.001

def background(col):
    if screen == None: return
    screen.fill(col)

def line(x0, y0, x1, y1, col, w = 1):
    if screen == None: return
    pygame.draw.line(screen, col, (x0, y0), (x1, y1), w)

def circle(x, y, r, col):
    if screen == None: return
    pygame.draw.circle(screen, col, (x, y), r)

def generate_colors(num_colors, saturation, value):
    hues = np.linspace(0, 360 - 360 / num_colors, num_colors)

    colors = [pygame.Color(0, 0, 0) for _ in range(num_colors)]
    for i, color in enumerate(colors): color.hsva = (hues[i], saturation, value, 100)

    return colors
