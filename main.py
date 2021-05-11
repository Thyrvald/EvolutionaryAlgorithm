# author: Paweł Gosk

from functions import *


def main():
    population_size = 10000
    population = generate_new_population(population_size)
    number_of_generations = 100
    evaluate_population(population)
    for generation in range(number_of_generations):
        offsprings = tournament_selection(population)
        population = generative_succession(offsprings, population_size)
        mutate_population(population)
        evaluate_population(population)

    ten_best_individuals = find_individuals_with_maximum_productivity(population, 10)
    file = open(f'results{population_size}.txt', 'w')
    file.write(f"Population size: {population_size}\n")
    for individual in ten_best_individuals:
        file.write(str(individual) + '\n')
    file.close()


if __name__ == '__main__':
    main()
