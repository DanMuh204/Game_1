"""В этом модуле определяются классы Node, Icon, Overworld"""
import pygame
from game_data import levels


class Node(pygame.sprite.Sprite):
    """Этот класс описывает объект Node

        Объект Node является представлением уровней в Overworld
    """
    def __init__(self, pos, status, icon_speed):
        """
        Инициализация объекта Node

        :param pos: Позиция, на которой будет находиться topleft отображения node
        :type pos: tuple
        :param status: статус доступности уровня для прохождения игроком
        :type status: str
        :param icon_speed: переменная скорости иконки, представляющей игрока
        :type icon_speed: int
        """
        super().__init__()  # инициализация класса Sprite
        self.image = pygame.Surface((100, 80))
        """поверхность размера 100 на 80"""
        if status == 'available':
            self.image.fill('red')
        else:
            self.image.fill('grey')
        self.rect = self.image.get_rect(center=pos)
        """прямоугольник, для которого topleft=pos"""

        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed / 2), self.rect.centery - (icon_speed / 2),
                                          icon_speed, icon_speed)
        """Зона обнаружения прибытия icon, позже необходимая для остановки движения icon"""


class Icon(pygame.sprite.Sprite):
    """Этот класс описывает объект Icon

        Объект Icon является представлением игрока в Overworld
    """
    def __init__(self, pos):
        """
        Инициализация объекта Icon

        :param pos: Позиция, на которой будет находиться topleft отображения icon
        :type pos: tuple
        """
        super().__init__()  # инициализация класса Sprite
        self.pos = pos
        """Позиция, на которой будет находиться topleft отображения icon, загруженная в переменную"""
        self.image = pygame.Surface((20, 20))
        """поверхность размера 20 на 20"""
        self.image.fill('blue')
        self.rect = self.image.get_rect(center=pos)
        """прямоугольник, для которого topleft=pos"""

    def update(self):
        """
        Функция обновления позиции центра прямоугольника иконки игрока на значение новой позиции
        """
        self.rect.center = self.pos


# Класс Overworld и логика создания overworld заимствованы с ютуб-канала Clear Code
class Overworld:
    """Этот класс описывает объект Overworld

        Объект Overworld является меню переключения уровней, через которое можно выбрать уровень для прохождения игроком
    """
    def __init__(self, start_level, max_level, surface, create_level):
        """
        Инициализация объекта Overworld

        :param start_level: стартовый уровень
        :type start_level: int
        :param max_level: максимальный доступный уровень
        :type max_level: int
        :param surface: экран, на котором всё отображается
        :param create_level: функция создания (перехода на) уровень
        """

        # Настройки
        self.display_surface = surface
        """Поверхность на экране"""
        self.max_level = max_level
        """Переменная максимального доступного уровня"""
        self.current_level = start_level
        """Переменная текущего уровня"""
        self.create_level = create_level
        """Функция создания уровня"""

        # Логика движения иконки
        self.moving = False
        """Переменная статуса движения иконки"""
        self.move_direction = pygame.math.Vector2(0, 0)
        """Вектор движения иконки"""
        self.speed = 8
        """Переменная скорости иконки"""

        # Спрайты
        self.setup_nodes()
        self.setup_icon()

    def setup_nodes(self):
        """
        Функция создания прямоугольников-представлений уровней
        """
        self.nodes = pygame.sprite.Group()
        """Группа спрайтов представлений уровней"""

        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'available', self.speed)
            else:
                node_sprite = Node(node_data['node_pos'], 'locked', self.speed)
            self.nodes.add(node_sprite)

    def draw_paths(self):
        """
        Функция отрисовки пути движения иконки от уровня к уровню
        """
        points = [node['node_pos'] for index, node in enumerate(levels.values()) if index <= self.max_level]
        if self.max_level > 0:
            pygame.draw.lines(self.display_surface, 'red', False, points, 6)

    def setup_icon(self):
        """
        Функция создания иконки в центре представления уровня
        """
        self.icon = pygame.sprite.GroupSingle()
        """Группа (из одного) спрайтов для иконки отображения игрока"""
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def input(self):
        """
        Функция проверки нажатия клавиш.
        """
        keys = pygame.key.get_pressed()

        if not self.moving:
            if keys[pygame.K_d] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data('next')
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_a] and self.current_level > 0:
                self.move_direction = self.get_movement_data('previous')
                self.current_level -= 1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)

    def get_movement_data(self, target):
        """
        Функция получения данных движения иконки. Если цель перейти к следующему уровню, то берётся вектор
        центра прямоугольника представления следующего уровня, если наоборот, то вектор центра прямоугольника
        представления предыдущего уровня. Разница стартового и следующего векторов возвращается

        :param target: Перейти к следующему/предыдущему уровню
        :type target: str
        :return: вектор разницы векторов стартового перед движением уровня и уровня прибытия
        """
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)

        if target == 'next':
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)
        return (end - start).normalize()

    def update_icon_pos(self):
        """
        Функция обновления позиции иконки игрока. Если иконка движется, то позиция спрайта иконки увеличивается на
        вектор направления движения иконки, помноженный на скорость. Если происходит коллизия с зоной остановки иконки,
        то движение останавливается, а вектор движения приводиться к (0,0)
        """
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0, 0)

    def run(self):
        """
        Функция вызова функций класса и отрисовки на экране представлений уровня и игрока
        """
        self.input()
        self.update_icon_pos()
        self.icon.update()
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
# Конец заимствования класса Overworld и логики создания overworld
