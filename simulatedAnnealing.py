import random
import heapq
import copy
import math
from math import sqrt
from itertools import islice
from operator import itemgetter
from numpy.random import random_integers as ri

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
        gap2 = abs((s[i-1] - P[i-1]))
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
            s[i] = s[i-1] + P[i]
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

def learn(i) -> list:
        global filename
        filename = i
        get_instance_on_file = get_instance("instances/" + filename)
        initialSolution = getInitialSolution(get_instance_on_file[1])
        feasibility_status = checkFeasibility(initialSolution[0], initialSolution[1])
        if feasibility_status:
            sa = SimulatedAnnealing(initialSolution= initialSolution, temperature=100.0, dec_temperature=0.92, num_iterations=30, max_changes=2)
            sa.run()
        else:
            print("ERROR: Initial solution not feasible!!!")
            return [-1]
        return sa.actual_state


class SimulatedAnnealing:

    def __init__(self, initialSolution, temperature, dec_temperature, num_iterations, max_changes):
        self.actual_state = []
        self.temperature = temperature
        self.dec_temperature = dec_temperature
        self.num_iterations = num_iterations
        self.max_changes = max_changes
        self.inc_neighbor = 10
        self.initial_state = initialSolution
        self.score = 0;
        self.size = len(initialSolution[0])
        self.max_value = 10;
        self.min_value =  -10;
        self.best_score = None
        self.best_s_arrangement = None

    #Como função de fitness vou somar a duração das tarefas com a solução dada
    def getFitness(self, P,s):
        sums = []
        for i in range(len(P)):
           sums.append(P[i] + s[i])
        return max(sums)

    def update_temperature(self):
        self.temperature *= self.dec_temperature


    def get_random_neighbor_2(self, P, current_s):
        neighbor = current_s

        changes = random.randint(1, self.max_changes) #vejo qual será o número de mudanças


        for i in random.sample([x for x in range(0, self.size-1)], changes):  #seleciono os vizinhos aleatórios para a mudança

            while True:
                perturbation = ri(-self.inc_neighbor,self.inc_neighbor) 

                if perturbation > 0:
                    perturbation = min(self.max_value, perturbation)
                else:
                    perturbation = max(self.min_value, perturbation)

                if neighbor[i] + perturbation >= 0:

                    neighbor[i] += perturbation
                    break

        for i in range(2, len(P)):
            gap1 = abs(neighbor[i-2] - neighbor[i-1])
            gap2 = abs((neighbor[i-1] - P[i-1]))
            max_gap = max(gap1, gap2)
            #Transform into feasible solution
            if 2*P[i] > max_gap:
                for j in range(1, len(P)):
                    if neighbor[j] > neighbor[i]:
                        neighbor[j] = neighbor[j] + 2*P[i] - max_gap
        return neighbor


    def get_random_neighbor(self, P, current_s):
        neighbor = current_s
        #List that the index that are going to change in this iteraction will be stored
        changes_list = []

        #changes = random.randint(1, self.max_changes) #vejo qual será o número de mudanças

        #Emulating do-while in python:

        while True:
            for i in random.sample([x for x in range(0, self.size-1)], self.max_changes):  #seleciono os vizinhos aleatórios para a mudança
              changes_list.append(i)
            if(changes_list[0] != changes_list[1]):
                break

        change1 = neighbor[changes_list[0]]
        change2 = neighbor[changes_list[1]]

        neighbor[changes_list[0]] = change2
        neighbor[changes_list[1]] = change1

        '''
         I don't think is a good idea checkFeasibility every time because this is expensive to do, so we d need a way to proove that the solution
        will be always factible when changing two neigboards. Since the initial solution is factible to everybody (abs(si- sj) >= min i, j, for all i, j in n)
        i can't see why just permutting the solution won't be factible anymore. Anyway, we have to think on a way to proove this
        print(checkFeasibility(P, neighbor))
        '''
        return neighbor


    def run(self):
        #initial_state: Tuple (P, s)
        self.actual_state_copy = self.initial_state 
        self.best_score = self.getFitness(self.actual_state_copy[0], self.actual_state_copy[1])
        self.actual_state_score = self.getFitness(self.actual_state_copy[0], self.actual_state_copy[1])
        self.best_s_arrangement = (self.actual_state_copy[0], self.actual_state_copy[1])
        while self.temperature > 0.01:
            self.update_temperature()
            for i in range(self.num_iterations):

                candidate = (self.actual_state_copy[0], self.get_random_neighbor_2(self.actual_state_copy[0].copy(), self.actual_state_copy[1].copy()))

                candidate_score = self.getFitness(self.actual_state_copy[0], candidate[1])

                delta = candidate_score - self.actual_state_score

                if(delta <= 0):
                    self.actual_state_copy = (self.actual_state_copy[0],  candidate[1])
                    self.actual_state_score = candidate_score
                    if self.best_score > self.actual_state_score:
                        self.best_s_arrangement = candidate
                        self.best_score = self.actual_state_score
                else:
                    boltz = math.exp(-float(delta)/self.temperature)
                    if(random.random() <= boltz):
                        self.actual_state_copy = (self.actual_state_copy[0],  candidate[1])
                        self.score = candidate_score
                        if self.best_score > self.actual_state_score:
                            self.best_s_arrangement = candidate
                            self.best_score = self.actual_state_score

        print(self)
        
    def __str__(self):
        with open("Output.txt", "a+") as text_file:
            print( '\n Valor encontrado para T na solução final do arquivo' + filename + ' = ' + str(self.best_score) + ' \n', file=text_file)

        return 'Solução final = \n' + str(["{0:0.2f}".format(i) for i in self.best_s_arrangement[1]]) + ' \n Solução inicial = \n' +  str(["{0:0.2f}".format(i) for i in self.initial_state[1]]) +  '\n Valor encontrado para T na solução inicial= \n' + str(self.getFitness(self.initial_state[0], self.initial_state[1])) + '\n Valor encontrado para T na solução final= \n' + str(self.best_score);
for i in ["trsp_50_1.dat", "trsp_50_2.dat"]:
    # for i in range(0, 3):
    learn(i)
