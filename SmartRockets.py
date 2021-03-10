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
FPS = 999

ROCKET_WIDTH = 10
ROCKET_LENGTH = 30
DNA_LENGTH = 600
MUTATION_RATE = 0.05
NUM_ROCKETS = 100
TARGET = (WIDTH // 2, int(HEIGHT * 0.1))

# define colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)


def main():

    rockets = []
    obstacles = []
    targets = []
    mating_pool = []
    fitness = []

    obstacle = pygame.Rect(175, 250, 350, 30)
    obstacles.append(obstacle)
    target = pygame.Rect(*TARGET, 20, 20)
    targets.append(target)

    for _ in range(NUM_ROCKETS):
        DNA = [Q_Vector2D.random() for _ in range(DNA_LENGTH)]
        rocket = Rocket(x=WIDTH / 2, y=HEIGHT / 8 * 7, dna=DNA)
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
        NUM_TICKS = 1000

        while running and NUM_TICKS:
            NUM_TICKS -= 1
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

                # if rocket.x < 0:
                #     rocket.x = 0
                #     rocket.stop()
                # if rocket.y < 0:
                #     rocket.y = 0
                #     rocket.stop()
                # if rocket.x > WIDTH:
                #     rocket.x = WIDTH
                #     rocket.stop()
                # if rocket.y > HEIGHT:
                #     rocket.y = HEIGHT
                #     rocket.stop()

                # rotating the orignal image
                rotated_rocket = pygame.transform.rotate(ROCKET_TEMPLATE, -rocket.angle_in_degrees)
                rect = rotated_rocket.get_rect()

                # set the rotated rectangle to the old center
                rect.center = (rocket.x, rocket.y)

                for obstacle in obstacles:
                    if rect.colliderect(obstacle) > 0:
                        rocket.stop()

                for target in targets:
                    if rect.colliderect(target) > 0:
                        rocket.stop()
                        rocket.successful = True

                # drawing the rotated rectangle to the screen
                SCREEN.blit(rotated_rocket, rect)

            for obstacle in obstacles:
                pygame.draw.rect(SCREEN, WHITE, obstacle)

            for target in targets:
                pygame.draw.rect(SCREEN, GREEN, target)

            # flipping the display after drawing everything
            pygame.display.flip()

        fitness.clear()
        for rocket in rockets:
            rocket.calculate_fitness(target=TARGET)
            fitness.append(rocket.fitness)
        max_fitness = max(fitness)
        print(f'Max fitness: {max_fitness}')
        scaler = 1 / max_fitness

        mating_pool.clear()
        for rocket in rockets:
            if rocket.active or rocket.successful:
                rocket.fitness *= scaler
                for _ in range(int(rocket.fitness * 1000)):
                    mating_pool.append(rocket.original_dna)
        random.shuffle(mating_pool)
        print(f'Mating pool size: {len(mating_pool)}')

        def crossover(mother_dna, father_dna):
            new_dna = []
            # dna_sequence = mother_dna + father_dna + mother_dna
            split_point = random.randint(0, len(mother_dna))
            # new_dna = dna_sequence[split_point:split_point + len(mother_dna)]
            for gene in zip(mother_dna, father_dna):
                if random.random() < 0.5:
                    # new_dna.append(gene[0])  # Mother DNA
                    new_dna = mother_dna[0:split_point] + father_dna[split_point:]
                else:
                    # new_dna.append(gene[1])  # Mother DNA
                    new_dna = father_dna[0:split_point] + mother_dna[split_point:]
            for i in range(len(new_dna)):
                if random.random() <= MUTATION_RATE:
                    new_dna[i] = Q_Vector2D.random()
            assert(len(new_dna) == len(mother_dna) == len(father_dna))
            return new_dna

        rockets.clear()
        for _ in range(NUM_ROCKETS):
            mother_dna = mating_pool.pop()
            father_dna = mating_pool.pop()
            DNA = crossover(mother_dna=mother_dna, father_dna=father_dna)
            rocket = Rocket(x=WIDTH / 2, y=HEIGHT / 8 * 7, dna=DNA)
            rockets.append(rocket)

    pygame.quit()


if __name__ == '__main__':
    main()
