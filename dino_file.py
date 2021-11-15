import pygame as pg
import time
from settings import *


class Dino(pg.sprite.Sprite):

    G = .70
    origin = (35, ground_level-42)
    duck_origin = (35, ground_level-26)

    def __init__(self):

        self.time = time.time()
        self.grounded = True
        self.ducked = False

        pg.sprite.Sprite.__init__(self)
        self.image = run1
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = Dino.origin
        # create dino hitbox for custom collision
        self.hitbox = (self.rect.x-1, self.rect.y, 35, 43)
        self.hitbox_rect = pg.Rect(self.hitbox)

        # initialize attribues for gravity mechanics
        self.acc = pg.math.Vector2((0, 0))
        self.vel = pg.math.Vector2((0, 0))
        self.pos = pg.math.Vector2(Dino.origin)


    # master function containing all Dino game logic
    def update(self, obstacles):

        self.movement()
        self.run_animation()
        self.duck_animation()

    def movement(self):

        # acc on the y-axis downwards by G
        self.acc = pg.math.Vector2(0, Dino.G)
        self.vel += self.acc
        self.pos += self.vel + 0.5*self.acc

        # prevent Dino from falling below ground_level
        # and set grounded to True
        if self.pos.y >= Dino.origin[1]:
            self.grounded = True
            self.pos.y = Dino.origin[1]
            self.vel.y = 0

        # update hitbox by making sure hitbox is bound to the rect.x and rect.y of the sprite
        self.rect.x, self.rect.y = self.pos
        self.hitbox = (self.rect.x-1, self.rect.y, 35, 43)
        self.hitbox_rect = pg.Rect(self.hitbox)


    # jump only when the dino is on ground and toggle grounded False as it is in the air
    def big_jump(self):
        if self.grounded:
            self.image = run1
            self.vel.y -= 14
            self.grounded = False


    def small_jump(self):
        if self.grounded:
            self.image = run1
            self.vel.y -= 12
            self.grounded = False


    def duck(self):
        self.vel.y += 8


    # visualize active hit box
    def draw_hitbox(self, screen):
        pg.draw.rect(screen, red, self.hitbox, 1)


    def run_animation(self):

        if self.grounded and not self.ducked:

            if time.time()-self.time >= 0.12:
                if self.image != run1:
                    self.image = run1
                else:
                    self.image = run2
                self.time = time.time()


    def duck_animation(self):

        if self.grounded and self.ducked:
            self.rect.x, self.rect.y = self.duck_origin
            self.hitbox = (self.rect.x, self.rect.y, 55, 25)
            self.hitbox_rect = pg.Rect(self.hitbox)
            if time.time()-self.time >= 0.12:
                if self.image != duck1:
                    self.image = duck1
                else:
                    self.image = duck2
                self.time = time.time()



