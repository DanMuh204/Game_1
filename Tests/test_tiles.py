"""В этом модуле происходит тестирование функции update класса Tile"""
import pygame
import pytest
from tiles import Tile

test_rect_1 = Tile((10, 10), 64)
"""Прямоугольник класса Tile для теста test_1"""
test_rect_2 = Tile((10, 10), 64)
"""Прямоугольник класса Tile для теста test_2"""
test_rect_3 = Tile((10, 10), 64)
"""Прямоугольник класса Tile для теста test_3"""
expected_answer_1 = 11
"""Ожидаемый ответ для test_1"""
expected_answer_2 = 10
"""Ожидаемый ответ для test_2"""
expected_answer_3 = 9
"""Ожидаемый ответ для test_3"""


def test_1():
    """
    Функция для тестирования функции обновления позиции объекта tile при смещении 'камеры'. Смещение равно 1
    """
    test_rect_1.update(1)
    assert expected_answer_1 == test_rect_1.rect.x


def test_2():
    """
    Функция для тестирования функции обновления позиции объекта tile при смещении 'камеры'. Смещение равно 0
    """
    test_rect_2.update(0)
    assert expected_answer_2 == test_rect_2.rect.x


def test_3():
    """
    Функция для тестирования функции обновления позиции объекта tile при смещении 'камеры'. Смещение равно -1
    """
    test_rect_3.update(-1)
    assert expected_answer_3 == test_rect_3.rect.x
