import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('brown')
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):  # camera shift x
        self.rect.x += x_shift


class FinalBlock(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('gold')
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):  # camera shift x
        self.rect.x += x_shift
