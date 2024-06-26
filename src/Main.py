import pygame, sys, math, random

from Grid import Grid
from Game import Game
from Tower import Tower
from Base import Base, EnemyBase
from Enemy import Enemy

from CONSTANT import *

pygame.init()

pygame.display.set_caption('Tower Defense - A New Frontier')

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

clock = pygame.time.Clock()

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
        tower.update()

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
    clock.tick(game.fps)
