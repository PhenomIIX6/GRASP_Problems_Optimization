from src.graspInterface import *
from scipy.optimize import minimize, Bounds
import numpy as np

class GraspFunctionMinimization(IMakeRCL, ILocalSearch, ISolution):
    def __init__(self, func, down_constraints, up_constraints, 
                 greediness_value = 0.8, random_rcl_size = 20, 
                 local_optimizer_method = 'trust-constr', 
                 epsilon = 1e-3, local_optimizer_max_iter = 1000):
        
        self.down_constraints = down_constraints
        self.up_constraints = up_constraints
        self.greediness_value = 1-greediness_value
        self.func = func

        self.bounds_constraints = Bounds(down_constraints, up_constraints)
        self.local_optimizer_method = local_optimizer_method
        self.epsilon = epsilon
        self.local_optimizer_max_iter = local_optimizer_max_iter

        self.random_rcl_size = random_rcl_size
    
    def construction(self):
        n = len(self.down_constraints)
        
        candidate_points = [self._get_random_point(n) for _ in range(self.random_rcl_size)]
        candidate_values = [self.func(point) for point in candidate_points]
        
        sorted_indices = np.argsort(candidate_values)
        
        rcl_size = max(1, int(len(candidate_points) * self.greediness_value))
        rcl_indices = sorted_indices[:rcl_size]
        
        selected_index = np.random.choice(rcl_indices)
        return candidate_points[selected_index]

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