import pygame as pg
import sys
from random import randint

WIN_WIDTH = 1300
WIN_HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
BLUE = (64, 224, 208)
GREEN = (0, 128, 0)
GRAY = (119, 136, 153)
RED = (255, 0, 0)
FPS = 60
MIN_SPEED = 5
MAX_SPEED = 10
MAX_CARS = 100
SIDE_DIST = 5
FRONT_DIST = 50


class Guy():
    width_guy = 50
    height_guy = 50

    def __init__(self, surface, color, speed=6):
        self.surf = surface
        self.color = color
        self.speed = speed
        self.x = 0
        self.y = surface.get_height() // 2
        self.rect = pg.Rect(self.x, self.y, Guy.width_guy, Guy.height_guy)

    def draw(self):
        pg.draw.rect(self.surf, self.color, self.rect)

    def jump(self, direction):
        if direction == 'up':
            if self.rect.y > 0:
                self.rect.y -= Guy.height_guy
        if direction == 'right':
            self.rect.x += Guy.width_guy
        if direction == 'down':
            if self.rect.y + Guy.height_guy < WIN_HEIGHT:
                self.rect.y += Guy.height_guy
        if direction == 'left':
            if self.rect.x > 0:
                self.rect.x -= Guy.width_guy


class Car():
    width_car = 50
    height_car = 100
    lane_width = width_car * 2
    lanes = WIN_WIDTH // 2 // lane_width
    def __init__(self, surface, speed=None, lane=None, x=None, y=None, up=True, image=None):
        self.image = image
        self.surf = surface
        self.speed = randint(MIN_SPEED, MAX_SPEED)
        self.up = up
        self.lane = randint(0, Car.lanes)
        x = (self.lane * Car.lane_width + (self.lane + 1) * Car.lane_width) // 2 
        self.rect = pg.Rect(x, y, Car.width_car, Car.height_car)

    def info(self):
        print('lane:', self.lane, 'speed:', self.speed, 'x:', self.rect.x, 'y:', self.rect.y)

    def drive(self):
        # pg.draw.rect(self.surf, self.color, self.rect)
        if self.image is not None:
            self.surf.blit(self.image, self.rect)
        if self.up:
            self.rect.y -= self.speed
            if self.rect.y < -Car.height_car:
                self.rect.y = self.surf.get_height()  # - Car.height_car
                while True:
                    collide_flag = False
                    for i in list_of_cars:
                        if i != self:
                            if pg.Rect.colliderect(i.rect, self.rect):
                                collide_flag = True
                                temp_lane = randint(0, Car.lanes)
                                while temp_lane == self.lane:
                                    temp_lane = randint(0, Car.lanes)
                                self.lane = temp_lane
                                self.rect.x = (self.lane * Car.lane_width + (self.lane + 1) * Car.lane_width) // 2
                    if not collide_flag:
                        break
                self.speed = randint(MIN_SPEED, MAX_SPEED)
            else:
                for i in list_of_cars:
                    if i != self:
                        if abs(i.rect.center[1] - self.rect.center[1]) < Car.height_car + FRONT_DIST:
                            if abs(i.rect.center[0] - self.rect.center[0]) < Car.width_car + SIDE_DIST:
                                self.speed = randint(MIN_SPEED, max(i.speed, MIN_SPEED)) - 2
        elif self.up is False:
            self.rect.y += self.speed
            if self.rect.y > WIN_HEIGHT:
                self.rect.y = -Car.height_car
                while True:
                    collide_flag = False
                    for i in list_of_cars:
                        if i != self:
                            if pg.Rect.colliderect(i.rect, self.rect):
                                collide_flag = True
                                temp_lane = randint(0, Car.lanes)
                                while temp_lane == self.lane:
                                    temp_lane = randint(0, Car.lanes)
                                self.lane = temp_lane
                                self.rect.x = (self.lane * Car.lane_width + (self.lane + 1) * Car.lane_width) // 2
                    if not collide_flag:
                        break
                self.speed = randint(MIN_SPEED, MAX_SPEED)
            else:
                for i in list_of_cars:
                    if i != self:
                        if abs(i.rect.center[1] - self.rect.center[1]) < Car.height_car + FRONT_DIST:
                            if abs(i.rect.center[0] - self.rect.center[0]) < Car.width_car + SIDE_DIST:
                                self.speed = randint(MIN_SPEED, max(i.speed, MIN_SPEED)) - 2


sc = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

clock = pg.time.Clock()
# Дороги
surf_left = pg.Surface((WIN_WIDTH // 2, WIN_HEIGHT))
# surf_left.fill(WHITE)
our_road = pg.image.load('road.gif')
image_surf_left = pg.transform.scale(our_road, (WIN_WIDTH // 2 - Car.width_car, WIN_HEIGHT))
rect_start_zone1 = image_surf_left.get_rect(topleft=(Guy.width_guy, 0))
surf_left_rect = surf_left.get_rect()
surf_left.blit(image_surf_left, rect_start_zone1)

surf_right = pg.Surface((WIN_WIDTH // 2, WIN_HEIGHT))
# surf_right.fill(BLACK)
image_surf_right = pg.transform.scale(our_road, (WIN_WIDTH // 2, WIN_HEIGHT))
rect_start_zone2 = image_surf_right.get_rect(topleft=(0, 0))
surf_right_rect = surf_right.get_rect()
surf_right.blit(image_surf_right, rect_start_zone2)

# Тротуар
image_a = pg.image.load('trotuar_228.png')
image_a = pg.transform.scale(image_a, (Guy.width_guy, WIN_HEIGHT))
rect_start_zone = image_a.get_rect(topleft=(0, 0))
# pg.draw.rect(surf_left, BLUE, rect)
surf_left.blit(image_a, rect_start_zone)

guy1 = Guy(surf_left, GREEN)
guy1.draw()

sc.blit(surf_left, (0, 0))
surf_left.blit(image_surf_left, rect_start_zone1)
sc.blit(surf_right, (WIN_WIDTH // 2, 0))
surf_right.blit(image_surf_right, rect_start_zone2)

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
            if event.key == pg.K_f:
                for i in list_of_cars:
                    i.info()
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
                image = pg.image.load('green_car_3.gif')
                image = pg.transform.scale(image, (Car.width_car, Car.height_car))
                new_speed = randint(MIN_SPEED, MAX_SPEED)
                # new_y = -Car.height_car
                new_y = surf_left.get_height()
                new_car = Car(surf_left, y=new_y, up=True, image=image)
                list_of_cars.append(new_car)

            if event.key == pg.K_2 and len(list_of_cars) < MAX_CARS:
                image = pg.image.load('green_car_2.gif')
                image = pg.transform.scale(image, (Car.width_car, Car.height_car))
                new_speed = randint(MIN_SPEED, MAX_SPEED)
                # new_y = surf_right.get_height()
                new_y = -Car.height_car
                new_car = Car(surf_right, y=new_y, up=False, image=image)
                list_of_cars.append(new_car)
    if active_left:
        # surf_left.fill(WHITE)
        # pg.draw.rect(surf_left, BLUE, (0, 0, Guy.width_guy, WIN_HEIGHT))
        surf_left.blit(image_surf_left, rect_start_zone1)
        surf_left.blit(image_a, rect_start_zone)
        for car in list_of_cars:
            if car.surf == surf_left:
                car.drive()
        guy1.draw()
        sc.blit(surf_left, (0, 0))
    if active_right:
        # surf_right.fill(BLACK)
        surf_right.blit(image_surf_right, rect_start_zone2)
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
