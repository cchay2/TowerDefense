import pygame
import math

class Projectile:
    def __init__(self, x, y, target, tower, speed=10):
        self.x = x
        self.y = y
        self.target = target
        self.tower = tower

        self.width = 5
        self.height = self.width

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = "black"

        self.speed = speed
        self.calculate_direction()

    def calculate_direction(self):
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance != 0:
            self.dx = dx / distance * self.speed
            self.dy = dy / distance * self.speed
        else:
            self.dx = 0
            self.dy = 0

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.topleft = (self.x, self.y)

        # Check if the projectile has exceeded the tower's range
        if self.distance_to(self.tower) > self.tower.range * 10:
            return True  # Indicates the projectile should be removed
        return False

    def distance_to(self, target):
        dx = self.x - target.x
        dy = self.y - target.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
