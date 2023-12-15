import pygame


class Tp(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('green')
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):  # camera shift
        self.rect.x += x_shift

