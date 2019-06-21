import random
import heapq
import copy
import math
from math import sqrt
from itertools import islice
from numpy.random import random_integers as ri
import numpy as np

#Just a function to guide us during development
#Idea: Test this when we generate neighboards, if is not feasible we brak and give an error
def checkFeasibility(P, s):
    status = True
    for i in range(0, len(P)):
        for j in range(0, len(P)):
            if status and i!=j:
                feasible = abs(s[i] - s[j]) >= min(P[i], P[j])
                if not(feasible):
                    status = False
    return status

def getInitialSolution(P):
    #Add descending order because we think this way the initial solution will be better
    P.sort(reverse=True)
    #start s array with -1
    s = [-1] * len(P)
    #Create the first and second si's because they are always the same
    i = 1
    s[i-1] = 0
    s[i] = s[i-1] + P[i]
    # start algorithm for the rest of the P's list
    for i in range(2, len(P)):
        gap1 = abs(s[i-2] - s[i-1])
        gap2 = abs((s[i-2] + P[i-2]) - (s[i-1] + P[i-1]))
        max_gap = max(gap1, gap2)
        #Transform into feasible solution
        if 2*P[i] > max_gap:
            for j in range(1, len(P)):
             if s[j] > s[i]:
                s[j] = s[j] + 2*P[i] - max_gap
        #continue with the algorithm
        if max_gap == gap1:
            s[i] = s[i-2] + P[i]
        else:
            s[i] = (s[i-1] + P[i-1]) + P[i]
    return (P,s)

def get_instance(filename):
    file = open(filename, 'r')

    weights = []

    instance_line_1 = file.readline().strip().split()

    for line in islice(file, 0, None):
        instance = line.strip().split()
        weights.append(float(instance[0]))        
    file.close()

    return int(instance_line_1[0]), weights

def learn() -> list:
        get_instance_on_file = get_instance("instances/teste.dat")
        initialSolution = getInitialSolution(get_instance_on_file[1])
        feasibility_status = checkFeasibility(initialSolution[0], initialSolution[1])
        if feasibility_status:
            sa = SimulatedAnnealing(initialSolution= initialSolution, temperature=100.0, dec_temperature=0.92, num_iterations=len(initialSolution[0]), max_changes=4)
            sa.run()
        else:
            print("ERROR: Initial solution not feasible!!!")
            return [-1]
        return sa.actual_state


class SimulatedAnnealing:

    def __init__(self, initialSolution, temperature, dec_temperature, num_iterations, max_changes=4):
        self.actual_state = []
        self.temperature = temperature
        self.dec_temperature = dec_temperature
        self.num_iterations = num_iterations
        self.max_changes = max_changes
        self.inc_neighbor = 2
        self.initial_state = initialSolution
        self.score = 0;
        self.max_value = 10;
        self.min_value =  -10;

    #TODO: HEEELP
    #Como função de fitness vou somar a duração das tarefas com a solução dada
    def getFitness(self, P,s):
        sums = []
        for i in range(len(P)):
           sums.append(P[i] + s[i])
        return max(sums)

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
        #initial_state: Tuple (P, s)
        self.actual_state_copy = self.initial_state 

        print(self.actual_state_copy)
        '''
        while self.temperature > 0.01:
            self.update_temperature()
            for i in range(self.num_iterations):
                candidate = self.get_random_neighbor(self.actual_state_copy.copy())

                candidate_score = self.getFitness(candidate)
                actual_state_score = self.getFitness(self.actual_state_copy)

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
        '''
    def __str__(self):
        return 'Estado da solução = \n' + str(["{0:0.2f}".format(i) for i in self.actual_state_copy]) + '\n Valor encontrado para T = \n' + str(self.score) + ' \n Solução inicial = \n' + str(self.initial_state);

learn()
