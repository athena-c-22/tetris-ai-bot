from random import uniform, choices, randint, randrange, random
from visual import run

population_size = 18

def generate_genome():
    genome = [-19.916366988549214 + uniform(-10, 10), -0.27026029511791627 + uniform(-10, 10), -1.5392396093619634 + uniform(-10, 10), -0.7875854176515529 + uniform(-10, 10), 3.7747020546884453 + uniform(-10, 10), -100.76555287796035 + uniform(-10, 10), 0.42446341412810096 + uniform(-10, 10)]
    return genome

def generate_population(population_size):
    population = [generate_genome() for _ in range(population_size)]
    return population

def fitness(weights):
    score = run(weights)
    return score

def selection(population):
    return choices(
        population=population,
        weights = [fitness(genome) for genome in population],
        k=2
    )

def single_point_crossover(genome1, genome2):
    if len(genome1) != len(genome2):
        raise ValueError("Genomes 1 and 2 must be of same length")
    
    length = len(genome1)
    if length < 2:
        return genome1, genome2
    
    p = randint(1, length - 1)
    return genome1[0:p] + genome2[p:], genome2[0:p] + genome1[p:]

def mutate(genome, num=1, probability=0.5):
    for _ in range(num):
        index = randrange(len(genome))
        genome[index] = genome[index] if random() > probability else genome[index] + uniform(-1, 1)
    return genome

def run_evolution(population_size, fitness_limit=21000, generation_limit=100):
    population = generate_population(population_size)

    for i in range(generation_limit):
        population = sorted(population, key=lambda genome:fitness(genome), reverse=True)

        if fitness(population[0]) >= fitness_limit:
            break

        next_generation = population[0:2]

        for j in range(int(len(population) / 2) - 1):
            parents = selection(population)
            offspring_a, offspring_b = single_point_crossover(parents[0], parents[1])
            offspring_a = mutate(offspring_a)
            offspring_b = mutate(offspring_b)
            next_generation += [offspring_a, offspring_b]

        population = next_generation

    population = sorted(population, key=lambda genome: fitness(genome), reverse=True)

    return population, i

breakpoint()
population, generations = run_evolution(18, 21000, 2)
print(population, generations)