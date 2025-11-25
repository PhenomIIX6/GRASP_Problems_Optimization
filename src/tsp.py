from src.graspInterface import *
import numpy as np
import copy

class GraspTSP(IMakeRCL, ILocalSearch, ISolution, ILog):    
    def __init__(self, matrix, greediness_value):
        self.matrix = matrix
        self.greediness_value = greediness_value

    # RCL
    def make_rcl(self):
        n = self.matrix.shape[0]
        seed = [[],float("inf")]
        
        # indexes
        indexes = np.array([i for i in range(0, n)])

        # start from random point
        sequence = [np.random.randint(0, n)]
        
        # not visited point
        notvisited_mask = np.array([True]*n, dtype=bool)
        notvisited_mask[sequence[0]] = False

        for i in range(1, n):
            rand = np.random.random()
            if rand <= self.greediness_value:
                next_city = self._get_min_point(self.matrix, notvisited_mask = notvisited_mask, city = sequence[-1])
            else:
                next_city = np.random.choice(indexes[notvisited_mask])

            notvisited_mask[next_city] = False
            sequence.append(next_city)
        
        sequence.append(sequence[0])
        seed[0] = sequence
        seed[1] = self._distance_calc(self.matrix, seed) 
        
        return seed
    
    # Local search
    def local_search(self, candidate):
        city_tour = self._two_opt(candidate)
        while (city_tour[0] != candidate[0]):
            candidate = copy.deepcopy(city_tour)
            city_tour = self._two_opt(candidate)
        return city_tour
    
    # better than
    def btt(self, seed, other):
        return seed[1] < other[1]
    
    # Log
    def log(self, iter, candidate, solution):
        print("=========================================================================================")
        print(f"Iteration {iter}\nRCL Candidate path: {candidate[0]}\nRCL Candidate distance: {candidate[1]}\nPath: {solution[0]}\nDistance: {solution[1]}")
        print("=========================================================================================")

    # 2 opt move 
    def _two_opt(self, city_tour):
        tour = copy.deepcopy(city_tour)
        best_route = copy.deepcopy(tour)
        seed = copy.deepcopy(tour)
        for i in range(0, len(tour[0]) - 2):
            for j in range(i+1, len(tour[0]) - 1):
                best_route[0][i:j+1] = list(reversed(best_route[0][i:j+1]))
                best_route[0][-1]  = best_route[0][0]
                best_route[1] = self._distance_calc(self.matrix, best_route)
                if (best_route[1] < tour[1]):
                    tour[1] = copy.deepcopy(best_route[1])
                    for n in range(0, len(tour[0])): 
                        tour[0][n] = best_route[0][n]
                best_route = copy.deepcopy(seed) 
        return tour
            
    # Nearest point with min distance
    def _get_min_point(self, Xdata, notvisited_mask, city):
        distance_vector = Xdata[:, city][notvisited_mask]
        return np.where(Xdata[:, city] == distance_vector.min())[0][0]
    
    # Distance calculate
    def _distance_calc(self, Xdata, city_tour):
        distance = 0
        for k in range(0, len(city_tour[0])-1):
            distance = distance + Xdata[city_tour[0][k]-1, city_tour[0][k+1]-1]            
        return distance
    
