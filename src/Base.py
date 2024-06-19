from Enemy import Enemy
import pygame

class Base:
    def __init__(self, hp, x, y, color):
        self.hp = hp
        self.x = x
        self.y = y

        self.width = 100
        self.height = 100

        self.center = (self.x + self.width // 2, self.y + self.height // 2)

        self.color = color

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def checkForLifeLoss(self, enemy_list):
        """Check to see if enemy makes contact with base"""
        closest_enemies = enemy_list[:5]
        print(closest_enemies)
        for enemy in closest_enemies:
            if self.rect.colliderect(enemy.rect):
                print("Lose health")
                self.takeDamage()
                enemy.expire = True

    def takeDamage(self):
        self.hp -= 1

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class EnemyBase(Base):
    def __init__(self, hp, x, y, color):
        Base.__init__(self, hp, x, y, color)
        self.spawn_time = 0
        self.spawn_end = 0
        self.hasSpawned = False
        self.spawn_cd = 1  # 1 second or every 60 frames

    def spawnEnemy(self, enemy_list, timer, grid, player_base):
        if not self.hasSpawned:
            enemy = Enemy(self.x+self.width, self.y+50, grid, player_base)
            enemy_list.append(enemy)
            enemy.calculate_path()
            self.spawn_time = timer
            self.spawn_end = timer + self.spawn_cd * 60
            self.hasSpawned = True

        if self.spawn_end <= timer:
            self.hasSpawned = False

            
    def draw(self, surface):
        pygame.draw.rect(surface, "dark red", pygame.Rect(self.x, self.y, self.width, self.height))