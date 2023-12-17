import unittest
import pygame
import pytest
from level import *
from player import Player

class TestScrollX(unittest.TestCase):
    def setUp(self):
        self.player = Player()
        self.world_shift = 0

    def test_scroll_x_shift_right(self):
        self.player.rect.centerx = screen_width / 3
        self.player.direction.x = 1

        Level.scroll_x(self)

        self.assertEqual(self.world_shift, -8)
        self.assertEqual(self.player.speed, 0)

    def test_scroll_x_shift_left(self):
        self.player.rect.centerx = screen_width - (screen_width / 3)
        self.player.direction.x = -1

        Level.scroll_x(self)

        self.assertEqual(self.world_shift, 8)
        self.assertEqual(self.player.speed, 0)

    def test_scroll_x_no_shift(self):
        self.player.rect.centerx = screen_width / 2
        self.player.direction.x = 1

        Level.scroll_x(self)

        self.assertEqual(self.world_shift, 0)
        self.assertEqual(self.player.speed, 8)
