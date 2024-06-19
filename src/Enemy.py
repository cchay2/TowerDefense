import pygame, sys, random, math

from Grid import Grid
from CONSTANT import *

class Enemy:
    def __init__(self, x, y, grid, target):
        self.hp = 10
        self.max_hp = 10

        self.x = x
        self.y = y

        self.width = 50
        self.height = 50

        self.center = (self.x + self.width // 2, self.y + self.height // 2)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.draw_rect = pygame.Rect(self.x+5, self.y+5, self.width-10, self.height-10)

        self.speed = random.choice([2, 2, 2, 5, 5, 10])
        self.path = []
        self.grid = grid
        self.target = target

        self.expire = False

    def calculate_path(self):
        start = (self.y // CELL_SIZE, self.x // CELL_SIZE)
        goal = (self.target.y // CELL_SIZE, self.target.x // CELL_SIZE)
        self.path = self.grid.bfs(start, goal)
        self.path = self.path[1:]

    def move(self):
        if self.path:
            next_node = self.path[0]
            next_x = next_node[1] * CELL_SIZE
            next_y = next_node[0] * CELL_SIZE

            dx = next_x - self.x
            dy = next_y - self.y
            dist = math.sqrt(dx**2 + dy**2)
            if dist != 0:
                dx = dx / dist
                dy = dy / dist

            self.x += dx * self.speed
            self.y += dy * self.speed

            if abs(self.x - next_x) < self.speed and abs(self.y - next_y) < self.speed:
                self.x = next_x
                self.y = next_y
                self.path.pop(0)

        self.center = (self.x + self.width // 2, self.y + self.height // 2)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.draw_rect = pygame.Rect(self.x+5, self.y+5, self.width-10, self.height-10)

    def takeDamage(self, damage):
        self.hp -= damage

    def updateHitPointHpBar(self):
        """Represent player hp on a % scale of 1-10"""
        hp_length = round((self.hp/self.max_hp)*self.width)

        self.current_hp_rect = pygame.Rect(self.x, self.y+self.height, hp_length, 5)
        self.empty_hp_rect = pygame.Rect(self.x, self.y+self.height, self.width, 5)

    def draw(self, surface):
        """Draw the player and hp bar"""
        self.updateHitPointHpBar()

        pygame.draw.rect(surface, "red", self.draw_rect)
        pygame.draw.rect(surface, "black", self.empty_hp_rect)
        pygame.draw.rect(surface, "green", self.current_hp_rect)