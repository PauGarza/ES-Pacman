import random
import numpy as np
import copy
from Pacman import Game
from Pacman import Pacman


POP_SIZE = 100
GENE_LENGTH = 4
MUTATION_RATE = 0.1
ELITISM = True

def run_es():
    global POP_SIZE, GENE_LENGTH, MUTATION_RATE, ELITISM
    
    weights = evolve(POP_SIZE, GENE_LENGTH, MUTATION_RATE, ELITISM)
    return tuple(weights)

def evolve(population_size, gene_length, mutation_rate, elitism):
    population = initialize_population(population_size, gene_length)
    for i in range(100):
        population = next_generation(population, mutation_rate, elitism)
    fitness_scores = evaluate_population(population)
    return select_best_individual(population, fitness_scores)

def initialize_population(population_size, gene_length):
    population = []
    for i in range(population_size):
        individual = []
        for j in range(gene_length):
            individual.append(random.uniform(-1, 1))
        population.append(individual)
    return population

def next_generation(population, mutation_rate, elitism):
    fitness_scores = evaluate_population(population)
    new_population = []
    if elitism:
        best_individual = select_best_individual(population, fitness_scores)
        new_population.append(best_individual)
    while len(new_population) < len(population):
        parent1 = select_individual_by_tournament(population, fitness_scores)
        parent2 = select_individual_by_tournament(population, fitness_scores)
        child = crossover(parent1, parent2)
        if random.random() < mutation_rate:
            mutate(child)
        new_population.append(child)
    return new_population

def evaluate_population(population):
    fitness_scores = []
    for individual in population:
        score = evaluate_individual(individual)
        fitness_scores.append(score)
    return fitness_scores

def evaluate_individual(individual):
    weights = tuple(individual)
    game_state = Game()
    pacman_agent = Pacman()
    game_state.initialize()
    pacman_agent.registerInitialState(game_state)
    while not game_state.isWin() and not game_state.isLose():
        action = pacman_agent.getAction(game_state)
        game_state = game_state.generateSuccessor(0, action)
        pacman_position = game_state.getPacmanPosition()
        ghost_positions = game_state.getGhostPositions()
        food = game_state.getFood().asList()
        score = game_state.getScore()
        distances = [manhattan_distance(pacman_position, ghost_position) for ghost_position in ghost_positions] + [manhattan_distance(pacman_position, food_position) for food_position in food]
        output = np.dot(np.array(weights), np.array(distances))
        pacman_agent.setFitness(output)
    return pacman_agent.getFitness()

def select_individual_by_tournament(population, fitness_scores):
    tournament_size = 5
    tournament = random.sample(range(len(population)), tournament_size)
    best_index = tournament[0]
    for i in tournament:
        if fitness_scores[i] > fitness_scores[best_index]:
            best_index = i
    return population[best_index]

def select_best_individual(population, fitness_scores):
    best_index = 0
    for i in range(len(population)):
        if fitness_scores[i] > fitness_scores[best_index]:
            best_index = i
    return population[best_index]

def crossover(parent1, parent2):
    child = copy.deepcopy(parent1)
    crossover_point = random.randint(1, len(parent1) - 1)
    child[crossover_point:] = parent2[crossover_point:]
    return child

def mutate(individual):
    mutation_index = random.randint(0, len(individual) - 1)
    individual[mutation_index] += random.uniform(-0.1, 0.1)
    if individual[mutation_index] > 1:
        individual[mutation_index] = 1
    elif individual[mutation_index] < -1:
        individual[mutation_index] = -1

def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
