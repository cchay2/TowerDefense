import pygame, sys, math

class Tower:
    def __init__(self, x, y):
        self.hp = 10
        self.range = 10  # actual pixel distance calculated at 10x
        self.damage = 1
        self.speed = 1  # How many shots fired per second?

        self.x = x
        self.y = y

        self.width = 50
        self.height = 50

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.draw_rect = pygame.Rect(self.x+5, self.y+5, self.width-10, self.height-10)

        self.shooting = False
        self.shoot_start = 0
        self.shoot_end = 0

        self.timer = 0

    def draw(self, surface):
        pygame.draw.rect(surface, "green", self.draw_rect)

        pygame.draw.circle(surface, "green", (self.x + self.width // 2, self.y + self.height // 2), self.range * 10, 1)

    def shoot(self, target):
        if self.timer <= self.shoot_end:
            self.shooting = True
        else:
            self.shooting = False

        if not self.shooting:
            print("BANG")
            target.takeDamage(self.damage)
            self.shoot_start = self.timer
            self.shoot_end = self.shoot_start + round(self.speed * 60)

    def sentry(self, enemy_list):
        self.acquireTarget(enemy_list)

    def acquireTarget(self, enemy_list):
        for enemy in enemy_list:
            if self.distanceTo(enemy) < self.range * 10:
                self.shoot(enemy)

    def distanceTo(self, target):
        a = (self.x - target.center[0]) ** 2
        b = (self.y - target.center[1]) ** 2

        return math.sqrt(a + b)