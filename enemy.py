import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.speed = 1
        self.image = pygame.Surface((size, size))
        self.image.fill('purple')
        self.rect = self.image.get_rect(topleft=pos)

    def move(self):
        self.rect.x += self.speed

    def reversed(self):
        self.speed *= -1

    def update(self, x_shift):  # camera shift x
        self.rect.x += x_shift
        self.move()


class InvisibleBlocks(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):  # camera shift x
        self.rect.x += x_shift
