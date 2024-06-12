import pygame, sys, math
from collections import deque

pygame.init()

pygame.display.set_caption('Tower Defense - A New Frontier')

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
CELL_SIZE = 50

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

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
                if self.grid[neighbor[0]][neighbor[1]] == 0:
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

class Game:
    def __init__(self):
        self.fps = 60
        self.tower_list = []
        self.towers = 0
        self.enemy_list = []
        self.path_changed = False

    def hasPathChanged(self):
        if self.path_changed:
            self.path_changed = False
            return True
        return False

    def place_tower(self, x, y):
        new_tower = Tower(x, y)
        self.tower_list.append(new_tower)
        self.path_changed = True

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

        self.shooting = False
        self.shoot_start = 0
        self.shoot_end = 0

        self.timer = 0

    def draw(self, surface):
        pygame.draw.rect(surface, "green", self.rect)
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

class Base:
    def __init__(self, hp, x, y, color):
        self.hp = hp
        self.x = x
        self.y = y

        self.width = 100
        self.height = 100

        self.center = (self.x + self.width // 2, self.y + self.height // 2)

        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

class EnemyBase(Base):
    def __init__(self, hp, x, y, color):
        Base.__init__(self, hp, x, y, color)
        self.spawn_time = 0
        self.spawn_end = 0
        self.hasSpawned = False
        self.spawn_cd = 1  # 1 second or every 60 frames

    def spawnEnemy(self, enemy_list, timer, grid, player_base):
        if not self.hasSpawned:
            enemy = Enemy(self.center[0], self.center[1], grid, player_base)
            enemy_list.append(enemy)
            enemy.calculate_path()
            self.spawn_time = timer
            self.spawn_end = timer + self.spawn_cd * 60
            self.hasSpawned = True

        if self.spawn_end <= timer:
            self.hasSpawned = False

    def draw(self, surface):
        pygame.draw.rect(surface, "dark red", pygame.Rect(self.x, self.y, self.width, self.height))

class Enemy:
    def __init__(self, x, y, grid, target):
        self.movement = 10
        self.hp = 50

        self.x = x
        self.y = y

        self.width = 50
        self.height = 50

        self.center = (self.x + self.width // 2, self.y + self.height // 2)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.speed = 5
        self.path = []
        self.grid = grid
        self.target = target

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

            if self.x < next_x:
                self.x += self.speed
            elif self.x > next_x:
                self.x -= self.speed

            if self.y < next_y:
                self.y += self.speed
            elif self.y > next_y:
                self.y -= self.speed

            if self.x == next_x and self.y == next_y:
                self.path.pop(0)

        self.center = (self.x + self.width // 2, self.y + self.height // 2)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def takeDamage(self, damage):
        self.hp -= damage

    def draw(self, surface):
        pygame.draw.rect(surface, "red", self.rect)
        pygame.draw.circle(surface, "black", self.center, 5, 1)

grid = Grid(SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE)

game = Game()

tower_list = [
    Tower(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50),
    Tower(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2),
    Tower(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100),
    Tower(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200),
]

game.tower_list.extend(tower_list)

player_base = Base(10, SCREEN_WIDTH - 150, SCREEN_HEIGHT // 2 - 50, "dark green")
enemy_base = EnemyBase(99999999, -70, SCREEN_HEIGHT // 2 - 75, "dark red")

timer = 0

while True:
    timer += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = event.pos
                grid_x = (mouse_x // CELL_SIZE) * CELL_SIZE
                grid_y = (mouse_y // CELL_SIZE) * CELL_SIZE
                game.place_tower(grid_x, grid_y)

    # Update the grid with the current tower positions
    grid.update_grid(game.tower_list)

    SCREEN.fill("sky blue")

    enemy_base.draw(SCREEN)
    player_base.draw(SCREEN)

    for tower in game.tower_list:
        tower.draw(SCREEN)
        tower.timer = timer
        tower.sentry(game.enemy_list)

    enemy_base.spawnEnemy(game.enemy_list, timer, grid, player_base)

    if game.hasPathChanged():
        for enemy in game.enemy_list:
            enemy.calculate_path()

    for enemy in game.enemy_list:
        if enemy.hp <= 0:
            game.enemy_list.remove(enemy)

        enemy.draw(SCREEN)
        enemy.move()

    pygame.display.update()
    clock.tick(60)
