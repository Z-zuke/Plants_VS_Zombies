import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, rect, win_size):
        super(Bullet, self).__init__()

        self.image = pygame.image.load('material/images/Bullet_1.png')
        self.rect = self.image.get_rect()
        # init position
        self.rect.left, self.rect.top = rect[0]+45, rect[1]
        self.width, self.height = win_size[0], win_size[1]

        self.speed = 5

    def update(self, *args):
        if self.rect.left < self.width:
            self.rect.left += self.speed
        else:
            self.kill()