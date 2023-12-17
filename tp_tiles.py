"""
В этом модуле определяется класс Tp
"""
import pygame  # импортируем библиотеку


class Tp(pygame.sprite.Sprite):
    """Этот класс описывает объект блока телепортации

        Блок телепортации отвечает за возвращение игрока в overworld
    """
    def __init__(self, pos, size):
        """
        Инициализация объекта tp

        :param pos: позиция, на которой будет находиться topleft отображения телепорта
        :type pos: tuple
        :param size: размер нарисованного телепорта (этот параметр будет умножен на 64)
        :type size: int
        """
        super().__init__()  # инициализация класса Sprite
        self.image = pygame.Surface((size, size))
        """поверхность размера (size, size)"""
        self.image.fill('green')
        self.rect = self.image.get_rect(topleft=pos)
        """прямоугольник, для которого topleft=pos"""

    def update(self, x_shift):
        """
        Функция движения камеры по горизонтали для данного объекта

        :param x_shift: величина смещения камеры (карты) по горизонтали для данного объекта
        :type x_shift: int
        """
        self.rect.x += x_shift
