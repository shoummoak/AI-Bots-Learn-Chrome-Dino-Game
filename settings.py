import pygame as pg
import os

# settings

# core settings
fps = 60
screen_width = 600
screen_height = 400

# gameplay settings
ground_level = screen_height*0.89
obstacle_spacing1 = (250, 520)
obstacle_spacing2 = (300, 550)
obstacle_spacing3 = (350, 650)
dino_left_x = 34
dino_right_x = 69

# {key:val}  --> {number of obstacles passed : speed of obstacles}
obstacle_speeds = {0:9}
# obstacle_speeds = {0: 5, 15: 6, 30: 7, 45: 8, 60: 9, 75: 10, 90: 11, 105: 12, 120: 13, 135: 14} original

# colors
white = (255, 255, 255)
blue = (0, 0, 200)
red = (255, 0, 0)

# images
run1 = pg.image.load(os.path.join("images", "run1.png"))
run2 = pg.image.load(os.path.join("images", "run2.png"))
duck1 = pg.image.load(os.path.join("images", "duck1.png"))
duck2 = pg.image.load(os.path.join("images", "duck2.png"))
sc1 = pg.image.load(os.path.join("images", "small_cactus1.png"))
sc2 = pg.image.load(os.path.join("images", "small_cactus2.png"))
bc1 = pg.image.load(os.path.join("images", "big_cactus1.png"))
bc2 = pg.image.load(os.path.join("images", "big_cactus2.png"))
bc3 = pg.image.load(os.path.join("images", "big_cactus3.png"))
sc2x = pg.image.load(os.path.join("images", "small_cactus_2x.png"))
bc2x = pg.image.load(os.path.join("images", "big_cactus_2x.png"))
sc3x = pg.image.load(os.path.join("images", "small_cactus_3x.png"))
bc3x = pg.image.load(os.path.join("images", "big_cactus_3x.png"))
bird1 = pg.image.load(os.path.join("images", "bird1.png"))
bird2 = pg.image.load(os.path.join("images", "bird2.png"))
