import pygame  # импортируем основную библиотеку для игры
import sys  # импортируем для завершения программы при возникновении проблемы
import re  # импортируем для последующего удаления из считанной из файла строки лишних символов
from settings import *  # импортируем настройки из settings
from level import Level  # импортируем класс Level из level.py
from overworld import Overworld  # импортируем класс Overworld из overwold.py


class Game:  # объявляем класс игры, через который будем обращаться к объектам классов Level и Overworld и не только
    def __init__(self):  # функция инициализации объектов
        with open('save_level', 'r') as f1:  # чтение файла сохранения - открытого уровня
            max_level = f1.read()
        with open('save_health', 'r') as f2:  # чтение файла сохранеия - здоровья
            max_health = f2.read()
        self.max_level = int(re.sub("[^0-9]", "", max_level[0]))  # записываем только численное значение
        self.max_health = int(re.sub("[^0-9]", "", max_health))  # записываем только численное значение
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)  # объект класса Overworld
        self.status = 'overworld'  # текущий статус игры

    def create_level(self, current_level):  # функция создания уровня
        self.level = Level(current_level, screen, self.create_overworld, self.change_max_health)  # объект класса Level
        # создаётся уровень номер current_level, отрисовка на screen,передаём методы create_overworld, change_max_health
        self.status = 'level'  # игрок находится в level

    def create_overworld(self, current_level, new_max_level):  # функция создания верхнего мира
        if new_max_level > self.max_level:  # если разблокирован новый уровень
            self.max_level = new_max_level  # то назначаем его новым максимальным доступным уровнем
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)  # созд. и отрис. Overworld
        # принимается перменменные и метод создания уровня
        self.status = 'overworld'  # игрок находится в overworld

    def change_max_health(self, amount):  # функция изменения здоровья
        self.max_health += amount  # на определённое значение, пришедшее в аргументе функции
        return self.max_health  # возвращает значение

    def run(self):  # функция запуска игры, которая в зависимости от статуса создаст overwolrd / level
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.level.level_interface(self.max_health)  # вызов метода отрисовки интерфейса с показателем здоровья


pygame.init()  # инициация pygame
screen = pygame.display.set_mode((screen_width, screen_height))  # создаём окно с параметрами ширины и высоты
clock = pygame.time.Clock()  # устанавливаем таймер для частоты обновления экрана
game = Game()  # создали объекта game, при запуске которого (метод run) будет запускаться остальная логика игры

while True:  # цикл для работы программы, заверщаемый при закрытии окна
    for event in pygame.event.get():  # обрабатываем каждое событие из очереди событий pygame
        if event.type == pygame.QUIT:  # если тип переменной event есть закрытие окна
            pygame.quit()  # выключить инициализированные модули pygame
            sys.exit()  # завершение программы при возникновении ошибки

    screen.fill('black')  # заполнить поверхность окна черным цветом
    game.run()  # вызов метода run для объекта game класса Game

    pygame.display.update()  # обновляем поверхность окна игры
    clock.tick(60)  # установим значение частоты обновления экрана (при её увеличении увеличеватся скорость игры)
