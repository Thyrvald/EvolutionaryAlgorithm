# author: Paweł Gosk

from random import *


class Individual:
    def __init__(self):
        self.sleep_time = randint(4, 10)
        self.work_time = randint(2, 12)
        self.work_intensity = randint(1, 10)
        self.tough_party = randint(0, 1)
        self.gentle_party = randint(0, 1)
        self.healthy_food = randint(0, 5)
        self.sport = randint(0, 4)
        self.work_curiosity = randint(0, 10)
        self.productivity = 10
        self.is_evaluated = False

    def __str__(self):
        return "sleep time: " + str(self.sleep_time) + " work time: " + str(self.work_time) + " work intensity: " + str(
            self.work_intensity) + " tough party: " + str(self.tough_party) + " gentle party: " + str(
            self.gentle_party) + " healthy food: " + str(self.healthy_food) + " sport: " + str(
            self.sport) + " work curiosity : " + str(self.work_curiosity) + "\n overall productivity: " + str(
            self.productivity)

    def change_is_evaluated(self):
        if self.is_evaluated:
            self.is_evaluated = False
        else:
            self.is_evaluated = True


def generate_new_population(population_size):
    list_of_individuals = []
    for i in range(population_size):
        new_individual = Individual()
        list_of_individuals.append(new_individual)
    return list_of_individuals


def evaluate_individual(individual):
    if individual.is_evaluated:
        return
    individual.productivity = 10
    exhaust = 10
    work_progress = 10
    well_being = 10
    time_spent_on_work_in_week = individual.work_time * 5

    if individual.sleep_time < 4:
        exhaust *= pow(0.99, individual.sleep_time)
        well_being *= 0.6
    if individual.sleep_time < 7:
        exhaust *= pow(0.97, individual.sleep_time)
        well_being *= 0.8
    elif 8 <= individual.sleep_time < 11:
        exhaust *= pow(0.9, individual.sleep_time)
    else:
        exhaust *= pow(0.93, individual.sleep_time)

    if individual.work_curiosity >= 9:
        individual.work_intensity = round(individual.work_intensity * 1.5)
        if individual.work_intensity > 10:
            individual.work_intensity = 10
    elif individual.work_curiosity < 4:
        individual.work_intensity = round(individual.work_intensity * 0.8)
        if individual.work_intensity < 1:
            individual.work_intensity = 1

    if individual.work_intensity < 4:
        work_progress_parameter = 0.45
        work_exhaustion_parameter = 0.97
    elif individual.work_intensity < 7:
        work_progress_parameter = 0.7
        work_exhaustion_parameter = 1
    elif individual.work_intensity < 9:
        work_progress_parameter = 0.9
        work_exhaustion_parameter = 1.1
    else:
        work_progress_parameter = 1
        work_exhaustion_parameter = 1.2

    work_progress += work_progress * pow(1.1, individual.work_time) * work_progress_parameter
    if individual.work_time < 6:
        exhaust *= (1.04 ** individual.work_time * work_exhaustion_parameter)
    elif individual.work_time < 9:
        exhaust *= (1.06 ** individual.work_time * work_exhaustion_parameter)
        work_progress *= 1.1
    elif individual.work_time < 11:
        exhaust *= (1.1 ** individual.work_time * work_exhaustion_parameter)
        work_progress *= 1.13
    else:
        exhaust *= (1.2 ** individual.work_time * work_exhaustion_parameter)
        work_progress *= 1.16

    if individual.tough_party:
        well_being *= 1 + individual.tough_party / 20
        time_spent_on_work_in_week -= individual.tough_party
        exhaust *= 1 + individual.tough_party / 10

    if individual.gentle_party:
        well_being *= 1 + individual.gentle_party / 10
        time_spent_on_work_in_week -= individual.gentle_party
        exhaust *= 1 + individual.tough_party / 20

    if individual.healthy_food == 0:
        well_being *= 0.95
    elif individual.healthy_food > 3:
        well_being *= 1.1
        time_spent_on_work_in_week -= 2

    if individual.sport == 0:
        well_being *= 0.95
    else:
        well_being *= 1 + individual.sport / 15
        time_spent_on_work_in_week -= individual.sport

    individual.productivity *= time_spent_on_work_in_week / (individual.work_time * 5)
    individual.productivity *= 10 / exhaust
    individual.productivity *= well_being / 10
    if work_progress / 10 < 15:
        individual.productivity *= 0.95
    elif work_progress > 20:
        individual.productivity *= 1.1

    if individual.work_curiosity < 2:
        individual.productivity *= 0.6
    elif individual.work_curiosity < 3:
        individual.productivity *= 0.8
    elif individual.work_curiosity < 6:
        individual.productivity *= 0.9
    elif individual.work_curiosity < 9:
        individual.productivity *= 1
    else:
        individual.productivity *= 1.1

    individual.productivity = round(individual.productivity, 2)
    individual.change_is_evaluated()


def evaluate_population(list_of_individuals):
    for individual in list_of_individuals:
        evaluate_individual(individual)


def tournament_selection(list_of_individuals):
    list_of_offsprings = []
    list_of_indices_to_leave = []
    for individual in list_of_individuals:
        list_of_offsprings.append(individual)
    for i in range(0, (len(list_of_individuals) - 1)):
        first_competitor = generate_index(len(list_of_offsprings) - 1, list_of_indices_to_leave)
        second_competitor = generate_index(len(list_of_offsprings) - 1, list_of_indices_to_leave)
        if first_competitor == -1 or second_competitor == -1:
            return list_of_offsprings
        elif first_competitor == second_competitor:
            list_of_indices_to_leave.append(first_competitor)
        else:
            if list_of_offsprings[first_competitor].productivity > list_of_offsprings[second_competitor].productivity:
                list_of_indices_to_leave.append(first_competitor)
                list_of_offsprings.remove(list_of_offsprings[second_competitor])
            else:
                list_of_indices_to_leave.append(second_competitor)
                list_of_offsprings.remove(list_of_offsprings[first_competitor])
    return list_of_offsprings


def generate_index(rand_range, indices):
    index = randint(0, rand_range)
    while_iteration_count = 1
    while check_if_index_in_list(index, indices):
        index = randint(0, rand_range)
        while_iteration_count += 1
        if while_iteration_count == len(indices):
            return -1
    return index


def check_if_index_in_list(index, list_of_indices):
    if list_of_indices:
        for i in list_of_indices:
            if index == i:
                return True
    return False


def mutate_individual(individual):
    if individual.is_evaluated:
        individual.change_is_evaluated()
    position_of_bit_to_mutate = randint(1, 8)
    if position_of_bit_to_mutate == 1:
        individual.sleep_time = round(individual.sleep_time * uniform(0.8, 1.3), 2)
        if individual.sleep_time > 12:
            individual.sleep_time = 12
    elif position_of_bit_to_mutate == 2:
        individual.work_time = round(individual.work_time * uniform(0.8, 1.3))
    elif position_of_bit_to_mutate == 3:
        individual.work_intensity = round(individual.work_intensity * uniform(0.9, 1.2))
        if individual.work_intensity < 1:
            individual.work_intensity = 1
        elif individual.work_intensity > 10:
            individual.work_intensity = 10
    elif position_of_bit_to_mutate == 4:
        individual.tough_party += randint(-1, 3)
        if individual.tough_party < 0:
            individual.tough_party += 1
    elif position_of_bit_to_mutate == 5:
        individual.gentle_party += randint(-1, 3)
        if individual.gentle_party < 0:
            individual.gentle_party += 1
    elif position_of_bit_to_mutate == 6:
        individual.healthy_food += randint(-5, 5)
        if individual.healthy_food > 5:
            individual.healthy_food = 5
        elif individual.healthy_food < 0:
            individual.healthy_food = 0
    elif position_of_bit_to_mutate == 7:
        individual.sport += randint(-4, 4)
        if individual.sport < 0:
            individual.sport = 0
    else:
        individual.work_curiosity = round(individual.work_curiosity * uniform(0.9, 1.2), 2)
        if individual.work_curiosity > 10:
            individual.work_curiosity = 10


def mutate_population(population):
    for individual in population:
        if randint(0, 100) < 30:
            mutate_individual(individual)


def generative_succession(list_of_offsprings, population_size):
    new_generation = generate_new_population(population_size)
    maximum_swap_index = 0
    index_of_individual_to_swap = 0
    for individual in list_of_offsprings:
        if len(new_generation) - maximum_swap_index > 0:
            index_of_individual_to_swap = randint(0, len(new_generation) - 1 - maximum_swap_index)
        new_generation.remove(new_generation[index_of_individual_to_swap])
        new_generation.append(individual)
        maximum_swap_index += 1
    return new_generation


def find_individuals_with_maximum_productivity(population, number_wanted_individuals):
    max_individuals = []
    max_individuals_indices = []
    if len(population) < number_wanted_individuals:
        wanted_individuals = len(population)
    else:
        wanted_individuals = number_wanted_individuals

    for i in range(wanted_individuals):
        max_index = 0
        for individual in population:
            if individual.productivity > population[max_index].productivity:
                if not check_if_index_in_list(population.index(individual), max_individuals_indices):
                    max_index = population.index(individual)
        if not check_if_index_in_list(max_index, max_individuals_indices):
            max_individuals_indices.append(max_index)

    for index in max_individuals_indices:
        max_individuals.append(population[index])
    return max_individuals
