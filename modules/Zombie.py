import random
import pygame


class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        super(Zombie, self).__init__()

        self.image = pygame.image.load('material/images/Zombie_0.png').convert_alpha()
        self.images = [pygame.image.load
                       ('material/images/Zombie_{}.png'.format(i)).convert_alpha() \
                       for i in range(0, 22)]
        self.dieimages = [pygame.image.load
                          ('material/images/ZombieDie_{}.png'.format(i)).convert_alpha() \
                          for i in range(0, 10)]
        self.attack_images = [pygame.image.load
                              ('material/images/ZombieAttack_{}.png'.format(i)).convert_alpha()\
                              for i in range(0, 21)]
        self.rect = self.images[0].get_rect()
        self.rect.top = 45 + random.randrange(0,4)*125
        self.rect.left = 1200
        self.energy = 5
        self.speed = 2
        self.die_time = 0
        self.isMeetPlant = False
        self.isAlive = True


    def update(self, *args):
        if self.energy > 0:
            if self.isMeetPlant:
                self.image = self.attack_images[args[0] % len(self.attack_images)]
            else:
                self.image = self.images[args[0] % len(self.images)]
            if self.rect.left > 250 and not self.isMeetPlant:
                self.rect.left -= self.speed
        else:
            if self.die_time < 20:
                self.image = self.dieimages[self.die_time//2]
                self.die_time += 1
            else:
                if self.die_time > 30:
                    self.kill()
                else:
                    self.die_time += 1