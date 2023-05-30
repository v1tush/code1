import pygame as pg
import sys
from random import randint

WIN_WIDTH = 540
WIN_HEIGHT = 960
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
BLUE = (64, 224, 208)
GREEN = (0, 128, 0)
GRAY = (119, 136, 153)
RED = (255, 0, 0)
FPS = 60
MIN_SPEED = 1
MAX_SPEED = 10
MAX_FISHES = 25


class Shark():
    width_shark = 50
    height_shark = 50

    def __init__(self, surface, color, speed=6):
        self.surf = surface
        self.color = color
        self.speed = speed
        self.x = 0
        self.y = surface.get_height() // 2
        self.rect = pg.Rect(self.x, self.y, Shark.width_shark, Shark.height_shark)

    def draw(self):
        pg.draw.rect(self.surf, self.color, self.rect)

    def jump(self, direction):
        if direction == 'up':
            if self.rect.y > 0:
                self.rect.y -= Shark.height_shark
        if direction == 'right':
            self.rect.x += Shark.width_shark
        if direction == 'down':
            if self.rect.y + Shark.height_shark < WIN_HEIGHT:
                self.rect.y += Shark.height_shark
        if direction == 'left':
            if self.rect.x > 0:
                self.rect.x -= Shark.width_shark


class Fishes():
    width_fish = randint(0, 250)
    height_fish = randint(0, 100)

    def __init__(self, surface, color, speed=3, x=None, y=None, up=True):
        self.surf = surface
        self.color = color
        self.speed = speed
        self.up = up
        self.rect = pg.Rect(x, y, Car.width_car, Car.height_car)
#         if x is None:
#             self.x = self.surf.get_width() // 2 - Car.width_car // 2
#         else:
#             self.x = x
#         if y is None:
#             self.y = self.surf.get_height()
#         else:
#             self.y = y

    def drive(self):
        pg.draw.rect(self.surf, self.color, self.rect)
        if self.up:
            self.rect.move_ip(0, -self.speed)
            if self.rect.y < -Car.height_car:
                self.rect.y = self.surf.get_height()
                self.rect.x = randint(Guy.width_guy, self.surf.get_width())
        else:
            self.rect.move_ip(0, self.speed)
            if self.rect.y > self.surf.get_height():
                self.rect.y = -Car.height_car
                self.rect.x = randint(0, self.surf.get_width())


sc = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

clock = pg.time.Clock()

surf_left = pg.Surface((WIN_WIDTH // 2, WIN_HEIGHT))
surf_left.fill(WHITE)
surf_left_rect = surf_left.get_rect()

surf_right = pg.Surface((WIN_WIDTH // 2, WIN_HEIGHT))
surf_right.fill(BLACK)
surf_right_rect = surf_right.get_rect(topleft=(WIN_WIDTH // 2, 0))
# Тротуар
pg.draw.rect(surf_left, BLUE, (0, 0, Guy.width_guy, WIN_HEIGHT))

guy1 = Guy(surf_left, GREEN)
guy1.draw()

sc.blit(surf_left, (0, 0))
sc.blit(surf_right, (WIN_WIDTH // 2, 0))

list_of_cars = []

active_left = False
active_right = False

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.pos[0] < WIN_WIDTH // 2:
                active_left = True
                active_right = False
            else:
                active_left = False
                active_right = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                list_of_cars = []
            if event.key == pg.K_SPACE:
                active_left = True
                active_right = True
            if event.key == pg.K_UP:
                guy1.jump('up')
            if event.key == pg.K_DOWN:
                guy1.jump('down')
            if event.key == pg.K_RIGHT:
                guy1.jump('right')
            if event.key == pg.K_LEFT:
                guy1.jump('left')
            if event.key == pg.K_1 and len(list_of_cars) < MAX_CARS:
                new_speed = randint(MIN_SPEED, MAX_SPEED)
                new_x = randint(Guy.width_guy, surf_left.get_width())
                new_y = surf_left.get_height()
                new_car = Car(surf_left, BLACK, speed=new_speed,
                              x=new_x, y=new_y, up=True)
                list_of_cars.append(new_car)

            if event.key == pg.K_2 and len(list_of_cars) < MAX_CARS:
                new_speed = randint(MIN_SPEED, MAX_SPEED)
                new_x = randint(0, surf_right.get_width())
                new_y = surf_right.get_height()
                new_car = Car(surf_right, WHITE, speed=new_speed,
                              x=new_x, y=new_y, up=False)
                list_of_cars.append(new_car)
    if active_left:
        surf_left.fill(WHITE)
        pg.draw.rect(surf_left, BLUE, (0, 0, Guy.width_guy, WIN_HEIGHT))
        for car in list_of_cars:
            if car.surf == surf_left:
                car.drive()
        guy1.draw()
        sc.blit(surf_left, (0, 0))
    if active_right:
        surf_right.fill(BLACK)
        for car in list_of_cars:
            if car.surf == surf_right:
                car.drive()
        guy1.draw()
        sc.blit(surf_right, (WIN_WIDTH // 2, 0))
    for car in list_of_cars:
        if guy1.surf == car.surf:
            if car.rect.colliderect(guy1.rect):
                guy1.rect.x = 0
                guy1.rect.y = guy1.surf.get_height() // 2
    if guy1.rect.left >= WIN_WIDTH // 2:
        guy1.surf = surf_right
        guy1.rect.x = 0

    pg.display.update()
    clock.tick(FPS)
