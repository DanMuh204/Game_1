"""В этом модуле определяется класс Level"""
import pygame
import re
from tiles import Tile
from tp_tiles import Tp
from baffs import Baff
from enemy import Enemy, InvisibleBlocks
from settings import tile_size, screen_width, screen_height
from player import Player
from game_data import levels


class Level:
    """Этот класс описывает объект уровень

        Объект уровень отвечает за создание уровня, интерфейс уровня, 'камеру' (то есть смещение уровня), вертикальную и
        горизонтальную коллизию (столкновение игрока с объектами по х-координате и у-координате), коллизию врага с
        невидимыми объектами, проверку смерти игрока, проверку победы игрока, проверку получения баффа, коллизию игрока
        с врагом (как по вертикали, так и по горизонтали).
    """
    def __init__(self, current_level, surface, create_overworld, change_max_health):
        """
        Инициализация объекта level

        :param current_level: текущий уровень
        :type current_level: int
        :param surface: экран, на котором всё отображается
        :param create_overworld: функция создания overworld
        :param change_max_health: функция изменения здоровья
        """

        # Настройки уровня
        self.display_surface = surface
        """Поверхность на экране"""
        self.current_level = current_level
        """Переменная, содержащая значение текущего уровня"""
        self.level_data = levels[self.current_level]['content']
        """Переменная, содержащая карту уровня"""
        self.setup_level(self.level_data)
        self.world_shift = 0
        """Переменная смещения всех объектов"""
        self.font = pygame.font.Font(None, 30)
        """Переменная, содержащая шрифт для интерфейса"""
        self.change_max_health = change_max_health
        """Функция изменения значения очков здоровья"""

        # Соединение с overworld
        self.create_overworld = create_overworld
        """Функция создания overworld"""
        self.new_max_level = levels[self.current_level]['unlock']
        """Переменная, содержащя разблокированный после прохождения текущего новый уровень"""

    def setup_level(self, layout):
        """
        Функция создания групп спрайтов объектов уровней в соответствии с картой уровня.

        :param layout: Содержимое карты уровня
        """
        self.tiles = pygame.sprite.Group()
        """Группа спрайтов плиток (поверхности)"""
        self.player = pygame.sprite.GroupSingle()
        """Группа спрайтов игрока"""
        self.teleport = pygame.sprite.Group()
        """Группа спрайтов телепортов"""
        self.baff_new_heart = pygame.sprite.Group()
        """Группа спрайтов баффов"""
        self.enemy = pygame.sprite.Group()
        """Группа спрайтов врагов"""
        self.invsblocks = pygame.sprite.Group()
        """Группа спрайтов невидимых блоков"""

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
                    tile_tp = Tp((x, y), tile_size)
                    self.teleport.add(tile_tp)
                elif cell == 'B':
                    tile_baff = Baff((x, y), tile_size / 2)
                    self.baff_new_heart.add(tile_baff)
                elif cell == 'E':
                    enemy_rect = Enemy((x, y), tile_size)
                    self.enemy.add(enemy_rect)
                elif cell == 'I':
                    invs = InvisibleBlocks((x, y), tile_size)
                    self.invsblocks.add(invs)

    def level_interface(self, amount):
        """
        Функция отображения на экране значения здоровья.

        :param amount: Значение очков здоровья
        :type amount: int
        """
        curr_hearts_surf = self.font.render(f'{str(amount)} Health Points', False, 'white')
        curr_hearts_rect = curr_hearts_surf.get_rect(midleft=(135, 115))
        self.display_surface.blit(curr_hearts_surf, curr_hearts_rect)

    def scroll_x(self):
        """
        Функция перемещения всех объектов на карте при приближении игрока к правой/левой стороне экрана. Если правый
        центр прямоугольника объекта игрок меньше деленной на 4 ширины экрана и вектор движения объекта игрок меньше 0,
        то смещение мира устанавливается на 4, а скорость игрок на 0. Если правый центр прямоугольника объекта игрок
        меньше 3/4 ширины экрана и вектор движения игрока больше 0, то смещение мира устанавливается на -8, а скорость
        игрока на 0. Иначе смещение миро 0, скорость игрока 8.
        """
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
        """
        Функция проверки горизонтальной коллизии игрока с объектом плитка. Х-координата объекта игрок изменяется в соот-
        ветствии с вектором движения, помноженном на скорость игрока. Когда происходит соприкосновение с объектом плитка
        объекта игрок, то, если вектор по горизонтали меньше нуля (т.е. коллизия слева), координатам левой стороны
        прямоугольника игрока придаются координаты правой стороны, а текущая позиция по х приравнивается к координатам
        левой стороны прямоугольника объекта игрок. Для коллизии справа все ровно наоборот.
        """
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        """
        Функция проверки вертикальной коллизии игрока с объектом плитка. Применяется функция создания 'гравитации'. Если
        происходит коллизия и вектор движения игрока направлен вниз, то нижней части прямоугольника объекта игрок прида-
        ётся координата верхней части объекта игрок, а вектор движения игрока по вертикали приравнивается к нулю. Также
        в переменную проверки нахождения игрока на 'земле' записывается значение true. Иначе (если вектор движения
        игрока направлен вверх), то верхней части прямоугольника объекта игрок придаётся координаты нижней части объекта
        игрок, а вектор движения игрока по вертикали приравнивается к нулю.
        Если игрок на 'земле' и вектор движения игрока по вертикали не равен нулю, то статусу 'на земле' придаётся
        значение false.
        """
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

        if player.on_ground and player.direction.y != 0:
            player.on_ground = False

    def enemy_collision_reverse(self):
        """
        Функция проверки коллизии врага с невидимыми блоками. Если коллизия произошла, то вызывается функция придания
        объекту враг обратной скорости (из класса Enemy).
        """
        for enemy in self.enemy.sprites():
            if pygame.sprite.spritecollide(enemy, self.invsblocks, False):
                enemy.reversed()

    def check_death(self):
        """
        Проверка игрока на смерть при выпадении из мира. Если верхняя половина прямоугольника объекта игрок ниже значе-
        ния высоты экрана, то от здоровья отнимается 10 единиц. Если здоровья оказывается ниже единицы, то показатель
        очков здоровья меняется на 10 и это значение записывается в файл сохранения здоровья. После всего этого создаёт-
        ся overworld.
        """
        if self.player.sprite.rect.top > screen_height:
            new_max_health = self.change_max_health(-10)
            if new_max_health < 1:
                new_max_health = self.change_max_health(10)
            with open('save_health', 'w') as f_health:
                f_health.write(str(new_max_health))
            self.create_overworld(self.current_level, 0)

    def check_win(self):
        """
        Функция проверки победы игрока в уровне. Если происходит коллизия с объектом телепорт, то создаётся overworld,
        читается текущее сохранённое значение доступного уровня и записывается в сохранения новое значение доступного
        уровня (максимальное из разблокированного уровня и записанного в сохранении разблокированного уровня).
        """
        if pygame.sprite.spritecollide(self.player.sprite, self.teleport, False):
            self.create_overworld(self.current_level, self.new_max_level)
            with open('save_level', 'r') as f_old:
                current_level_in_file = f_old.read()
                current_level_in_file = int(re.sub("[^0-9]", "", current_level_in_file[0]))
            with open('save_level', 'w') as f_new:
                f_new.write(str(max(self.new_max_level, current_level_in_file)))

    def check_baff_collisions(self):
        """
        Функция проверки коллизии с объектом бафф. Если произошло соприкосновение, то объект бафф удаляется, а здоровье
        увеличивается на 15 единиц и новое значение записывается в файл сохранения здоровья.
        """
        if pygame.sprite.spritecollide(self.player.sprite, self.baff_new_heart, True):
            new_max_health = self.change_max_health(15)
            with open('save_health', 'w') as f_health:
                f_health.write(str(new_max_health))

    def check_enemy_collisions(self):
        """
        Функция проверки столкновения игрока и врага

        Если игрок столкнулся с врагом сверху (т.е. если нижняя часть прямоугольника игрока находиться выше центра пря-
        моугольника врага и вектор движения игрока по у больше или равен 0 (чтобы исключить убийство при соприкосновении
        с боковой стороной врага в падении)), то враг умирает, иначе здоровье уменьшается на 1 каждые шестьдесят
        миллисекунд. В случае, если здоровье опустилось до нуля, происходит выход в overworld, здоровье ставиться на 10
        единиц и это значение записывается в файл сохранения.
        """
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy, False)
        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                """Переменная, хранящая значение центра прямоугольника по у-координате объекта враг """
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    enemy.kill()
                else:
                    new_max_health = self.change_max_health(-1)
                    if new_max_health < 1:
                        self.create_overworld(self.current_level, 0)
                        new_max_health = self.change_max_health(10)
                        f_health = open('save_health', 'w')
                        f_health.write(str(new_max_health))
                        f_health.close()

    def run(self):
        """
        Функция запуска обновлений объектов на экране, отрисовки объектов на экране, 'камеры' (т.е. передвижения мира) и
        запуска функций проверки на коллизии, смерть, победу, получения баффа.
        """

        # Объекты уровня и их смещение
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.teleport.update(self.world_shift)
        self.teleport.draw(self.display_surface)
        self.baff_new_heart.update(self.world_shift)
        self.baff_new_heart.draw(self.display_surface)
        self.scroll_x()

        # Объекты и коллизия, связанные с врагами
        self.enemy.update(self.world_shift)
        self.enemy.draw(self.display_surface)
        self.invsblocks.update(self.world_shift)
        self.enemy_collision_reverse()
        self.check_enemy_collisions()

        # Игрок и функции, с ним связанные
        self.player.update()
        self.player.draw(self.display_surface)
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.check_baff_collisions()
        self.check_death()
        self.check_win()
