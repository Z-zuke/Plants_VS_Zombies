import time

import pygame
import random


WIDTH = 400
HEIGHT = 500
FPS = 60

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()  # sound init
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Test Game')  # set windows title

myfont = pygame.font.Font(None, 60)
# render函数第一个参数是要绘制的文本，第二个参数是启用抗锯齿能力，第三个参数是文本的颜色。
textImg = myfont.render('pygame', True, WHITE)

# Game Loop
running = True
count = 0
start = time.time()
clock = pygame.time.Clock()
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    for event in pygame.event.get():
        # check for closing event
        if event.type == pygame.QUIT:
            running = False

    # update
    count += 1
    now = time.time()
    fps = count / (now-start)
    fpsImg = myfont.render(str(fps), True, WHITE)

    screen.fill(BLACK)
    screen.blit(fpsImg, (100, 100))
    # after drawing down, flip the display
    pygame.display.flip()

pygame.quit()