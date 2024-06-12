import pygame, sys, random, math, time

pygame.init()

pygame.display.set_caption('Tower Defense - A New Frontier')

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

SCREEN = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )

clock = pygame.time.Clock()

class Game:
	def __init__(self):
		self.fps = 60
		self.tower_list = []
		self.towers = 0

		self.enemy_list = []

	def hasPathChanged(self):
		if len(self.tower_list) != self.towers:
			self.towers = len(self.tower_list)
			return True
		else:
			return False

class Tower:
	def __init__(self, x, y):
		self.hp = 10
		self.range = 20 # actual pixel distance calculated at 10x
		self.damage = 1
		self.speed = .5 # How many shots fired per second?

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
		pygame.draw.circle(surface, "green", (self.x+self.width//2, self.y+self.height//2), self.range*10, 1)

	def shoot(self, target):
		if self.timer <= self.shoot_end:
			self.shooting = True
		else:
			self.shooting = False

		if not self.shooting:
			print("BANG")
			target.takeDamage(self.damage)
			self.shoot_start = self.timer
			self.shoot_end = self.shoot_start + round(self.speed*60)

	def sentry(self, enemy_list):
		self.acquireTarget(enemy_list)

	def acquireTarget(self, enemy_list):
		for enemy in enemy_list:
			#print(self.distanceTo(enemy))
			if self.distanceTo(enemy) < self.range*10:
				self.shoot(enemy)


		#print()

	def distanceTo(self, target):
		## Assuming target is an object
		a = (self.x-target.center[0])**2
		b = (self.y-target.center[1])**2

		return math.sqrt(a+b)

class Base:
	def __init__(self, hp, x, y, color):
		self.hp = hp
		self.x = x
		self.y = y

		self.width = 100
		self.height = 100

		self.center = (self.x+self.width//2, self.y+self.height//2)

		self.color = color

	def draw(self, surface):
		pygame.draw.rect(surface, "dark red", pygame.Rect(self.x, self.y, self.width, self.height))


class EnemyBase(Base):
	def __init__(self, hp, x, y, color):
		Base.__init__(self, hp, x, y, color)
		self.spawn_time = 0
		self.spawn_end = 0
		self.hasSpawned = False
		self.spawn_cd = 1 # 1 second or every 60 frames

	def spawnEnemy(self, enemy_list, timer):
		"""sps is spawn per second. multiply by 60 or fps"""
		if not self.hasSpawned:
			enemy_list.append(Enemy(self.center[0], self.center[1]))
			self.spawn_time = timer
			self.spawn_end = timer + self.spawn_cd*60
			self.hasSpawned = True

		if self.spawn_end <= timer:
			self.hasSpawned = False

	def calculatePath(self, target):
		"""For simple movement, calculates a path to the target, or player base, for all simple enemy units to follow"""
		path = []


		return path

	def draw(self, surface):
		pygame.draw.rect(surface, "dark red", pygame.Rect(self.x, self.y, self.width, self.height))


class Enemy:
	def __init__(self, x, y):
		self.movement = 10
		self.hp = 5

		self.x = x # 500
		self.y = y # 400

		self.width = 50
		self.height = 50

		self.center = (self.x+self.width//2, self.y+self.height//2)
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

		self.speed = 10
		self.direction = "east"
		self.path = []

	def move(self, tower_list, target):
		"""
		Check to see if it is colliding with a tower. If so then change direction to move right
		"""
		if self.direction == "east":
			moveright_rect = pygame.Rect(self.x+self.speed, self.y, self.width, self.height)

			for tower in tower_list:
				if moveright_rect.colliderect(tower.rect):
					self.direction = "north"
					break

		elif self.direction == "north":
			moveup_rect = pygame.Rect(self.x, self.y-self.speed, self.width, self.height)
			moveright_rect = pygame.Rect(self.x+self.speed, self.y, self.width, self.height)

			self.direction = "east"

			for tower in tower_list:
				if moveright_rect.colliderect(tower.rect):
					self.direction = "north"
					break

				if moveup_rect.colliderect(tower.rect):
					self.direction = "south"
					break


		elif self.direction == "south":
			movedown_rect = pygame.Rect(self.x, self.y-self.speed, self.width, self.height)
			moveright_rect = pygame.Rect(self.x+self.speed, self.y, self.width, self.height)

			for tower in tower_list:
				if movedown_rect.colliderect(tower.rect):
					if moveright_rect.colliderect(tower.rect):
						self.direction = "north"
						break
					else:
						self.direction = "east"
						break

		if self.direction == "east":
			self.x += self.speed
		if self.direction == "west":
			self.x -= self.speed
		if self.direction == "north":
			self.y -= self.speed
		if self.direction == "south":
			self.y += self.speed

		self.center = (self.x+self.width//2, self.y+self.height//2)
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


	def takeDamage(self, damage):
		self.hp -= damage

	def draw(self, surface):
		pygame.draw.rect(surface, "red", self.rect)
		pygame.draw.circle(surface, "black", self.center, 5, 1)


game = Game()

game.tower_list = [Tower(SCREEN_WIDTH//2-50, SCREEN_HEIGHT//2-50), Tower(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-100)]
player_base = Base(10, SCREEN_WIDTH-30, SCREEN_HEIGHT//2-50, "dark green")

enemy_base = EnemyBase(99999999, -70, SCREEN_HEIGHT//2-75, "dark red")
enemy_list = []


#for i in range(5):
#	enemy_list.append( Enemy(random.randint(100, SCREEN_WIDTH-100), random.randint(100, SCREEN_HEIGHT-100)) )

timer = 0

while True:
	timer += 1 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.display.quit()
			pygame.quit()
			sys.exit()

	SCREEN.fill( "sky blue" )

	enemy_base.draw(SCREEN)
	player_base.draw(SCREEN)

	if game.hasPathChanged():
		enemy_base.calculatePath(game.tower_list)

	for tower in game.tower_list:
		tower.draw(SCREEN)
		tower.timer = timer
		tower.sentry(enemy_list)

	enemy_base.spawnEnemy(enemy_list, timer)

	for enemy in enemy_list:
		if enemy.hp <= 0:
			enemy_list.remove(enemy)

		enemy.move(game.tower_list, player_base)
		#print(enemy.x)
		enemy.draw(SCREEN)



	pygame.display.update()
	clock.tick( 60 )