import pygame, sys, math, random
from collections import deque

pygame.init()

pygame.display.set_caption('Tower Defense - A New Frontier')

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
CELL_SIZE = 50

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

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


grid = Grid(SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE)

game = Game()

tower_list = []

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
        if enemy.hp <= 0 or enemy.expire:
            game.enemy_list.remove(enemy)

        enemy.draw(SCREEN)
        enemy.move()


    ## Display Base Lives
    player_base.checkForLifeLoss(game.enemy_list)
    base_hp_text = "Base Lives: " + str(player_base.hp)
    base_hp_display = my_font.render(base_hp_text, False, "black")
    SCREEN.blit(base_hp_display, (SCREEN_WIDTH-150,SCREEN_HEIGHT-50))

    pygame.display.update()
    clock.tick(60)
