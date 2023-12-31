"""
В этом модуле определяются классы Enemy и InvisibleBlocks
"""
import pygame  # импортируем библиотеку


class Enemy(pygame.sprite.Sprite):  # создаём класс для врагов
    """Этот класс описывает объект враг

        Враг умеет передвигаться по горизонтали в обе стороны
    """
    def __init__(self, pos, size):  # инициализируем объекты позиция и размер
        """
        Инициализация объекта enemy

        :param pos: позиция, на которой будет находиться topleft отображения врага
        :type pos: tuple
        :param size: размер нарисованного врага (этот параметр будет умножен на 64)
        :type size: int
        """
        super().__init__()  # инициализация класса Sprite
        self.speed = 1  # создаём переменную скорости противника
        """создаём переменную скорости врага, равный единице"""
        self.image = pygame.Surface((size, size))  # создаём поверхность определённого размера
        """поверхность размера (size, size)"""
        self.image.fill('purple')  # придаём этой поверхности цвет
        self.rect = self.image.get_rect(topleft=pos)  # делаем на этой поверхности прямоугольник
        """прямоугольник, для которого topleft=pos"""

    def move(self):  # функция движения врага
        """
        Эта функуия отвечает за движение врага по х=координате в соответствии со скоростью (self.speed)
        """
        self.rect.x += self.speed  # изменения х-координаты врага в соответсвии со скоростью

    def reversed(self):  # функция придания противнику обратной скорости
        """
        Эта функция придаёт противнику скорость, обратрную его (т.е. разворачивает его)
        """
        self.speed *= -1  # меняем скорость противника на отрицательную

    def update(self, x_shift):  # функция движение камеры по горизонтали и движения противника
        """
        Функция движения камеры по горизонтали для данного объекта и вызов функции движения противника

        :param x_shift: величина смещения камеры (карты) по горизонтали для данного объекта
        :type x_shift: int
        """
        self.rect.x += x_shift  # двигаем наши tile по горизонтали в соответсвие со значением смещения камеры
        self.move()  # вызываем функцию движения противника


class InvisibleBlocks(pygame.sprite.Sprite):  # создаём класс для невидимых препятствий на пути врагов
    """Этот класс описывает объект невидимый блок

        Невидимый блок ограничивает область передвижения врага
    """
    def __init__(self, pos, size):  # инициализируем объекты позиция и размер
        """
        Инициализация объекта невидимый блок

        :param pos: позиция, на которой будет находиться topleft отображения (без цвета) невидимого блока
        :type pos: tuple
        :param size: размер отображения (без цвета) невидимого блока (этот параметр будет умножен на 64)
        :type size: int
        """
        super().__init__()  # инициализация класса Sprite
        self.image = pygame.Surface((size, size))  # создаём поверхность определённого размера
        """поверхность размера (size, size)"""
        self.rect = self.image.get_rect(topleft=pos)  # делаем на этой поверхности прямоугольник
        """прямоугольник, для которого topleft=pos"""

    def update(self, x_shift):  # функция движение камеры по горизонтали
        """
        Функция движения камеры по горизонтали для данного объекта

        :param x_shift: величина смещения камеры (карты) по горизонтали для данного объекта
        :type x_shift: int
        """
        self.rect.x += x_shift  # двигаем наши tile по горизонтали в соответствии со значением смещения камеры
