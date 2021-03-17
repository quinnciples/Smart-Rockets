import pygame
import math
import sys
import random
import time
random.seed(time.perf_counter())
sys.path.append("C:\\users\\alexa\\Documents\\Github\\QFunctions")
from Q_Functions import Q_Vector2D
from Q_Functions import Q_weighted_choice3 as weighted_choice
import string

from difflib import ndiff


def calculate_levenshtein_distance(str_1, str_2):
    """
    The Levenshtein distance is a string metric for measuring the difference between two sequences.
    It is calculated as the minimum number of single-character edits necessary to transform one string into another
    """
    distance = 0
    buffer_removed = buffer_added = 0
    for x in ndiff(str_1, str_2):
        code = x[0]
        # Code ? is ignored as it does not translate to any modification
        if code == ' ':
            distance += max(buffer_removed, buffer_added)
            buffer_removed = buffer_added = 0
        elif code == '-':
            buffer_removed += 1
        elif code == '+':
            buffer_added += 1
    distance += max(buffer_removed, buffer_added)
    return distance


class Monkey:

    def __init__(self, sequence_length=42):
        self.sequence = ''.join([random.choice(string.ascii_letters + " " + string.punctuation) for _ in range(sequence_length)])
        self.fitness = 0

    def calculate_fitness(self, target):
        assert len(target) == len(self.sequence)
        new_fitness = random.uniform(0, 0.2)
        for expected_char, actual_char in zip(target, self.sequence):
            if expected_char == actual_char:
                new_fitness += 1
        self.fitness = new_fitness
        # new_fitness = calculate_levenshtein_distance(target, self.sequence)
        # self.fitness = 1 / new_fitness


def main():

    NUM_MONKEYS = 500
    MUTATION_RATE = 0.005
    TARGET = 'To be, or not to be? That is the question.'
    ITERATIONS = 0
    monkeys = []
    new_monkeys = []

    for _ in range(NUM_MONKEYS):
        monkey = Monkey()
        monkeys.append(monkey)

    running = True

    while running > 0:
        ITERATIONS += 1

        max_fitness = 0
        best_guess = ''
        for monkey in monkeys:
            if monkey.sequence == TARGET:
                running = False
            monkey.calculate_fitness(target=TARGET)
            if monkey.fitness >= max_fitness:
                max_fitness = monkey.fitness
                best_guess = monkey.sequence

        print(f'Iteration: {ITERATIONS} Max fitness: {max_fitness:.0f} *** Best guess: {best_guess}')

        mating_pool = [idx for idx, monkey in enumerate(monkeys)]
        mating_weights = [monkey.fitness for idx, monkey in enumerate(monkeys)]

        def crossover(mother_dna, father_dna):
            new_dna = []
            # dna_sequence = mother_dna + father_dna + mother_dna
            split_point = random.randint(0, len(mother_dna))
            # new_dna = dna_sequence[split_point:split_point + len(mother_dna)]
            for gene in zip(mother_dna, father_dna):
                if random.random() < 0.5:
                    new_dna += gene[0]  # Mother DNA
                    # new_dna = mother_dna[0:split_point] + father_dna[split_point:]
                else:
                    new_dna += gene[1]  # Mother DNA
                    # new_dna = father_dna[0:split_point] + mother_dna[split_point:]
            for i in range(len(new_dna)):
                if random.random() <= MUTATION_RATE:
                    new_dna[i] = random.choice(string.ascii_letters + " " + string.punctuation)
            new_dna = ''.join([ _ for _ in new_dna])
            assert(len(new_dna) == len(mother_dna) == len(father_dna))
            return new_dna

        new_monkeys.clear()
        for _ in range(NUM_MONKEYS):
            mother_choice, father_choice = weighted_choice(list_of_choices=mating_pool, list_of_weights=mating_weights, number_of_choices=2, replacement=False)
            mother_dna = monkeys[mother_choice].sequence
            father_dna = monkeys[father_choice].sequence
            DNA = crossover(mother_dna=mother_dna, father_dna=father_dna)
            monkey = Monkey()
            monkey.sequence = DNA
            new_monkeys.append(monkey)
        monkeys = None
        monkeys = [monkey for monkey in new_monkeys]
        new_monkeys.clear()


if __name__ == '__main__':
    main()
