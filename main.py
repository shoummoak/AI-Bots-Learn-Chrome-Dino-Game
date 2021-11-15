# imports
import pygame as pg
import neat
import os

from settings import *
from dino_file import Dino
from obstacles import Obstacle


def max_current_fitness(genomes_local):

    print("highest fitness: {}".format((lambda genomes: max([genome.fitness for genome in genomes]) if genomes != [] else None)(genomes_local)))

def stop_running(dinos):

    if len(dinos) == 0:
        return True

def scroll_background(bg1, bg1_left, bg2, bg2_left):

    screen.blit(bg1, (bg1_left, screen_height*0.85))
    screen.blit(bg2, (bg2_left, screen_height*0.85))


# award fitness for still staying in the run
def award_fitness(genomes_local, prev_obstacles_crossed, obstacles_crossed):

    # print("prev, new: {}, {}".format(prev_obstacles_crossed, obstacles_crossed))

    award_more = False
    if obstacles_crossed > prev_obstacles_crossed:
        prev_obstacles_crossed = obstacles_crossed
        award_more = True

    # award fitness for still staying in the run
    for genome in genomes_local:
        genome.fitness += 0.03
        if award_more:
            genome.fitness += 3
            # print("awarded more")

    # return updated value to update the main var in the run_game() function
    return prev_obstacles_crossed


# this is one ugly function
def dino_action(dinos, genomes_local, neural_nets, Obs):

    for index, dino in enumerate(dinos):

        # print("len, obs1, obs2: {} {} {}".format(len(Obs.obstacles), Obs.obstacle1, Obs.obstacle2))

        size = len(Obs.obstacles)

        # if obstacles list is empty, do nothing and wait for it to get filled by the Obs object
        if size == 0:
            return None

        # since there is only 1 obs in the list, position x=600 is virtually treated as obs2
        elif size == 1:

            input_data = (dino.hitbox_rect.y, Obs.obstacles[0].rect.left - dino_right_x,
                          Obs.obstacles[0].rect.y, Obs.obstacles[0].rect.width,
                          Obs.obstacles[0].rect.height,
                          600 - Obs.obstacles[0].rect.right,
                          Obs.move_v)

        # since for a few frames obs1 and obs2 become 1 & 2 respectively, 
        # this raises 'out of range' exception. Therefore, hard coded 0 & 1 
        # indices so that main game logic is not followed
        elif size == 2:

            input_data = (dino.hitbox_rect.y, Obs.obstacles[0].rect.left - dino_right_x,
                          Obs.obstacles[0].rect.y, Obs.obstacles[0].rect.width,
                          Obs.obstacles[0].rect.height,
                          Obs.obstacles[1].rect.left - Obs.obstacles[0].rect.right,
                          Obs.move_v)

        else:
            # gather the input data information
            # input_data --> (dino y position, distance to obs1, obs1 y position, width of obs1, 
            #                 height of obs1, distance between obs1 and obs2, obs movement speed)
            # kinda messy, I know. Can't be helped.
            input_data = (dino.hitbox_rect.y, Obs.obstacles[Obs.obstacle1].rect.left - dino_right_x,
                          Obs.obstacles[Obs.obstacle1].rect.y, Obs.obstacles[Obs.obstacle1].rect.width,
                          Obs.obstacles[Obs.obstacle1].rect.height,
                          Obs.obstacles[Obs.obstacle2].rect.left - Obs.obstacles[Obs.obstacle1].rect.right,
                          Obs.move_v)

        # output is a list/tuple of 3 values
        output = neural_nets[index].activate(input_data)
        # pick the highest value among the 3
        activated_index = output.index(max(output))

        if activated_index > 0.8:

            if activated_index == 0:
                if dino.ducked is True:
                    dino.ducked = False
                dino.big_jump()

            elif activated_index == 1:
                if dino.ducked is True:
                    dino.ducked = False
                dino.small_jump()

            else:
                dino.ducked = True
                dino.duck()


# collision works under the premise that Dino can only collide with the obstacles at index 0 and 1
def check_collision(dinos, genomes_local, neural_nets, obstacles, dino_sprites):

    # if at least 2 obstacles are still alive in the list
    if len(obstacles) >= 2:
        obj1 = obstacles[0]
        obj2 = obstacles[1]
        for index, dino in enumerate(dinos):
            if dino.hitbox_rect.colliderect(obj1.rect) or dino.hitbox_rect.colliderect(obj2.rect):
                dinos.remove(dino)
                dino_sprites.remove(dino)
                del(genomes_local[index])
                del(neural_nets[index])
                # print("colliding at left:{} and right:{}".format(obj.rect.left, obj.rect.right))

    # if there is only 1 obstacle alive in the list
    elif len(obstacles) == 1:
        obj1 = obstacles[0]
        for index, dino in enumerate(dinos):
            if dino.hitbox_rect.colliderect(obj1.rect):
                dinos.remove(dino)
                dino_sprites.remove(dino)
                del(genomes_local[index])
                del(neural_nets[index])

    # if the obstacles list is empty, nothing happens. This function is structures this way in order
    # to bypass 'list index out of range errors'

def run_game(genomes, config):

    # intitalize background
    bg1 = pg.image.load(os.path.join("images", "ground.png")).convert()
    bg2 = bg1.copy()
    bg_width = bg1.get_width()
    bg1_left = 0
    bg2_left = bg_width
    bg_speed = 10
    # background initialized

    """
    : set the initial fitness of every genome to 0
    : create a local_genome (referencing the genomes of list genomes) container
       to modify genome fitness
    : according to each genome, create the respective neural network
    NOTE:the number of genomes, pop_size has been specified in the config text file
    """
    genomes_local = []
    neural_nets = []
    dinos = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        genomes_local.append(genome)
        neural_nets.append(neat.nn.FeedForwardNetwork.create(genome, config))
        dinos.append(Dino())


    # create sprite group dino_sprites and add all the Dino bots seperately to the group
    dino_sprites = pg.sprite.Group()
    for dino in dinos:
        dino_sprites.add(dino)

    # generate sprite group obstacle_sprites and add Obstacle obj
    # note the Obstacle obj holds a list of individual obstacles.
    # It is not a single obstacle itself
    obstacle_sprites = pg.sprite.Group()
    Obs = Obstacle()
    # obstacles attribute of Obstacle is the list of objects belonging to [SmalCactus, Bird, BigCactus etc.]
    obstacles = Obs.obstacles
    # we add this list to the sprite group obstacle_sprites
    obstacle_sprites.add(obstacles)

    # this counter is used to award fitness to Dinos when they have corssed an obstacle
    # this var will always have the same value as Obs.obstacles_crossed BUT when
    # Obs.obstacles_crossed increments itself, the difference of 1 with this var allows
    # us to confirm a new obstacle has been crossed, and fitness awarded appropriately
    prev_obstacles_crossed = 0
    running = True

    while running:

        for event in pg.event.get():

            if event.type == pg.QUIT:
                running = False
                pg.quit()
                quit()


        screen.fill(white)

        # BACKGROUND SCROLLING LOGIC BL0CK
        bg1_left -= bg_speed
        bg2_left -= bg_speed
        if bg1_left <= -1 * bg_width:
            bg1_left = bg2_left + bg_width
        if bg2_left <= -1 * bg_width:
            bg2_left = bg1_left + bg_width
        scroll_background(bg1, bg1_left, bg2, bg2_left)

        if stop_running(dinos):
            running = False

        # draw sprites
        dino_sprites.draw(screen)
        obstacle_sprites.draw(screen)

        # update Obstacle sprites
        Obs.update(obstacle_sprites, screen)

        # print()
        max_current_fitness(genomes_local)
        dino_action(dinos, genomes_local, neural_nets, Obs)
        check_collision(dinos, genomes_local, neural_nets, obstacles, dino_sprites)
        prev_obstacles_crossed = award_fitness(genomes_local, prev_obstacles_crossed, Obs.obstacles_crossed)

        # update Dino sprites
        dino_sprites.update(obstacles)

        # screen is being updated here once. No need to repeat this anywhere else.
        pg.display.flip()
        clock.tick(fps)


def run(config_file):

    # create the config object with the config-feedforward.txt template
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    # create population object
    p = neat.Population(config)

    # statistical information stdout
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # run up to the i'th generations if the ideal fitness has not been achieved by then
    winner = p.run(run_game, 50)

    # draw neural network of the best genome
    # visualize.draw_net(config, winner, True)


# initialize pygame
pg.init()
clock = pg.time.Clock()

# set up window
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("ML Bot learns to play Chrome's T-rex Run")

# intialize pygame
pg.init()
clock = pg.time.Clock()

# set up simulation window
screen = pg.display.set_mode((screen_width, screen_height))

# prepare the path to the [NEAT] config file
if __name__ == "__main__":
    main_file_dir = os.path.dirname(__file__)
    config_file = os.path.join(main_file_dir, "config-feedforward.txt")
    run(config_file)
