import random
import heapq
import copy
import math
from math import sqrt
from itertools import islice
from numpy.random import random_integers as ri


def get_instance(filename):
    file = open(filename, 'r')

    weights = []

    instance_line_1 = file.readline().strip().split()

    for line in islice(file, 1, None):
        instance = line.strip().split()
        weights.append(float(instance[0]))        
    file.close()

    return int(instance_line_1[0]), weights

def learn(N, P) -> list:
        sa = SimulatedAnnealing(size= N, weights = P, temperature=100.0, dec_temperature=0.92, num_iterations=N, max_changes=4)
        #sa.fitness_function = self.run_episode
        sa.run()

        return sa.actual_state


class SimulatedAnnealing:

    def __init__(self, weights, size, temperature, dec_temperature, num_iterations, max_changes=4):
        self.actual_state = []
        self.size = size
        self.temperature = temperature
        self.dec_temperature = dec_temperature
        self.num_iterations = num_iterations
        self.max_changes = max_changes
        self.inc_neighbor = 2
        self.initial_state = weights
        self.score = 0;
        self.max_value = 10;
        self.min_value =  -10;

    #TODO: HEEELP
    #Como função de fitness vou somar a duração das tarefas com a solução dada
    def fitness_function(self, solution):       
        value = sum(solution) 
        return value

    def update_temperature(self):
        self.temperature *= self.dec_temperature


    def get_random_neighbor(self, current):
        neighbor = current

        changes = random.randint(1, self.max_changes) #vejo qual será o número de mudanças
        for i in random.sample([x for x in range(0, self.size-1)], changes):  #seleciono os vizinhos aleatórios para a mudança

            perturbation = ri(-self.inc_neighbor,self.inc_neighbor) 

            if perturbation > 0:
                perturbation = min(self.max_value, perturbation)
            else:
                perturbation = max(self.min_value, perturbation)

            neighbor[i] += perturbation

        return neighbor


    def run(self):
        #Solução inicial : exato como foi a leitura do arquivo
        self.actual_state_copy = self.initial_state

        while self.temperature > 0.01:
            self.update_temperature()
            for i in range(self.num_iterations):
                candidate = self.get_random_neighbor(self.actual_state_copy.copy())

                candidate_score = self.fitness_function(candidate)
                actual_state_score = self.fitness_function(self.actual_state_copy)

                delta = candidate_score - actual_state_score
                self.score = actual_state_score

                if(delta > 0):
                    self.actual_state_copy = candidate
                    self.score = candidate_score
                else:
                    p = math.exp(delta/self.temperature)
                    if(random.random() < p):
                        self.actual_state_copy = candidate
                        self.score = candidate_score
        print(self)

    def __str__(self):
        return 'Estado da solução = \n' + str(["{0:0.2f}".format(i) for i in self.actual_state_copy]) + '\n Valor encontrado para T = \n' + str(self.score) + ' \n Solução inicial = \n' + str(self.initial_state);

get_instance_on_file = get_instance("trsp/trsp_50_1.dat")
learn(get_instance_on_file[0], get_instance_on_file[1])
