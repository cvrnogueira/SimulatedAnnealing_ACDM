import random
import heapq
import copy
import math
from math import sqrt
from itertools import islice


def get_instance(filename):
    file = open(filename, 'r')

    weights = []

    instance_line_1 = file.readline().strip().split()

    for line in islice(file, 1, None):
        instance = line.strip().split()
        weights.append(float(instance[0]))        
    file.close()

    return int(instance_line_1[0]), weights



def normalize01(x, func, a, b):
    a, b = min(func(a), func(b)), max(func(a), func(b))

    return (func(x) - a) / (b - a)


def learn(N, P) -> list:
        sa = SimulatedAnnealing(size= N, weights = P, temperature=100.0, dec_temperature=0.92, num_iterations=N, max_changes=8)
        #sa.fitness_function = self.run_episode
        sa.run()

        return sa.current_state


class SimulatedAnnealing:

    def __init__(self, weights, size, temperature, dec_temperature, num_iterations, max_changes=8):
        self.current_state = []
        self.size = size
        self.min_value = -10
        self.max_value = 10
        self.temperature = temperature
        self.dec_temperature = dec_temperature
        self.num_iterations = num_iterations
        self.max_changes = max_changes
        self.inc_neighbor = 2
        self.initial_state = weights
        self.score = 0;

    #Como função de fitness vou somar a duração das tarefas com a solução dada
    def fitness_function(self, solution):        
        print(solution)
        #  print(weights)

    def update_temperature(self):
        self.temperature *= self.dec_temperature

    def get_random_neighbor(self, current):
        neighbor = current

        changes = random.randint(1, self.max_changes)
        for i in random.sample([x for x in range(0, self.size)], changes):
            inc =  random.uniform(-self.inc_neighbor, self.inc_neighbor)
            if inc > 0:
                inc = min(self.max_value, inc)
            else:
                inc = max(self.min_value, inc)
            neighbor[i] += inc

        return neighbor


    def run(self):
        #Solução inicial : exato como foi a leitura do arquivo
        self.current_state = self.initial_state

        while self.temperature > 0.01:
             self.update_temperature()
             for i in range(2): #(self.num_iterations):
                candidate = self.get_random_neighbor(self.current_state.copy())

                candidate_score = self.fitness_function(candidate)
               # current_state_score = self.fitness_function(self.current_state)

        #         delta = candidate_score - current_state_score
        #         self.score = current_state_score

        #         if(delta > 0):
        #             self.current_state = candidate
        #             self.score = candidate_score
        #         else:
        #             p = math.exp(delta/self.temperature)
        #             if(random.random() < p):
        #                 self.current_state = candidate
        #                 self.score = candidate_score

        #    print("Temperature "+str("{0:0.2f}".format(self.temperature))+":")
        #    print(self)

    def __str__(self):
        return 'state = ' + str(["{0:0.2f}".format(i) for i in self.current_state]) + ' score = ' + str(self.score);

get_instance_on_file = get_instance("trsp/trsp_50_1.dat")
learn(get_instance_on_file[0], get_instance_on_file[1])
