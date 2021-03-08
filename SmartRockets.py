import pygame
import math
import sys
import random
import time
random.seed(time.perf_counter())
sys.path.append("C:\\users\\alexa\\Documents\\Github\\QFunctions")
from Q_Functions import Q_Vector2D
from rocket import Rocket

PI = math.pi
TWO_PI = 2.0 * math.pi

# define constants
WIDTH = 700
HEIGHT = 500
FPS = 60

ROCKET_WIDTH = 10
ROCKET_LENGTH = 30
DNA_LENGTH = 100

# define colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)


def main():

    rockets = []
    # DNA = [Q_Vector2D.random() for _ in range(DNA_LENGTH)]
    DNA = [Q_Vector2D(4, 0.02) for _ in range(DNA_LENGTH)]
    print(DNA)
    rocket = Rocket(x=WIDTH / 2, y=HEIGHT / 2, dna=DNA)
    # force = Q_Vector2D(angle=0, magnitude=0.1)
    # rocket.apply_force(force)
    rockets.append(rocket)

    # initialize pygame and create screen
    pygame.init()
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    # for setting FPS
    CLOCK = pygame.time.Clock()

    # define a surface (RECTANGLE)
    ROCKET_TEMPLATE = pygame.Surface((ROCKET_LENGTH, ROCKET_WIDTH))
    # for making transparent background while rotating an image
    ROCKET_TEMPLATE.set_colorkey(BLACK)
    # fill the rectangle / surface with green color
    ROCKET_TEMPLATE.fill(WHITE)

    # keep rotating the rectangle until running is set to False
    running = True

    while running:
        # set FPS
        CLOCK.tick(FPS)

        # clear the screen every time before drawing new objects
        SCREEN.fill(BLACK)

        # check for the exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for rocket in rockets:
            rocket.apply_force()
            rocket.update()

            if rocket.x < 0:
                rocket.x = 0
                rocket.stop()
            if rocket.y < 0:
                rocket.y = 0
                rocket.stop()
            if rocket.x > WIDTH:
                rocket.x = WIDTH
                rocket.stop()
            if rocket.y > HEIGHT:
                rocket.y = HEIGHT
                rocket.stop()

            # rotating the orignal image
            rotated_rocket = pygame.transform.rotate(ROCKET_TEMPLATE, -rocket.angle_in_degrees)
            rect = rotated_rocket.get_rect()

            # set the rotated rectangle to the old center
            rect.center = (rocket.x, rocket.y)
            # print((rocket.x, rocket.y))

            # drawing the rotated rectangle to the screen
            SCREEN.blit(rotated_rocket, rect)

        # flipping the display after drawing everything
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
