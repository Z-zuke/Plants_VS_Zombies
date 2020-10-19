import random
import pygame
from modules.Zombie import Zombie

class FlagZombie(Zombie):
    def __init__(self):
        super(FlagZombie, self).__init__()

        self.image = pygame.image.load('material/images/FlagZombie_0.png').convert_alpha()
        self.images = [pygame.image.load('material/images/FlagZombie_{}.png'.format(i)).convert_alpha() \
                       for i in range(0, 12)]

        self.speed = 3
        self.energy = 4
