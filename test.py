from src.grasp import *
from src.tsp import *
from src.functionminimization import *
from scipy import optimize
import math
import pandas as pd

if __name__ == "__main__":
    # Distance Matrix (17 cities,  optimal = 1922.33)
    matrix = pd.read_csv('datasets/dataset0.txt', sep = '\t') 
    matrix = matrix.values

    # tsp = GraspTSP(matrix, 0.5)
    # grasp = Grasp(tsp)
    # best_solution = grasp.grasp(5, 5, log=True)
    
    # print("Best solution:")
    # print(f"Best path: {best_solution[0]}")
    # print(f"Best distance {best_solution[1]}")

    func = lambda x: (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2
    down_constraints = [-5, -5]
    up_constraints = [5, 5]
    funcmin = GraspFunctionMinimization(func, down_constraints, up_constraints)
    grasp = Grasp(funcmin)
    best_solution = grasp.grasp(15, 15, log=True)
    # print("Best solution")
    # print(f"Minimum: {best_solution.x}\nValue: {best_solution.fun}")

    # func = lambda x: 100 * math.sqrt(abs(x[1] - 0.01 * x[0]**2)) + 0.01 * abs(x[0] + 10)
    # down_constraints = [-15, -3]
    # up_constraints = [-5, 3]
    # funcmin = GraspFunctionMinimization(func, down_constraints, up_constraints, random_rcl_size=30)
    # grasp = Grasp(funcmin)
    # best_solution = grasp.grasp(15, 15, True)
    # print("Best solution")
    # print(f"Minimum: {best_solution.x}\nValue: {best_solution.fun}")

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