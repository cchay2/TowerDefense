from Tower import Tower

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