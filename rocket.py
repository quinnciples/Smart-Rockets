import math
import sys
sys.path.append("C:\\users\\alexa\\Documents\\Github\\QFunctions")
from Q_Functions import Q_Vector2D


class Rocket:
    LENGTH = 30
    WIDTH = 10
    COLOR = (255, 255, 255)

    def __init__(self, x, y, dna: list):
        self.velocity = Q_Vector2D(angle=0, magnitude=0)
        self.x = x
        self.y = y
        self.dna = [x for x in dna]
        self.original_dna = [x for x in dna]
        self.active = True
        self.fitness = math.inf
        self.successful = False

    def apply_force(self) -> None:
        if self.active:
            if self.dna:
                acceleration = self.dna.pop(0)
            else:
                acceleration = Q_Vector2D(angle=0, magnitude=0)
            self.velocity = self.velocity + acceleration
            self.velocity.limit(2)

    def stop(self):
        self.velocity.magnitude = 0.0
        self.active = False

    def update(self):
        self.x = self.x + self.velocity.x
        self.y = self.y + self.velocity.y

    @property
    def angle_in_degrees(self):
        return self.velocity.degrees

    def calculate_fitness(self, target):
        if self.active or self.successful:
            # self.fitness = 1 / (math.sqrt(((target[1] - self.y) ** 2) + ((target[0] - self.x) ** 2)) + 0.0001)
            self.fitness = 1 / (((target[1] - self.y) ** 2) + ((target[0] - self.x) ** 2) + 0.0001)
        else:
            self.fitness = 0


if __name__ == '__main__':
    pass
