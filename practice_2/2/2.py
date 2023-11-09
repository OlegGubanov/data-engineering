import numpy as np
import os

matrix = np.load("matrix_66_2.npy")
dimension = len(matrix)

x = list()
y = list()
z = list()
limit = 500 + 66

for i in range(dimension):
    for j in range(dimension):
        if matrix[i][j] > limit:
            x.append(i)
            y.append(j)
            z.append(matrix[i][j])

np.savez("points", x=x, y=y, z=z)
np.savez_compressed("points_compressed", x=x, y=y, z=z)

print(os.path.getsize("points.npz"))
print(os.path.getsize("points_compressed.npz"))
