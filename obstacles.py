import pygame as pg
import random as rd
import time

from settings import *


class Obstacle():

    def __init__(self):

        # number of obstacles that have completely left the screen
        # used to update the move_v and to specify the set of obstacles to be generated
        self.obstacles_crossed = 0

        # these two indices point to the 1st and 2nd incoming obstacles respectively in the obstacles list
        # 0 and 1 as initially the obstacles at indices 0 and 1 will be the first 2 obstacles Dino will face
        self.obstacle1 = 0
        self.obstacle2 = 1

        # movement speed at which the obstacles travel
        # the longer the game played, the higher it is. Initial value at 5.
        self.move_v = 5

        # create the list of objects in the run
        # the list will be filled by the add_obstacles() function
        self.obstacles = []

        # 1st obstacle's x-coordinate
        self.x_offset = 1000


    # master function containing all Obstacle game logic
    def update(self, obstacle_sprites, screen):

        self.add_obstacles(obstacle_sprites, screen)
        self.move()
        self.update_indices()
        self.remove_obstacles()
        self.update_speed()
        # self.debug_obs1_2(screen)
        # self.print()


    # add more obstacles after 15 obstacles have crossed the game screen i.e. len(obstacles) = 0
    # this keep happening forever
    def add_obstacles(self, obstacle_sprites, screen):

        if len(self.obstacles) == 0:

            # remove the empty obstacles list
            obstacle_sprites.remove(self.obstacles)
            self.x_offset = 600
            self.generate_obstacles()

        # simply add the newly created list of obstacles as before
        obstacle_sprites.add(self.obstacles)


    # generate a specific set of obstacles based on obstacles_crossed count
    def generate_obstacles(self):

        if self.obstacles_crossed < 30:
            for i in range(15):
                self.obstacles.append(Bird(self.x_offset))
                self.x_offset += rd.randint(obstacle_spacing1[0], obstacle_spacing1[1])

        else:
            for i in range(15):
                self.obstacles.append(rd.choice([SmallCactus(self.x_offset), SmallCactus2x(self.x_offset), SmallCactus3x(self.x_offset), BigCactus(self.x_offset), BigCactus2x(self.x_offset), BigCactus3x(self.x_offset), Bird(self.x_offset)]))
                self.x_offset += rd.randint(obstacle_spacing1[0], obstacle_spacing1[1])

        # if self.obstacles_crossed < 15:
        #     for i in range(15):
        #         self.obstacles.append(rd.choice([SmallCactus(self.x_offset), SmallCactus2x(self.x_offset), SmallCactus3x(self.x_offset), BigCactus(self.x_offset)]))
        #         self.x_offset += rd.randint(obstacle_spacing1[0], obstacle_spacing1[1])
        #
        # elif self.obstacles_crossed >= 15:
        #     for i in range(15):
        #         self.obstacles.append(rd.choice([SmallCactus(self.x_offset), SmallCactus2x(self.x_offset), SmallCactus3x(self.x_offset), BigCactus(self.x_offset), BigCactus2x(self.x_offset), BigCactus3x(self.x_offset), Bird(self.x_offset)]))
        #         self.x_offset += rd.randint(obstacle_spacing1[0], obstacle_spacing1[1])
        #
        # # elif self.obstacles_crossed >= 60 and self.obstacles_crossed < 75:
        #     for i in range(15):
        #         self.obstacles.append(rd.choice([SmallCactus(self.x_offset), SmallCactus2x(self.x_offset), SmallCactus3x(self.x_offset), BigCactus(self.x_offset), BigCactus2x(self.x_offset), BigCactus3x(self.x_offset), Bird(self.x_offset)]))
        #         self.x_offset += rd.randint(obstacle_spacing2[0], obstacle_spacing2[1])
        #
        # elif self.obstacles_crossed >= 75:
        #     for i in range(15):
        #         self.obstacles.append(rd.choice([SmallCactus(self.x_offset), SmallCactus2x(self.x_offset), SmallCactus3x(self.x_offset), BigCactus(self.x_offset), BigCactus2x(self.x_offset), BigCactus3x(self.x_offset), Bird(self.x_offset)]))
        #         self.x_offset += rd.randint(obstacle_spacing3[0], obstacle_spacing3[1])


    def move(self):

        for obstacle in self.obstacles:
            obstacle.rect.x -= self.move_v


    # remove obstacles that have left the screen
    # furthermore, update obs1 and obs2 from 1 and 2 back to 0 and 1
    def remove_obstacles(self):

        if self.obstacles[0].rect.right < 0:
            self.obstacles_crossed += 1
            del(self.obstacles[0])

            self.obstacle1 = 0
            self.obstacle2 = 1


    # update obs1 and obs2 from 0 and 1 to 1 and 2 repectively when the obstacle at index 0 is between Dino
    # and the left wall of the screen. Insures absolute accuracy of the positions of the first 2 obstacles
    def update_indices(self):

        if self.obstacles[0].rect.right < 35:
            self.obstacle1 = 1
            self.obstacle2 = 2


    # set speed based on the number of obstacles crossed
    def update_speed(self):

        if self.obstacles_crossed in obstacle_speeds:
            self.move_v = obstacle_speeds[self.obstacles_crossed]


    def print(self):

        print("obstacles crossed: ", self.obstacles_crossed)
        print("speed: ", self.move_v)
        # print(self.obstacles[0].rect.x)

    def debug_obs1_2(self, screen):

        pg.draw.rect(screen, red, self.obstacles[self.obstacle1].rect)
        pg.draw.rect(screen, red, self.obstacles[self.obstacle2].rect)


# Unique Obstacle classes. A class for each obstacle type
class SmallCactus(pg.sprite.Sprite):

    def __init__(self, position):

        # calling super with self as param
        pg.sprite.Sprite.__init__(self)
        # pick a random small_cactus among the 2 in images
        self.image = rd.choice([sc1, sc2])
        self.rect = self.image.get_rect()
        self.rect.x = position
        self.rect.bottom = ground_level


class SmallCactus2x(pg.sprite.Sprite):

    def __init__(self, position):

        # calling super with self as param
        pg.sprite.Sprite.__init__(self)
        # pick a random small_cactus among the 2 in images
        self.image = sc2x
        self.rect = self.image.get_rect()
        self.rect.x = position
        self.rect.bottom = ground_level


class SmallCactus3x(pg.sprite.Sprite):

    def __init__(self, position):

        # calling super with self as param
        pg.sprite.Sprite.__init__(self)
        # pick a random small_cactus among the 2 in images
        self.image = sc3x
        self.rect = self.image.get_rect()
        self.rect.x = position
        self.rect.bottom = ground_level
        # self.hitbox = (self.rect.x, self.rect.y, 72, 46)
        # self.hitbox_rect = pg.Rect(self.hitbox)


class BigCactus(pg.sprite.Sprite):

    def __init__(self, position):

        # calling super with self as param
        pg.sprite.Sprite.__init__(self)
        # pick a random big_cactus among the 3 in images
        self.image = rd.choice([bc1, bc2, bc3])
        self.rect = self.image.get_rect()
        self.rect.x = position
        self.rect.bottom = ground_level


class BigCactus2x(pg.sprite.Sprite):

    def __init__(self, position):

        # calling super with self as param
        pg.sprite.Sprite.__init__(self)
        # pick a random small_cactus among the 2 in images
        self.image = bc2x
        self.rect = self.image.get_rect()
        self.rect.x = position
        self.rect.bottom = ground_level


class BigCactus3x(pg.sprite.Sprite):

    def __init__(self, position):

        # calling super with self as param
        pg.sprite.Sprite.__init__(self)
        # pick a random small_cactus among the 2 in images
        self.image = bc3x
        self.rect = self.image.get_rect()
        self.rect.x = position
        self.rect.bottom = ground_level


class Bird(pg.sprite.Sprite):

    def __init__(self, position):
        # calling super with self as param
        pg.sprite.Sprite.__init__(self)
        self.time = time.time()
        # load the bird/terrordactyl image
        self.image = bird2
        self.rect = self.image.get_rect()
        self.rect.x = position

        # note there are three y positions of Bird --> HIGH, MED, LOW
        self.rect.bottom = rd.choice([ground_level - 10, ground_level - 30, ground_level - 55])


    def flap_animation(self):

        if time.time()-self.time >= 0.25:

            self.time = time.time()
            if self.image == bird1:
                self.image = bird2
            else:
                self.image = bird1