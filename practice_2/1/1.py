import numpy as np
import json

matrix = np.load('matrix_66.npy')
matrix_dimension = len(matrix)
matrix_size = matrix.size
flip = np.fliplr(matrix)

matrix_sum = np.concatenate(matrix).sum()
matrix_average = matrix_sum / matrix_size
matrix_main_sum = matrix.trace()
matrix_main_average = matrix_main_sum / matrix_dimension
matrix_side_sum = flip.trace()
matrix_side_average = matrix_side_sum / matrix_dimension
matrix_max = matrix.max()
matrix_min = matrix.min()

matrix_stat = dict()
matrix_stat["sum"] = matrix_sum
matrix_stat["avr"] = matrix_average
matrix_stat["sumMD"] = matrix_main_sum
matrix_stat["avrMD"] = matrix_main_average
matrix_stat["sumSD"] = matrix_side_sum
matrix_stat["avrSD"] = matrix_side_average
matrix_stat["max"] = matrix_max
matrix_stat["min"] = matrix_min

for key, value in matrix_stat.items():
    matrix_stat[key] = float(value)

with open("matrix_stat_66.json", "w") as result:
    result.write(json.dumps(matrix_stat))

normalized_matrix = np.ndarray((matrix_dimension, matrix_dimension), dtype=float)
for i in range(0, matrix_dimension):
    for j in range(0, matrix_dimension):
        normalized_matrix[i][j] = matrix[i][j] / matrix_sum

np.save("normalized_matrix_66", normalized_matrix)
