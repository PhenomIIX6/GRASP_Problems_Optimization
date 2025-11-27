import numpy as np
import random

class Grasp():
    def __init__(self, grasp_class):
        self.grasp_class = grasp_class

    def grasp(self, max_iteration, log=False):
        count_iteration = 0
        best_solution = 0
        first_solution = True
        
        while (count_iteration < max_iteration): 
            # Phase 1: Construction
            candidate = self.grasp_class.construction()

            # Phase 2: Local search
            solution = self.grasp_class.local_search(candidate)

            if first_solution:
                best_solution = solution
                first_solution = False
            elif self.grasp_class.btt(solution, best_solution):
                best_solution = solution
            
            count_iteration += 1
            if log:
                self.grasp_class.log(count_iteration, candidate, solution)

        return best_solution