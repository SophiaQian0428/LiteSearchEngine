import numpy as np
import math


def euclidean_distance_similarity(a: np.ndarray, b: np.ndarray) -> float:
    ed = np.linalg.norm(a - b)
    sim = 1 - 2/math.pi * math.atan(ed)
    # sim = 1 / (1 + ed)
    return sim


if __name__ == '__main__':
    a = np.array([3., 2., 1.])
    b = np.array([6., 4., 2.])
    print(euclidean_distance_similarity(a, b))
