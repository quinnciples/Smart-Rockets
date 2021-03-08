import math
import sys
from typing import MappingView
sys.path.append("C:\\users\\alexa\\Documents\\Github\\QFunctions")
from Q_Functions import Q_Vector2D
from Q_Functions import Q_map


class Rocket:
    def __init__(self, x, y, dna: list):
        self.velocity = Q_Vector2D(angle=0, magnitude=0)
        self.x = x
        self.y = y
        self.dna = dna

    def apply_force(self) -> None:
        if self.dna:
            acceleration = self.dna.pop(0)
        else:
            acceleration = Q_Vector2D(angle=0, magnitude=0)
        self.velocity = self.velocity + acceleration

    def stop(self):
        self.velocity.magnitude = 0

    def update(self):
        self.x = self.x + self.velocity.x
        self.y = self.y + self.velocity.y

    @property
    def angle_in_degrees(self):
        return self.velocity.degrees


if __name__ == '__main__':
    pass
