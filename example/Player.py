import pygame
import os


WIDTH = 400
HEIGHT = 500

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # create a rectangle for sprite image
        self.image = pygame.Surface((50,50))
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)

    def update(self):
        self.rect.x += 5;
        if self.rect.left > WIDTH:
            self.rect.right = 0