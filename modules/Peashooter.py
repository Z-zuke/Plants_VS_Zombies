import pygame


class Peashooter(pygame.sprite.Sprite):
    def __init__(self, last_time):
        super(Peashooter, self).__init__()
        self.image = pygame.image.load('material/images/Peashooter_00.png').convert_alpha()
        self.images = [pygame.image.load
                      ('material/images/Peashooter_{:02d}.png'.format(i)).convert_alpha()\
                        for i in range(0, 13)]

        self.rect = self.images[0].get_rect()
        self.last_time = last_time
        self.energy = 3 * 15
        self.zombies = set()

    def update(self, *args):
        for zombie in self.zombies:
            if not zombie.isAlive:
                # self.zombies.pop()  # ? remove dead zombie, pop remove the last element
                continue
            self.energy -= 1

        if self.energy <= 0:
            for zombie in self.zombies:
                zombie.isMeetPlant = False
            self.kill()

        self.image = self.images[args[0] % len(self.images)]