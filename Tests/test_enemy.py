"""В данном модуле происходит тестирование функций reversed и move из класса Enemy"""
import pygame
import pytest
from enemy import Enemy

test_enemy_1 = Enemy((10, 10), 60)
"""Враг для теста test_move_1"""
test_enemy_2 = Enemy((10, 10), 60)
"""Враг для теста test_reversed_1"""
test_enemy_3 = Enemy((10, 10), 60)
"""Враг для теста test_move_2"""


def test_move_1():
    """
    Функция для тестирования функции движения врага. Двигаем его на 1 вправо
    """
    test_enemy_1.move()
    assert test_enemy_1.rect.x == 11


def test_reversed_1():
    """
    Функция для тестирования функции разворота врага. Разворачиваем его.
    """
    test_enemy_2.reversed()
    assert test_enemy_2.speed == -1


def test_move_2():
    """
    Функция для тестирования функций разворота и движения врага. Разворачиваем и двигаем его.
    """
    test_enemy_3.reversed()
    test_enemy_3.move()
    assert test_enemy_3.rect.x == 9
