import cli
num_nodes, = cli.request(["number of nodes", int, 12])

import pygame
import numpy as np
from random import randint
import math
from typing import Tuple, List

# network = generate_network(num_nodes)
# importance = pagerank(network)

class Bubble:
    screen : pygame.Surface = None
    screen_size : Tuple[int, int] = (0, 0)
    bubbles : List["Bubble"] = []
    
    def __init__(self, index : int, mass : float) -> None:
        Bubble.bubbles.append(self)
        width, height = Bubble.screen_size

        self.pos = np.array([randint(0, width - 1), randint(0, height - 1)], dtype="float64")
        self.vel = np.array([0, 0], dtype="float64")

        self.mass = mass
        self.indices = [i for i in range(randint(1, 4)) if i != index]

    @staticmethod
    def init(screen : pygame.Surface) -> None:
        Bubble.screen = screen
        Bubble.screen_size = screen.get_size()

    @staticmethod
    def update_all(delta_time : float) -> None:
        for bubble in Bubble.bubbles: bubble.update(delta_time)

    @staticmethod
    def show_all() -> None:
        for bubble in Bubble.bubbles: bubble.show_lines()
        for bubble in Bubble.bubbles: bubble.show_bubble()

    def update(self, delta_time : float) -> None:
        width, height = Bubble.screen_size

        # Center seeking force
        CENTER_SEEKING_FACTOR = 0.05
        
        center_seeking = [width / 2, height / 2] - self.pos
        center_seeking = center_seeking * CENTER_SEEKING_FACTOR * delta_time
        self.vel += center_seeking

        # Bubble avoding force
        AVOIDANCE_FACTOR = 2.0

        for other in Bubble.bubbles:
            if other is self: continue
            towards = self.pos - other.pos
            self.vel += towards / (np.linalg.norm(towards) ** 2) * AVOIDANCE_FACTOR

        # Connection limiting force
        CONNECTION_PULL_FACTOR = 8.0
        CONNECTION_MAX_LENGTH = 150.0

        for index in self.indices:
            towards = self.pos - Bubble.bubbles[index].pos
            magnitude = np.linalg.norm(towards)

            if magnitude > CONNECTION_MAX_LENGTH:
                self.vel += (-towards) / (np.linalg.norm(towards) ** 2) * CONNECTION_PULL_FACTOR

        # Apply forces
        self.vel *= np.interp(self.mass, [0, 1], [0.96, 0.75])
        self.pos += self.vel

    def get_draw_info(self) -> Tuple[float, Tuple[int, int, int]]:
        radius = self.mass * 30 + 5
        
        mx, my = pygame.mouse.get_pos()
        is_highlighted = ((self.pos[0] - mx) ** 2 + (self.pos[1] - my) ** 2) ** 0.5 < radius

        color = (160, 160, 255, 20) if is_highlighted else (60, 60, 190)
        
        return (radius, color, is_highlighted)

    def show_lines(self) -> None:
        _, color, is_highlighted = self.get_draw_info()
        LINE_SPACING = 5

        for index in self.indices:
            other = Bubble.bubbles[index]
            
            angle = math.atan2(self.pos[1] - other.pos[1], self.pos[0] - other.pos[0])
            offset = [math.cos(math.pi / 2 + angle) * LINE_SPACING, math.sin(math.pi / 2 - angle) * LINE_SPACING]

            darkness = min(max(1 - np.linalg.norm(self.pos - other.pos) / 300, 0.1), 1)
            line_color = color
            if not is_highlighted: line_color = (color[0] * darkness + 35 * (1 - darkness), color[1] * darkness + 35 * (1 - darkness), color[2] * darkness + 35 * (1 - darkness))

            pygame.draw.line(Bubble.screen, line_color, self.pos + offset, other.pos + offset, 1)

    def show_bubble(self) -> None:
        radius, color, _ = self.get_draw_info()
        pygame.draw.circle(Bubble.screen, color, self.pos, radius)    

#
#
#

size = width, height = (600, 600)

pygame.init()

screen = pygame.display.set_mode(size)
pygame.display.set_caption(f"Bubble Network   ( n = {num_nodes} )")
pygame.display.set_icon(pygame.Surface((1, 1)))

clock = pygame.time.Clock()

Bubble.init(screen)

for i in range(num_nodes):
    mass = (((num_nodes - i) / num_nodes) ** 4) * 0.8 + 0.2
    Bubble(i, mass)

should_close = False

while not should_close:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: should_close = True
    
    delta_time = clock.tick(60) * 0.001
    screen.fill((35, 35, 35))

    Bubble.update_all(delta_time)
    Bubble.show_all()

    pygame.display.flip()

pygame.quit()
