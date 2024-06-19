import sys

from collections import deque
from CONSTANT import *

class Grid:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cols = width // cell_size
        self.rows = height // cell_size
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def update_grid(self, towers):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for tower in towers:
            col = tower.x // self.cell_size
            row = tower.y // self.cell_size
            self.grid[row][col] = 1

    def get_neighbors(self, node):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        neighbors = []
        for direction in directions:
            neighbor = (node[0] + direction[0], node[1] + direction[1])
            if 0 <= neighbor[0] < self.rows and 0 <= neighbor[1] < self.cols:
                if self.grid[int(neighbor[0])][int(neighbor[1])] == 0:
                    neighbors.append(neighbor)
        return neighbors

    def bfs(self, start, goal):
        queue = deque([start])
        came_from = {start: None}
        
        while queue:
            current = queue.popleft()

            if current == goal:
                path = []
                while current is not None:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]

            for neighbor in self.get_neighbors(current):
                if neighbor not in came_from:
                    queue.append(neighbor)
                    came_from[neighbor] = current

        return []