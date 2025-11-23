from src.graspInterface import *
from scipy.optimize import minimize, Bounds
import numpy as np

class GraspFunctionMinimization(IMakeRCL, ILocalSearch, ISolution):
    def __init__(self, func, down_constraints, up_constraints, 
                 greediness_value = 0.8, random_rcl_size = 20, 
                 random_rcl_max_iteration = 1000, local_optimizer_method = 'trust-constr', 
                 epsilon = 1e-3, local_optimizer_max_iter = 1000):
        
        self.down_constraints = down_constraints
        self.up_constraints = up_constraints
        self.greediness_value = greediness_value
        self.func = func

        self.bounds_constraints = Bounds(down_constraints, up_constraints)
        self.local_optimizer_method = local_optimizer_method
        self.epsilon = epsilon
        self.local_optimizer_max_iter = local_optimizer_max_iter

        self.random_rcl_size = random_rcl_size
        self.random_rcl_max_iteration = random_rcl_max_iteration
    
    def make_rcl(self):
        n = len(self.down_constraints)
        
        rand = np.random.random()
        if rand <= self.greediness_value:
            random_point = self._get_random_point(n)
            random_rcl = [random_point]
            
            while len(random_rcl) < self.random_rcl_size:
                k = 0
                while self.func(random_point) >= self.func(random_rcl[-1]) and k < self.random_rcl_max_iteration:
                    random_point = self._get_random_point(n)
                    k += 1
                random_rcl.append(random_point)
            return random_rcl[-1]
        
        else:
            return self._get_random_point(n)

    def local_search(self, candidate):
        return minimize(self.func, 
                        candidate, 
                        method=self.local_optimizer_method, 
                        bounds=self.bounds_constraints, 
                        options={'gtol': 
                                 self.epsilon, 
                                 'maxiter': self.local_optimizer_max_iter,
                                 'verbose': 0})

    def btt(self, solution, best_solution):
        return solution.fun < best_solution.fun

    def log(self, iter, candidate, solution):
        print("=========================================================================================")
        print(f"Iteration {iter}\nRCL Candidate point: {candidate}\nPoint: {solution.x}\nValue: {solution.fun}")
        print("=========================================================================================")

    def _get_random_point(self, n):
        vector = np.zeros(n)
        for i in range(n):
            vector[i] = np.random.uniform(self.down_constraints[i], self.up_constraints[i])
        return vector