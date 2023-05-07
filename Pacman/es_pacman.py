import random
import math


POPULATION_SIZE = 10
NUM_GENERATIONS = 5
MUTATION_RATE = 0.05


def create_population():
    population = []
    for i in range(POPULATION_SIZE):
        individual = [random.randint(0, 3) for j in range(50)]
        population.append(individual)
    return population


def evaluate_fitness(individual, layout, pacman_pos, ghosts_pos):
    pacman = pacman_pos
    ghosts = ghosts_pos
    score = 0
    num_moves = 0

    for i in range(len(individual)):
        direction = individual[i]
        if direction == 0:
            next_pos = (pacman.row - 1, pacman.col)
        elif direction == 1:
            next_pos = (pacman.row, pacman.col + 1)
        elif direction == 2:
            next_pos = (pacman.row + 1, pacman.col)
        else:
            next_pos = (pacman.row, pacman.col - 1)

        if next_pos in layout.walls.asList():
            continue

        pacman = Pacman(*next_pos)
        num_moves += 1

        for ghost in ghosts:
            if pacman.row == ghost.row and pacman.col == ghost.col:
                score -= 10  # Penalizar a Pacman si es atrapado por un fantasma

        if pacman.get_position() in layout.food.asList():
            score += 1

        if pacman.get_position() in layout.capsules:
            score += 10

        if layout.isWin(score):
            break

        if num_moves >= 1000:
            break

    return score


def select_parents(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    probabilities = [fitness_score / total_fitness for fitness_score in fitness_scores]
    parent_indices = random.choices(range(len(population)), weights=probabilities, k=2)
    return [population[parent_indices[0]], population[parent_indices[1]]]


def reproduce(parents):
    children = []
    for i in range(POPULATION_SIZE):
        parent1, parent2 = parents
        crossover_point = random.randint(1, len(parent1) - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        children.append(child)
    return children


def mutate(individual):
    for i in range(len(individual)):
        if random.random() < MUTATION_RATE:
            individual[i] = random.randint(0, 3)
    return individual


def get_next_move(layout, pacman_pos, ghosts_pos):
    population = create_population()

    for generation in range(NUM_GENERATIONS):
        fitness_scores = [evaluate_fitness(individual, layout, pacman_pos, ghosts_pos) for individual in population]
        parents = select_parents(population, fitness_scores)
        children = reproduce(parents)
        population = parents + children
        population = [mutate(individual) for individual in population]

    fitness_scores = [evaluate_fitness(individual, layout, pacman_pos, ghosts_pos) for individual in population]
    best_individual = population[fitness_scores.index(max(fitness_scores))]

    return best_individual[0]  # Devuelve el primer movimiento del mejor individuo
