from __future__ import absolute_import, division, print_function

import random
from collections import deque
from platypus import EpsilonProgressContinuation, RandomGenerator, TournamentSelector, Multimethod,\
    GAOperator, SBX, PM, UM, PCX, UNDX, SPX, DifferentialEvolution, EpsMOEA

class BorgMOEA(EpsilonProgressContinuation):
    
    def __init__(self, problem,
                 epsilons,
                 population_size = 100,
                 generator = RandomGenerator(),
                 selector = TournamentSelector(2),
                 recency_list_size = 50,
                 max_mutation_index = 10,
                 **kwargs):
        super(BorgMOEA, self).__init__(
                EpsMOEA(problem,
                        epsilons,
                        population_size,
                        generator,
                        selector,
                        **kwargs))
        self.recency_list = deque()
        self.recency_list_size = recency_list_size
        self.restarted_last_check = False
        self.base_mutation_index = 0
        self.max_mutation_index = max_mutation_index
        
        # overload the variator and iterate method
        self.algorithm.variator = Multimethod(self, [
                GAOperator(SBX(), PM()),
                DifferentialEvolution(),
                UM(),
                PCX(),
                UNDX(),
                SPX()])
        
        self.algorithm.iterate = self.iterate
        
    def do_action(self):
        if self.check():
            if self.restarted_last_check:
                self.base_mutation_index = min(self.base_mutation_index+1,
                                               self.max_mutation_index)
                 
            # update the mutation probability prior to restart
            probability = self.base_mutation_index / float(self.max_mutation_index)
            probability = probability + (1.0 - probability)/self.algorithm.problem.nvars
            self.mutator.probability = probability
             
            self.restart()
            self.restarted_last_check = True
        else:
            if self.restarted_last_check:
                self.base_mutation_index = max(self.base_mutation_index-1, 0)
             
            self.restarted_last_check = False
        
    def iterate(self):
        if len(self.archive) <= 1:
            parents = self.selector.select(self.variator.arity, self.population)
        else:
            parents = self.selector.select(self.variator.arity-1, self.population) + [random.choice(self.archive)]
 
        random.shuffle(parents)
        
        children = self.variator.evolve(parents)
         
        self.algorithm.evaluate_all(children)
        self.nfe = self.algorithm.nfe
         
        for child in children:
            self._add_to_population(child)
             
            if self.archive.add(child):
                self.recency_list.append(child)
                  
                if len(self.recency_list) > self.recency_list_size:
                    self.recency_list.popleft()