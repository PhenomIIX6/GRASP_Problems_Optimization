from src.grasp import *
from src.tsp import *
from src.functionminimization import *
from src.knapsackgrasp import *
from scipy import optimize
import math
import pandas as pd
import csv

def csv_parser_knapsack(filename): 
    with open(f"{filename}", "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        
        weight = []
        value = []
        id = []
        n = int()
        capacity = int()
        
        i = 0
        for row in csv_reader:
            i += 1
            if not row:
                continue
                
            if i == 1:
                n = int(row[0])
            elif 1 < i <= n + 1:
                id.append(int(row[0]) - 1)
                value.append(int(row[1]))
                weight.append(int(row[2]))
            else:
                capacity = int(row[0])

    return id, value, weight, capacity, n

def build_distance_matrix(coordinates):
   a = coordinates
   b = a.reshape(np.prod(a.shape[:-1]), 1, a.shape[-1])
   return np.sqrt(np.einsum('ijk,ijk->ij',  b - a,  b - a)).squeeze()

if __name__ == "__main__":
    # 17 cities,  optimal = 1922.33
    # matrix = pd.read_csv('datasets/tsp_dataset0.txt', sep = '\t') 
    # matrix = matrix.values
    # tsp = GraspTSP(matrix, 0.5)
    # grasp = Grasp(tsp)
    # best_solution = grasp.grasp(5, log=True)
    # print("Best solution:")
    # print(f"Best path: {best_solution[0]}")
    # print(f"Best distance {best_solution[1]}")

    # 51 cities, optimal ~ around 7500
    # matrix = pd.read_csv('datasets/tsp_dataset1.txt', sep = '\t')
    # matrix = matrix.values
    # matrix = build_distance_matrix(matrix)
    # tsp = GraspTSP(matrix, 0.8)
    # grasp = Grasp(tsp)
    # best_solution = grasp.grasp(100, log=True)
    # print("Best solution:")
    # print(f"Best path: {best_solution[0]}")
    # print(f"Best distance {best_solution[1]}")

    # Rozenbrok function, minimum in [1, 1]
    # func = lambda x: (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2
    # down_constraints = [-5, -5]
    # up_constraints = [5, 5]
    # funcmin = GraspFunctionMinimization(func, down_constraints, up_constraints)
    # grasp = Grasp(funcmin)
    # best_solution = grasp.grasp(15, log=True)
    # print("Best solution")
    # print(f"Minimum: {best_solution.x}\nValue: {best_solution.fun}")

    # Bukin N6 function, minimum in [-10, -1]  
    func = lambda x: 100 * math.sqrt(abs(x[1] - 0.01 * x[0]**2)) + 0.01 * abs(x[0] + 10)
    down_constraints = [-15, -3]
    up_constraints = [-5, 3]
    funcmin = GraspFunctionMinimization(func, down_constraints, up_constraints, random_rcl_size=30)
    grasp = Grasp(funcmin)
    best_solution = grasp.grasp(15, log=True)
    print("Best solution")
    print(f"Minimum: {best_solution.x}\nValue: {best_solution.fun}")

    # Bukin N6 function using scipy optimize
    # down_constraints = [-15, -3]
    # up_constraints = [-5, 3]
    # bounds_constraints = Bounds(down_constraints, up_constraints)
    # a = minimize(func, [-3, -3], 
    #          method='trust-constr', 
    #          bounds=bounds_constraints, 
    #          options={  'gtol': 1e-4, 
    #                     'maxiter': 1000,
    #                     'verbose': 0})
    # print(a.x)

    # Knapsack problem with 20 items, answer is 31621
    # id, value, weight, capacity, n = csv_parser_knapsack('datasets/knapsack_dataset0.csv')
    # knapsack = GraspKnapsack(id, value, weight, capacity, n, greediness_value=0.4)
    # grasp = Grasp(knapsack)
    # result = grasp.grasp(max_iteration=10, log=True)    
    # print("Best knapsack solution:")
    # print(f"Selected items: {[id[i] for i in range(n) if result[i] == 1]}")
    # print(f"Total value: {knapsack._calculate_value(result)}")
    # print(f"Total weight: {knapsack._calculate_weight(result)}")
    # print(f"Capacity: {capacity}")

    # Knapsack problem with 10000 items, answer is 49885
    # id, value, weight, capacity, n = csv_parser_knapsack('datasets/knapsack_dataset1.csv')
    # knapsack = GraspKnapsack(id, value, weight, capacity, n, greediness_value=0.4)
    # grasp = Grasp(knapsack)
    # result = grasp.grasp(max_iteration=20, log=True)
    # print("Best knapsack solution:")
    # print(f"Selected items: {[id[i] for i in range(n) if result[i] == 1]}")
    # print(f"Total value: {knapsack._calculate_value(result)}")
    # print(f"Total weight: {knapsack._calculate_weight(result)}")
    # print(f"Capacity: {capacity}")