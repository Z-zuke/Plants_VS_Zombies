import time
import pygame
import os

from modules.Bullet import Bullet
from modules.Peashooter import Peashooter
from modules.Sunflower import Sunflower
from modules.Wallnut import Wallnut
from modules.Sun import Sun
from modules.Zombie import Zombie
from modules.FlagZombie import FlagZombie


pygame.init()
FPS = 20
window_size = (1200, 600)

screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Plants VS Zombies')
# init backgroud music
pygame.mixer.init()
pygame.mixer.music.load("material/music/02 - Crazy Dave (Intro Theme).mp3")
# game logo
logo = pygame.image.load('material/images/logo.jpg').convert_alpha()
pygame.display.set_icon(logo)
# window's backgroud image
bg_img_path = 'material/images/background1.jpg'
bg_img_obj = pygame.image.load(bg_img_path).convert_alpha()

# image for mouse follow
sunflowerImg = pygame.image.load('material/images/SunFlower_00.png').convert_alpha()
wallnutImg = pygame.image.load('material/images/WallNut_00.png').convert_alpha()
peashooterImg = pygame.image.load('material/images/Peashooter_00.png').convert_alpha()

# seed bar
sunbankImg = pygame.image.load('material/images/SeedBank.png').convert_alpha()
flower_seed = pygame.image.load("material/images/TwinSunflower.gif")
wallnut_seed = pygame.image.load("material/images/WallNut.gif")
peashooter_seed = pygame.image.load("material/images/Peashooter.gif")

# begining with 1000 sun assets
text = '1000'
sun_font = pygame.font.SysFont('arial', 20)
sun_num_surface = sun_font.render(text, True, (0,0,0))

# create spriteGroup
peashooterGroup = pygame.sprite.Group()
sunflowerGroup = pygame.sprite.Group()
wallnutGroup = pygame.sprite.Group()
bulletGroup = pygame.sprite.Group()
plantGroup = pygame.sprite.Group()  # contain all plant
zombieGroup = pygame.sprite.Group()
sunList = pygame.sprite.Group()

clock = pygame.time.Clock()


GEN_SUN_EVENT = pygame.USEREVENT + 1  # event_id
pygame.time.set_timer(GEN_SUN_EVENT, 3000)

GEN_BULLET_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(GEN_BULLET_EVENT, 2000)

GEN_ZOMBIE_EVENT = pygame.USEREVENT + 3
pygame.time.set_timer(GEN_ZOMBIE_EVENT, 6000)

GEN_FLAGZOMBIE_EVENT = pygame.USEREVENT + 4
pygame.time.set_timer(GEN_FLAGZOMBIE_EVENT, 8000)

def mian():
    global text
    global sun_font
    global sun_num_surface
    running = True
    index = 0
    choose = 0  # choose which seed to plant
    while running:
        # if index >= 120:
        #     index = 0
        clock.tick(FPS)
        # play backgroud music
        # if not pygame.mixer.music.get_busy():
        #     pygame.mixer.music.play()

        # plot backgroud
        screen.blit(bg_img_obj, (0,0))
        # plot sunbank and nums
        screen.blit(sunbankImg, (250,0))
        screen.blit(sun_num_surface, (265,60))
        # plot seed bar
        screen.blit(flower_seed, (330,10))
        screen.blit(wallnut_seed, (380,10))
        screen.blit(peashooter_seed, (430,10))

        # update plant
        plantGroup.update(index)
        plantGroup.draw(screen)
        # plot bullet
        bulletGroup.update(index)
        bulletGroup.draw(screen)
        # plot zombie
        zombieGroup.update(index)
        zombieGroup.draw(screen)
        # plot sun
        sunList.update(index)
        sunList.draw(screen)

        # detect collide ( collide_rect_ratio(0.5) --> same line collide )
        for bullet in bulletGroup:
            for zombie in zombieGroup:
                if pygame.sprite.collide_rect_ratio(0.5)(bullet, zombie):
                    zombie.energy -= 1
                    bulletGroup.remove(bullet)
        for wallnut in wallnutGroup:
            for zombie in zombieGroup:
                if pygame.sprite.collide_rect_ratio(0.5)(wallnut, zombie):
                    zombie.isMeetPlant = True
                    wallnut.zombies.add(zombie)
        for peashooter in peashooterGroup:
            for zombie in zombieGroup:
                if pygame.sprite.collide_rect_ratio(0.5)(peashooter, zombie):
                    zombie.isMeetPlant = True
                    peashooter.zombies.add(zombie)
        for sunflower in sunflowerGroup:
            for zombie in zombieGroup:
                if pygame.sprite.collide_rect_ratio(0.5)(sunflower, zombie):
                    zombie.isMeetPlant = True
                    sunflower.zombies.add(zombie)

        # plot seed follow mouse drive
        (x, y) = pygame.mouse.get_pos()
        if choose == 1:
            screen.blit(sunflowerImg, (x - sunflowerImg.get_rect().width // 2,
                                       y - sunflowerImg.get_rect().height // 2))
        elif choose == 2:
            screen.blit(wallnutImg, (x - wallnutImg.get_rect().width // 2,
                                     y - wallnutImg.get_rect().height // 2))
        elif choose == 3:
            screen.blit(peashooterImg, (x - peashooterImg.get_rect().width // 2,
                                        y - peashooterImg.get_rect().height // 2))

        # listen for event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # generate sun event
            if event.type == GEN_SUN_EVENT:
                for sprite in sunflowerGroup:
                    now = time.time()
                    if now - sprite.last_time >= 3:
                        sun = Sun(sprite.rect)
                        sunList.add(sun)
                        sprite.last_time = now
            # generate bullet event
            if event.type == GEN_BULLET_EVENT:
                for sprite in peashooterGroup:
                    now = time.time()
                    if now - sprite.last_time >= 2:
                        bullet = Bullet(sprite.rect, window_size)
                        bulletGroup.add(bullet)
                        sprite.last_time = now
            # generate zombie event
            if event.type == GEN_ZOMBIE_EVENT:
                zombie = Zombie()
                zombieGroup.add(zombie)
            # generate flagzombie event
            if event.type == GEN_FLAGZOMBIE_EVENT:
                flagzombie = FlagZombie()
                zombieGroup.add(flagzombie)

            # plant seed event
            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed_key = pygame.mouse.get_pressed() # tuple (1,0,0) = (left, mid, right)
                # right bottom --> cancel
                if pressed_key[2] and choose != 0:
                    choose = 0
                # left bottom --> select
                if pressed_key[0] == 1:
                    pos = pygame.mouse.get_pos()
                    (x, y) = pos
                    if 330 <= x <= 380 and 10 <= y <= 80 and int(text) >= 50:
                        # print('点中了太阳花卡片')
                        choose = 1  # sunflower
                    elif 380 < x <= 430 and 10 <= y <= 80 and int(text) >= 50:
                        # print('点中了坚果卡片')
                        choose = 2  # wallnut
                    elif 430 < x <= 480 and 10 <= y <= 80 and int(text) >= 100:
                        # print('点中了豌豆射手卡片')
                        choose = 3  # peashooter
                    elif 250 < x < 1200 and 70 < y < 600:
                        # plant seed, not allow stack
                        if choose == 1:
                            current_time = time.time()
                            trueX = x // 100 * 100
                            trueY = y // 125 * 125
                            print(trueX,trueY)
                            canHold = True
                            for plant in plantGroup:
                                if plant.rect.left-50 <= trueX <= plant.rect.left + 50 \
                                        and plant.rect.top-50 <= trueY <= plant.rect.top + 50:
                                    canHold = False
                                    break
                            if not canHold or trueY < 100:
                                break

                            if canHold:
                                sunflower = Sunflower(current_time)
                                sunflower.rect.top = y
                                sunflower.rect.left = x
                                sunflowerGroup.add(sunflower)
                                plantGroup.add(sunflower)
                                choose = 0
                                # deduct seed value
                                text = int(text) - 150
                                sun_num_surface = sun_font.render(str(text), True, (0,0,0))
                        elif choose == 2:
                            trueX = x // 100 * 100
                            trueY = y // 125 * 125
                            canHold = True
                            for plant in plantGroup:
                                if plant.rect.left - 50 <= trueX <= plant.rect.left + 50 \
                                        and plant.rect.top - 50 <= trueY <= plant.rect.top + 50:
                                    canHold = False
                                    break
                            if not canHold or trueY < 100:
                                break

                            if canHold:
                                wallnut = Wallnut()
                                wallnut.rect.top = y
                                wallnut.rect.left = x
                                wallnutGroup.add(wallnut)
                                plantGroup.add(wallnut)
                                choose = 0
                                # deduct seed value
                                text = int(text) -50
                                sun_num_surface = sun_font.render(str(text), True, (0, 0, 0))
                        elif choose == 3:
                            trueX = x // 100 * 100
                            trueY = y // 125 * 125
                            canHold = True
                            for plant in plantGroup:
                                if plant.rect.left - 50 <= trueX <= plant.rect.left + 50 \
                                        and plant.rect.top - 50 <= trueY <= plant.rect.top + 50:
                                    canHold = False
                                    break
                            if not canHold or trueY < 100:
                                break

                            if canHold:
                                current_time = time.time()
                                peashooter = Peashooter(current_time)
                                peashooter.rect.top = y
                                peashooter.rect.left = x
                                peashooterGroup.add(peashooter)
                                plantGroup.add(peashooter)
                                choose = 0
                                # deduct seed value
                                text = int(text) - 100
                                sun_num_surface = sun_font.render(str(text), True, (0, 0, 0))
                        pass
                    else:
                        pass
                    for sun in sunList:
                        if sun.rect.collidepoint(pos):
                            sunList.remove(sun)
                            text = str(int(text)+50)
                            sun_num_surface = sun_font.render(text, True, (0,0,0))

        index += 1
        pygame.display.update()


if __name__ == '__main__':
    mian()