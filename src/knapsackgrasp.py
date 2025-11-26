from src.graspInterface import *
import numpy as np
import random

class GraspKnapsack(IMakeRCL, ILocalSearch, ISolution, ILog):
    def __init__(self, ids, values, weights, capacity, n, greediness_value=0.5):
        self.ids = ids
        self.values = values
        self.weights = weights
        self.capacity = capacity
        self.n = n
        self.greediness_value = greediness_value

    def make_rcl(self):
        remaining_capacity = self.capacity
        solution = [0] * self.n
        available_items = list(range(self.n))
        
        ratios = [self.values[i] / self.weights[i] for i in range(self.n)]
        
        while available_items and remaining_capacity > 0:
            feasible_items = [i for i in available_items if self.weights[i] <= remaining_capacity]
            
            if not feasible_items:
                break
                
            feasible_items.sort(key=lambda i: ratios[i], reverse=True)
            
            rcl_size = max(1, int(len(feasible_items) * self.greediness_value))
            rcl = feasible_items[:rcl_size]
            
            selected_item = random.choice(rcl)
            
            solution[selected_item] = 1
            remaining_capacity -= self.weights[selected_item]
            available_items.remove(selected_item)
        
        return solution

    def local_search(self, candidate):
        return self._local_search_impl(candidate, self.weights, self.values, self.ids, self.capacity)
    
    def _local_search_impl(self, solution, weight, value, id, capacity):
        temp = solution[:]
        for i in range(len(temp)):
            max_temp_weight = 0
            max_value_temp = 0
            max_value = 0
            
            if temp[i] == 0:
                temp[i] = 1
                for j in range(len(temp)):
                    if temp[j] == 1:
                        max_value_temp += value[id[j]]
                        max_temp_weight += weight[id[j]]
                temp[i] = 0
            elif temp[i] == 1:
                temp[i] = 0
                max_value_temp = 0
                max_value = 0
                for j in range(len(temp)):
                    if temp[j] == 1:
                        max_value_temp += value[id[j]]
                        max_temp_weight += weight[id[j]]
                temp[i] = 1
            
            for j in range(len(solution)):
                if solution[j] == 1:
                    max_value += value[id[j]]
            
            if capacity - max_temp_weight >= 0 and max_value_temp > max_value:
                solution = temp[:]

        return solution

    def btt(self, solution, best_solution):
        return self._calculate_value(solution) > self._calculate_value(best_solution)

    def log(self, iter, candidate, solution):
        print("=========================================================================================")
        print(f"Iteration {iter}")
        print(f"RCL Candidate solution: {[self.ids[i] for i in range(self.n) if candidate[i] == 1]}")
        print(f"RCL Candidate value: {self._calculate_value(candidate)}")
        print(f"Solution: {[self.ids[i] for i in range(self.n) if solution[i] == 1]}")
        print(f"Value: {self._calculate_value(solution)}")
        print(f"Weight: {self._calculate_weight(solution)}")
        print("=========================================================================================")

    def _calculate_value(self, solution):
        return sum(self.values[i] for i in range(self.n) if solution[i] == 1)

    def _calculate_weight(self, solution):
        return sum(self.weights[i] for i in range(self.n) if solution[i] == 1)
