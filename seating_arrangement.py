import random
import numpy as np

class SeatingArrangement:
    def __init__(self):
        self.students = []
        self.rows = 0
        self.cols = 0
        self.constraints = []

    def create_initial_population(self, pop_size):
        seats = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        if len(seats) < len(self.students):
            raise ValueError("Number of seats is less than number of students.")
        return [random.sample(seats, len(self.students)) for _ in range(pop_size)]

    def fitness(self, shibutz):
        score = 0
        seat_positions = {self.students[i]: shibutz[i] for i in range(len(self.students))}
        for constraint in self.constraints:
            if constraint[0] == 'not_next_to':
                student1, student2_list = constraint[1], constraint[2]
                for student2 in student2_list:
                    if student1 in seat_positions and student2 in seat_positions:
                        pos1, pos2 = seat_positions[student1], seat_positions[student2]
                        if not self.are_neighbors(pos1, pos2):
                            score += 1
            elif constraint[0] == 'next_to':
                student1, student2_list = constraint[1], constraint[2]
                for student2 in student2_list:
                    if student1 in seat_positions and student2 in seat_positions:
                        pos1, pos2 = seat_positions[student1], seat_positions[student2]
                        if self.are_neighbors(pos1, pos2):
                            score += 1
            elif constraint[0] == 'preferred_location':
                student, row, col = constraint[1], constraint[2], constraint[3]
                if student in seat_positions:
                    if seat_positions[student] == (row, col):
                        score += 1
        return score

    def are_neighbors(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) <= 1 and abs(pos1[1] - pos2[1]) <= 1

    def crossover(self, parent1, parent2):
        idx = random.randint(0, len(parent1)-1)
        child1 = parent1[:idx] + [p for p in parent2 if p not in parent1[:idx]]
        child2 = parent2[:idx] + [p for p in parent1 if p not in parent2[:idx]]
        return child1, child2

    def mutate(self, shibutz, mutation_rate=0.01):
        for i in range(len(shibutz)):
            if random.random() < mutation_rate:
                j = random.randint(0, len(shibutz)-1)
                shibutz[i], shibutz[j] = shibutz[j], shibutz[i]
        return shibutz

    def genetic_algorithm(self, pop_size, generations):
        population = self.create_initial_population(pop_size)
        for _ in range(generations):
            population = sorted(population, key=lambda shibutz: self.fitness(shibutz), reverse=True)
            next_generation = population[:pop_size//2]
            while len(next_generation) < pop_size:
                parent1, parent2 = random.sample(population[:pop_size//2], 2)
                child1, child2 = self.crossover(parent1, parent2)
                next_generation += [self.mutate(child1), self.mutate(child2)]
            population = next_generation
        best_shibutz = sorted(population, key=lambda shibutz: self.fitness(shibutz), reverse=True)[0]
        return best_shibutz

    def display_seating(self, shibutz):
        seating = np.empty((self.rows, self.cols), dtype=object)
        for i, pos in enumerate(shibutz):
            seating[pos] = self.students[i]
        return seating
