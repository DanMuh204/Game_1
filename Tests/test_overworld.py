import unittest
import pytest
import pygame
from overworld import Node

def test_node_init(self):
    pos = (100, 100)
    status = 'available'
    icon_speed = 10
    node = Node(pos, status, icon_speed)
    assert node.rect.center == pos
    assert node.detection_zone == pygame.Rect(node.rect.centerx - (icon_speed / 2), node.rect.centery - (icon_speed / 2), icon_speed, icon_speed)
    if status == 'available':
        assert node.image.get_at((0, 0)) == (255, 0, 0, 255)
    else:
        assert node.image.get_at((0, 0)) == (128, 128, 128, 255)