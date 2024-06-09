import pygame, sys, random, math, time

pygame.init()

pygame.display.set_caption('Tower Defense - A New Frontier')

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SCREEN = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )

clock = pygame.time.Clock()

# class Arrow: ## Ignore for now
# 	def __init__(self, x, y, damage):
# 		self.damage = damage

# 		self.x = x
# 		self.y = y

# 		self.width = 10
# 		self.height = 10

# 		self.shooting = False
# 		self.shoot_start = 0
# 		self.shoot_end = 0

# 	def draw(self, surface):
# 		pygame.draw.rect(surface, "blue", pygame.Rect(self.x, self.y, self.width, self.height))

class Tower:
	def __init__(self):
		self.hp = 10
		self.range = 10 # actual pixel distance calculated at 10x
		self.damage = 1
		self.speed = 1 # How many shots fired per second?

		self.x = 400
		self.y = 300

		self.width = 50
		self.height = 50

		self.shooting = False
		self.shoot_start = 0
		self.shoot_end = 0

		self.timer = 0

	def draw(self, surface):
		pygame.draw.rect(surface, "green", pygame.Rect(self.x, self.y, self.width, self.height))
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
	def __init__self(self):

class Enemy:
	def __init__(self, x, y):
		self.movement = 10
		self.hp = 1

		self.x = x # 500
		self.y = y # 400

		self.width = 50
		self.height = 50

		self.center = (self.x+self.width//2, self.y+self.height//2)

	def move(self, target):
		pass

	def takeDamage(self, damage):
		self.hp -= damage

	def draw(self, surface):
		pygame.draw.rect(surface, "red", pygame.Rect(self.x, self.y, self.width, self.height))
		pygame.draw.circle(surface, "black", self.center, 5, 1)


tower = Tower()

enemy_list = []

for i in range(5):
	enemy_list.append( Enemy(random.randint(100, 700), random.randint(100, 500)) )

timer = 0


SCREEN.fill( "sky blue" )

tower.draw(SCREEN)
tower.timer = timer
tower.sentry(enemy_list)

for enemy in enemy_list:
	if enemy.hp <= 0:
		enemy_list.remove(enemy)
	enemy.draw(SCREEN)

pygame.display.update()

time.sleep(1)

while True:
	timer += 1 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.display.quit()
			pygame.quit()
			sys.exit()

	SCREEN.fill( "sky blue" )

	tower.draw(SCREEN)
	tower.timer = timer
	tower.sentry(enemy_list)

	for enemy in enemy_list:
		if enemy.hp <= 0:
			enemy_list.remove(enemy)
		enemy.draw(SCREEN)



	pygame.display.update()
	clock.tick( 60 )