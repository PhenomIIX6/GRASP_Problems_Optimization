from src.graspInterface import *
import numpy as np
import copy

class GraspTSP(IMakeRCL, ILocalSearch, ISolution, ILog):    
    def __init__(self, matrix, greediness_value):
        self.matrix = matrix
        self.greediness_value = 1-greediness_value

    # RCL
    def construction(self):
        n = self.matrix.shape[0]
        seed = [[],float("inf")]

        # start from random point
        sequence = [np.random.randint(0, n)]
        
        # not visited point
        notvisited_mask = np.array([True]*n, dtype=bool)
        notvisited_mask[sequence[0]] = False

        for _ in range(1, n):
            distance_vector = self.matrix[:, sequence[-1]][notvisited_mask]
            sorted_indices = np.argsort(distance_vector)

            rcl_size = max(1, int(len(distance_vector) * self.greediness_value))
            rcl_indices = sorted_indices[:rcl_size]

            selected_index = np.random.choice(rcl_indices)
            selected_value = distance_vector[selected_index]

            next_city = np.where(self.matrix[:, sequence[-1]] == selected_value)[0][0]
    
            notvisited_mask[next_city] = False
            sequence.append(next_city)
        
        sequence.append(sequence[0])
        seed[0] = sequence
        seed[1] = self._distance_calc(self.matrix, seed) 
        
        return seed
    
    # Local search
    def local_search(self, candidate):
        tour = copy.deepcopy(candidate)
        
        improved = True
        while improved:
            improved = False
            for i in range(1, len(tour[0]) - 2):
                for j in range(i + 2, len(tour[0])):
                        
                    new_route = tour[0][:]
                    new_route[i:j] = new_route[i:j][::-1]
                    new_route[-1] = new_route[0]
                    
                    new_distance = self._distance_calc(self.matrix, [new_route, 0])
                    
                    if new_distance < tour[1]:
                        tour[0] = new_route
                        tour[1] = new_distance
                        improved = True
                        break
                if improved:
                    break
                    
        return tour
    
    # better than
    def btt(self, seed, other):
        return seed[1] < other[1]
    
    # Log
    def log(self, iter, candidate, solution):
        print("=========================================================================================")
        print(f"Iteration {iter}\nRCL Candidate path: {candidate[0]}\nRCL Candidate distance: {candidate[1]}\nPath: {solution[0]}\nDistance: {solution[1]}")
        print("=========================================================================================")

    # Distance calculate
    def _distance_calc(self, Xdata, city_tour):
        distance = 0
        for k in range(0, len(city_tour[0])-1):
            distance = distance + Xdata[city_tour[0][k]-1, city_tour[0][k+1]-1]            
        return distance
    
