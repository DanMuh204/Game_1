import pygame


class Baff(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('pink')
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):  # camera shift x
        self.rect.x += x_shift