from src.grasp import *
from src.tsp import *
import pandas as pd

if __name__ == "__main__":
    # Distance Matrix (17 cities,  optimal = 1922.33)
    matrix = pd.read_csv('datasets/dataset0.txt', sep = '\t') 
    matrix = matrix.values

    tsp = GraspTSP(matrix, 0.5)
    grasp = Grasp(tsp)

    best_solution = grasp.grasp(15, 15)

    print(best_solution)
