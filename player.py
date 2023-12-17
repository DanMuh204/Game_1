"""
В этом модуле определяется класс Player
"""
import pygame


class Player(pygame.sprite.Sprite):
    """Этот класс описывает объект игрок

        Объект игрок отвечает за отрисовку на экране и движения игрока
    """
    def __init__(self, pos):
        """
        Инициализация объекта tp

        :param pos: позиция, на которой будет находиться topleft отображения игрока
        :type pos: tuple
        """
        super().__init__()  # инициализация класса Sprite
        self.image = pygame.Surface((32, 64))
        """поверхность размера 32 на 64"""
        self.image.fill('blue')
        self.rect = self.image.get_rect(topleft=pos)
        """прямоугольник, для которого topleft=pos"""

        # Движение игрока
        self.direction = pygame.math.Vector2(0, 0)
        """Создаём переменную движения (вектора) игрока"""
        self.speed = 8
        """Создаём переменную скорости игрока"""
        self.gravity = 0.8
        """Создаём переменную модификатора гравитации"""
        self.jump_speed = -16
        """Создаём переменную скорости прыжка"""

        # Статусы игрока
        self.on_ground = False
        """Создаём переменную, отвечающую за проверку нахождения игрока на 'полу'"""

    def get_input(self):
        """
        Функция распознавания нажатия определённых клавиш и изменения движения игрока в соответствии с ними
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def apply_gravity(self):
        """
        Функция применения гравитации к игроку
        """
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        """
        Функция прыжка игрока (изменения направления по вертикали)
        """
        self.direction.y = self.jump_speed

    def update(self):
        """
        Функция обновления проверки нажатия
        """
        self.get_input()
