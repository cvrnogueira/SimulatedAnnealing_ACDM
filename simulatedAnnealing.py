import random
import heapq
import copy
import math
from math import sqrt
from itertools import islice
from numpy.random import random_integers as ri
import numpy as np


def checkFeasibility(P, s):
    status = True
    for i in range(0, len(P)):
        for j in range(0, len(P)):
            if status and i!=j:
                feasible = abs(s[i] - s[j]) >= min(P[i], P[j])
                if not(feasible):
                    print("feasibilty print")
                    print(s[i], s[j],  abs(s[i] - s[j]), P[i], P[j], min(P[i], P[j]))
                    status = False
    return status

def getInitialSolution(P):
    order_descending = P.sort(reverse=True)
    s = [0] * len(P)
    chosen_gaps = [0] * len(P)
    i = 1
    s[i-1] = 0
    s[i] = s[i-1] + P[i]
    chosen_gaps[1] = abs(s[0] - s[1])
    for i in range(2, len(P)):
        gap1 = abs(s[i-2] - s[i-1])
        gap2 = abs((s[i-2] + P[i-2]) - (s[i-1] + P[i-1]))
        max_gap = max(gap1, gap2)
        chosen_gaps[i] = max_gap
        if 2*P[i] > chosen_gaps[i]:
            problematic_gap = chosen_gaps[i]
            problematic_indice = i
            for j in range(1, len(P)):
             if s[j] > s[problematic_indice]:
                s[j] = s[j] + 2*P[problematic_indice] - problematic_gap

        if max_gap == gap1:
            s[i] = s[i-2] + P[i]
        else:
            s[i] = (s[i-1] + P[i-1]) + P[i]
    print("solution print")
    print(P, s, chosen_gaps)
    return (P,s, chosen_gaps)

def transformIntoFeasibleSolution(P, s, chosen_gaps):
    #gap começa em zero!!
    if not(checkFeasibility(P, s)):
        for i in range(1,len(P)):
            if 2*P[i] > chosen_gaps[i]:
                problematic_gap = chosen_gaps[i]
                problematic_indice = i
            break;

        for i in range(1, len(P)):
             if s[i] > s[problematic_indice]:
                s[i] = s[i] + 2*P[problematic_indice] - problematic_gap

    return(P, s, checkFeasibility(P, s))

def get_instance(filename):
    file = open(filename, 'r')

    weights = []

    instance_line_1 = file.readline().strip().split()

    for line in islice(file, 0, None):
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

get_instance_on_file = get_instance("instances/teste.dat")
initialSolution = getInitialSolution(get_instance_on_file[1])
#feasibility_status = checkFeasibility(initialSolution[0], initialSolution[1])
#if not(feasibility_status):
response = transformIntoFeasibleSolution(initialSolution[0], initialSolution[1], initialSolution[2])
print(response)
#learn(get_instance_on_file[0], get_instance_on_file[1])
