import pygame, re
from tiles import Tile
from tp_tiles import Tp
from baffs import Baff
from enemy import  Enemy, InvisibleBlocks
from settings import tile_size, screen_width, screen_height
from player import Player
from game_data import levels

class Level:
    def __init__(self, current_level, surface, create_overworld, change_max_health):

        # level setup
        self.display_surface = surface
        self.current_level = current_level
        self.level_data = levels[self.current_level]['content']
        self.setup_level(self.level_data)
        self.font = pygame.font.Font(None, 30)
        self.world_shift = 0
        self.current_x = 0

        #overworld connection

        self.create_overworld = create_overworld
        self.new_max_level = levels[self.current_level]['unlock']
        # dust
        self.player_on_ground = False
        # Player setup
        self.goal = pygame.sprite.GroupSingle()

        self.change_max_health = change_max_health

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.teleport = pygame.sprite.Group()
        self.baff_new_heart = pygame.sprite.Group()
        self.enemy = pygame.sprite.Group()
        self.invsblocks = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                elif cell == 'P':
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
                elif cell == 'T':
                    tile_tp = Tp((x,y), tile_size)
                    self.teleport.add(tile_tp)
                elif cell == 'B':
                    tile_baff = Baff((x,y), tile_size / 2)
                    self.baff_new_heart.add(tile_baff)
                elif cell == 'E':
                    enemy_rect = Enemy((x,y), tile_size)
                    self.enemy.add(enemy_rect)
                elif cell == 'I':
                    invs = InvisibleBlocks((x,y), tile_size)
                    self.invsblocks.add(invs)

    def level_interface(self, amount):
        curr_hearts_surf = self.font.render(f'{str(amount)} Hearts now', False, 'white')
        curr_hearts_rect = curr_hearts_surf.get_rect(midleft = (135, 115))
        self.display_surface.blit(curr_hearts_surf, curr_hearts_rect)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def enemy_collision_reverse(self):
        for enemy in self.enemy.sprites():
            if pygame.sprite.spritecollide(enemy, self.invsblocks, False):
                enemy.reversed()

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
            #self.fps_modificator_logic = False
            new_max_health = self.change_max_health(-1)
            if new_max_health < 1:
                new_max_health = self.change_max_health(1)
            with open('save_health', 'w') as f_health:
                f_health.write(str(new_max_health))
            self.create_overworld(self.current_level, 0)

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.teleport, False):
            #self.fps_modificator_logic = False
            self.create_overworld(self.current_level, self.new_max_level)
            with open('save_level', 'r') as f_old:
                current_level_in_file = f_old.read()
                current_level_in_file = int(re.sub("[^0-9]", "", current_level_in_file[0]))
            with open('save_level', 'w') as f_new:
                f_new.write(str(max(self.new_max_level, current_level_in_file)))

    def check_baff_collisions(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.baff_new_heart, True):
            new_max_health = self.change_max_health(1)
            with open('save_health', 'w') as f_health:
                f_health.write(str(new_max_health))

    """"
    def check_speed_baff(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.baff_speed, False):
            self.fps_modificator_logic = True
        if self.fps_modificator_logic == True:
            return
        else:
            return 

    
    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_overworld(self.current_level, self.new_max_level)
    """
    def run(self):

        # level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.teleport.update(self.world_shift)
        self.teleport.draw(self.display_surface)
        self.baff_new_heart.update(self.world_shift)
        self.baff_new_heart.draw(self.display_surface)
        self.scroll_x()

        # enemy
        self.enemy.update(self.world_shift)
        self.enemy.draw(self.display_surface)
        self.invsblocks.update(self.world_shift)
        self.enemy_collision_reverse()

        # player
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
        self.check_death()
        self.check_win()
        self.check_baff_collisions()
        #self.check_win()