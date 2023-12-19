import numpy as np
import lucwia as lw # A simple Pygame wrapper
import pagerank as pr
from itertools import combinations

NUM_NODES = 8
WIDTH, HEIGHT = SIZE = (700, 700)

BACKGROUND_COLOR = (200, 200, 200)
CONNECTION_COLOR = (85, 140, 155)
bubble_colors = lw.generate_colors(NUM_NODES, saturation=70, value=65)

# Data structures

class Bubble:
    def __init__(self, rank) -> None:
        self.position = np.random.uniform([0, 0], [WIDTH, HEIGHT])
        self.rank = rank
        self.color = bubble_colors.pop()

class Connection:
    def __init__(self, b1, b2) -> None:
        self.bubble1, self.bubble2 = b1, b2

# MVC

def rank_to_radius(rank):
    return rank * 250 + 15

class PagerankModel:
    def __init__(self) -> None:
        self.network = pr.Network(NUM_NODES, max_links=2)
        self.bubbles = [Bubble(rank) for rank in pr.pagerank(self.network.to_matrix())]
        self.connections = self.create_connections(self.network.nodes, self.bubbles)
    
    def create_connections(self, nodes, bubbles):
        connections = []
        for i, node in enumerate(nodes):
            links = node[1]
            for j in links: connections.append(Connection(bubbles[i], bubbles[j]))
        return connections

    def update_bubble_positions(self):
        for bubble1, bubble2 in combinations(self.bubbles, 2):
            self.update_bubble_position(bubble1, bubble2)
            self.update_bubble_position(bubble2, bubble1)

    def update_bubble_position(self, b1, b2):
        pos1, pos2 = b1.position, b2.position
        vel = np.zeros(2)

        CENTER_SEEKING_FACTOR = 0.002
        vel += (np.array(SIZE) / 2 - pos1) * CENTER_SEEKING_FACTOR

        towards = pos2 - pos1
        distance = np.linalg.norm(towards)

        AVOIDANCE_DISTANCE = 300
        AVOIDANCE_FACTOR = 0.05
        vel += (towards / distance) * (distance * AVOIDANCE_FACTOR - AVOIDANCE_FACTOR * AVOIDANCE_DISTANCE)

        pos1 += vel * (1 - b1.rank)

class PagerankView:
    def draw_connections(self, connections):
        LINE_SPACING = 8
        for connection in connections:
            pos1, pos2, color = connection.bubble1.position, connection.bubble2.position, connection.bubble1.color

            angle = np.arctan2(pos1[1] - pos2[1], pos1[0] - pos2[0])
            offset = np.array([np.cos(np.pi / 2 + angle), np.sin(np.pi / 2 - angle)]) * LINE_SPACING
            
            lw.line(*(pos1 + offset), *(pos2 + offset), color, w=3)

    def draw_bubbles(self, bubbles):
        for bubble in bubbles:
            pos, rank, color = bubble.position, bubble.rank, bubble.color
            lw.circle(pos[0], pos[1], rank_to_radius(rank), color)

class PagerankController:
    def __init__(self, model, view) -> None:
        self.model, self.view = model, view
    
    def update(self):
        self.model.update_bubble_positions()
        self.view.draw_connections(self.model.connections)
        self.view.draw_bubbles(self.model.bubbles)

if __name__ == "__main__":
    lw.init(SIZE, title=f"PageRank visualisering (antal noder: {NUM_NODES})")
    
    pr_controller = PagerankController(PagerankModel(), PagerankView())

    while not lw.should_close():
        lw.update()
        lw.background(BACKGROUND_COLOR)
        pr_controller.update()
    
    lw.quit()
