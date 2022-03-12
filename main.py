
from cmath import sin
from genericpath import exists
from hmac import trans_36
from re import I
from tkinter import Y
from turtle import width
from matplotlib.pyplot import draw
from numpy import mat
import pygame
import neat
import os
import random
import math
import pickle
pygame.init()

#---------------------------------------------------------------------------------------------------------------#
TICK = 30
WIN_WIDTH, WIN_HEIGHT = 960, 540
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
COOLDOWN_TIME = 35
#---------------------------------------------------------------------------------------------------------------#

ALLY_AIRCRAFT_IMG = pygame.image.load(
    os.path.join('Assets', 'ALLY_AIR_CRAFT.PNG'))

ALLY_AIRCRAFT = pygame.transform.scale(
    ALLY_AIRCRAFT_IMG, (ALLY_AIRCRAFT_IMG.get_width() * 4, ALLY_AIRCRAFT_IMG.get_height() * 4))

#---------------------------------------------------------------------------------------------------------------#
EDGE_IMG = pygame.image.load(
    os.path.join('Assets', 'EDGE.PNG'))
EDGE = pygame.transform.scale(
    EDGE_IMG, (EDGE_IMG.get_width() * 4, EDGE_IMG.get_height() * 4))

COIN_IMG = pygame.image.load(
    os.path.join('Assets', 'COIN.PNG'))

COIN = pygame.transform.scale(
    COIN_IMG, (COIN_IMG.get_width() * 4, COIN_IMG.get_height() * 4))

ROCK001_IMG = pygame.image.load(
    os.path.join('Assets', 'ROCK_001.PNG'))

ROCK001 = pygame.transform.scale(
    ROCK001_IMG, (ROCK001_IMG.get_width() * 4, ROCK001_IMG.get_height() * 4))

ROCK002_IMG = pygame.image.load(
    os.path.join('Assets', 'ROCK_002.PNG'))

ROCK002 = pygame.transform.scale(
    ROCK002_IMG, (ROCK002_IMG.get_width() * 4, ROCK002_IMG.get_height() * 4))

#---------------------------------------------------------------------------------------------------------------#
FONT = pygame.font.Font('freesansbold.ttf', 20)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

#---------------------------------------------------------------------------------------------------------------#


class Ally_Aircraft():
    player_rangle = 0

    def __init__(self, ):
        self.transform = pygame.Rect(WIN_WIDTH * 1/16,
                                     WIN_HEIGHT/2 - ALLY_AIRCRAFT.get_height()/2,
                                     ALLY_AIRCRAFT.get_width(),
                                     ALLY_AIRCRAFT.get_height())

    def Movement(self, key_pressed):

        if key_pressed[pygame.K_w]:
            print('UP')
            self.transform.y -= 10
        if key_pressed[pygame.K_s]:
            print('DOWN')
            self.transform.y += 10

    def AIMovement(self, output):
        # if(self.transform.y > 0):
        index = ally_aircrafts.index(self)
        if(output[0] <= 0.5):
            self.transform.y -= 7
        else:
            #ge[index].fitness -= 10
            pass
            # if(self.transform.y < (WIN_HEIGHT - ALLY_AIRCRAFT.get_height())):
        if(output[0] >= -0.5):
            self.transform.y += 7
        else:
            #ge[index].fitness -= 10
            pass

        if(output[0] == 0.0):
            # efsh5 omo
            ge[index].fitness -= 10

    def Shoot(self):
        pass

    def Draw(self):
        WIN.blit(ALLY_AIRCRAFT, (self.transform.x, self.transform.y))

    def DebugDraw(self):
        pygame.draw.rect(WIN, BLUE, self.transform, 2)
        # pygame.draw.line(WIN, RED, (self.transform.midright[0], self.transform.midright[1]),
        #                  (self.transform.midright[0] * 3, self.transform.midright[1] + math.sin(180) * 1), 3)
        # pygame.draw.line(WIN, RED, (self.transform.midright[0], self.transform.midright[1]),
        #                  ((self.transform.midright[0] * 3) - 30, self.transform.midright[1] - 100), 3)
        # pygame.draw.line(WIN, RED, (self.transform.midright[0], self.transform.midright[1]),
        #                  ((self.transform.midright[0] * 3) - 30, self.transform.midright[1] + 100), 3)
        # pygame.draw.line(WIN, RED, (self.transform.midright[0], self.transform.midright[1]),
        #                  ((self.transform.midright[0] * 3) - 270, self.transform.midright[1] - 150), 3)
        # pygame.draw.line(WIN, RED, (self.transform.midright[0], self.transform.midright[1]),
        #                  ((self.transform.midright[0] * 3) - 270, self.transform.midright[1] + 150), 3)
        #self.player_rangle += 1
        # print(self.player_rangle)

    def Radar(self, radar_angle):
        length = 0
        x = int(self.transform.center[0])
        y = int(self.transform.center[1])
        try:
            while not WIN.get_at((x, y)) == pygame.Color(34, 32, 52, 255) and length < 150:

                length += 1
                x = int(
                    self.transform.center[0] + math.cos(math.radians(0 + radar_angle)) * length)
                y = int(
                    self.transform.center[1] - math.sin(math.radians(0 + radar_angle)) * length)
        except:
            pass
        pygame.draw.line(WIN, BLUE, self.transform.center, (x, y), 3)
        dist = int(math.sqrt(math.pow(self.transform.center[0] - x, 2)
                             + math.pow(self.transform.center[1] - y, 2)))
        # print(dist)
        # _Inputs.append(radar_angle)
        # _Inputs.append(dist)
        _Inputs.extend([radar_angle, dist])

    def Destroy(self):
        if self.transform.y < 0 + EDGE.get_height():
            index = ally_aircrafts.index(self)
            ally_aircrafts.remove(self)
            ge[index].fitness -= 100
            ge.pop(index)
            nets.pop(index)
        if self.transform.y > (WIN_HEIGHT - ALLY_AIRCRAFT.get_height() - EDGE.get_height()):
            index = ally_aircrafts.index(self)
            ally_aircrafts.remove(self)
            ge[index].fitness -= 100
            ge.pop(index)
            nets.pop(index)

    def DestroyOnContact(self, collider):
        if self.transform.colliderect(collider.transform):
            index = ally_aircrafts.index(self)
            ally_aircrafts.remove(self)
            ge[index].fitness -= 100
            ge.pop(index)
            nets.pop(index)

    def Yay(self, collider, x):
        if self.transform.colliderect(collider.transform):

            for g in ge:
                g.fitness += 50
            game_coins.pop(x)


class WorldUPPER_EDGE():

    def __init__(self):
        self.transform = pygame.Rect(0,
                                     WIN_HEIGHT - EDGE.get_height(),
                                     EDGE.get_width(),
                                     EDGE.get_height())

    def Draw(self):
        WIN.blit(EDGE, (self.transform.x, self.transform.y))


class WorldLOWWER_EDGE():

    def __init__(self):
        self.transform = pygame.Rect(0,
                                     0,
                                     EDGE.get_width(),
                                     EDGE.get_height())

    def Draw(self):
        WIN.blit(EDGE, (self.transform.x, self.transform.y))


class GameEntity():

    def __init__(self, img, xpos, ypos):
        self.transform = pygame.Rect(WIN_WIDTH + xpos,
                                     ypos - img.get_height(),
                                     img.get_width(),
                                     img.get_height())
        self.img = img

    def Move(self, gamespeed):
        self.transform.x -= gamespeed

    def Draw(self):
        WIN.blit(self.img, (self.transform.x, self.transform.y))

    def DebugDraw(self):
        pygame.draw.rect(WIN, RED, self.transform, 2)

    def Destroy(self, objects, x):
        if(self.transform.x < - self.img.get_width()):
            objects.pop(x)

    # def DestroyOnContact(self, collider, x):
    #     if self.transform.colliderect(collider.transform):
    #         ally_aircrafts.pop(x)
    #         ge[x].fitness -= 1
    #         ge.pop(x)
    #         nets.pop(x)


class Coin():

    def __init__(self, img, xpos, ypos):
        self.transform = pygame.Rect(WIN_WIDTH + xpos,
                                     ypos - img.get_height(),
                                     img.get_width(),
                                     img.get_height())
        self.img = img

    def Move(self, gamespeed):
        self.transform.x -= gamespeed

    def Draw(self):
        WIN.blit(self.img, (self.transform.x, self.transform.y))

    def DebugDraw(self):
        pygame.draw.rect(WIN, GREEN, self.transform, 2)

    def Destroy(self, objects):
        if(self.transform.x < - self.img.get_width()):
            game_coins.remove(self)


class Gen():

    gamespeed = 10

    def __init__(self):
        self.gen_cooldown = COOLDOWN_TIME

    def speedup(self):
        self.gamespeed += 1

    def cooldown(self):

        if self.gen_cooldown < 0:
            self.gen_cooldown = COOLDOWN_TIME
        else:
            self.gen_cooldown -= 1

    def run(self):

        self.cooldown()
        # spawn Rocks
        ammount = random.randint(0, 2)
        # print(self.gen_cooldown)

        if self.gen_cooldown == 10:

            for i in range(ammount):
                fcintime = random.randint(0, 10)

                if fcintime >= 7:
                    rocks.append(GameEntity(ROCK001,
                                            random.randint(10, 50), random.randint(40, 240)))
                    rocks.append(GameEntity(ROCK001,
                                            random.randint(10, 50), random.randint(720, 860)))
                else:
                    rocks.append(GameEntity(ROCK001,
                                            random.randint(10, 50), random.randint(240, 720)))
                # if type == 2:
                #     rocks.append(GameEntity(ROCK001,
                #                             random.randint(10, 200), WIN_HEIGHT/2))

            spawnCoin = random.randint(0, 10)
            if spawnCoin < 3:
                game_coins.append(Coin(COIN, random.randint(
                    10, 200), random.randint(20, 860)))

        if len(rocks) != 0:
            for x, rock in enumerate(rocks):
                rock.Destroy(rocks, x)
                rock.Move(self.gamespeed)
                rock.Draw()
                rock.DebugDraw()
        if len(game_coins) != 0:
            for x, coin in enumerate(game_coins):
                if coin in game_coins:
                    coin.Destroy(coin)
                    coin.Move(self.gamespeed)
                    coin.Draw()
                    coin.DebugDraw()


def main(genomes, config):
    global ally_aircrafts, ge, nets, rocks, game_coins, _Inputs, radsValue

    ally_aircrafts = []
    ge = []
    nets = []
    rocks = []
    game_coins = []
    _Inputs = []

    radsValue = []
    gen = Gen()
    clock = pygame.time.Clock()
    wle = WorldLOWWER_EDGE()
    wue = WorldUPPER_EDGE()
    for genome_id, genome in genomes:
        genome.fitness = 0
        ally_aircrafts.append(Ally_Aircraft())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
    while True:
        clock.tick(TICK)
        WIN.fill((255, 255, 255))

        wle.Draw()
        wue.Draw()

        gen.cooldown()
        gen.run()
        if len(ally_aircrafts) == 0:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        for i, aircraft in enumerate(ally_aircrafts):
            aircraft.Draw()
            aircraft.DebugDraw()
            _Inputs = [aircraft.transform.y]
            for radar_angle in (-90, -20, 0, 20, 90):
                aircraft.Radar(radar_angle)

            ge[i].fitness += 3
            #print(str([i]) + str(ge[i].fitness))

            # for rock in rocks[:3]:
            #     _Inputs.extend([rock.transform.x, rock.transform.y])
            # if len(rocks) < 3:
            #     for i in range(3-len(rocks)):
            #         _Inputs.extend([1000, 540])

            if len(game_coins) < 1:
                _Inputs.extend([1000, 540])
            else:
                _Inputs.extend([game_coins[0].transform.x,
                               game_coins[0].transform.y])

            output = nets[ally_aircrafts.index(aircraft)].activate(
                (_Inputs))

            if aircraft in ally_aircrafts:
                aircraft.AIMovement(output)
            for rock in rocks:
                if aircraft in ally_aircrafts:
                    aircraft.DestroyOnContact(rock)
            for coin in game_coins:
                if aircraft in ally_aircrafts:
                    aircraft.Yay(coin, game_coins.index(coin))
            if aircraft in ally_aircrafts:
                aircraft.Destroy()

        text_1 = FONT.render(
            f'Aircrafts Alive:  {str(len(ally_aircrafts))}', True, (0, 0, 0))
        WIN.blit(text_1, (50, 50))
        pygame.display.update()


def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(main, 2**64)
    with open("winner.pkl", "wb") as f:
        pickle.dump(winner, f)
        f.close()
    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
