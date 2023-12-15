class Game:
    def __init__(self):
        self.max_level = 2
        self.overworld = Overworld(1, self.max_level, screen, self.create_level)
        self.status = 'level_1'

    def move_to_leve_2(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()