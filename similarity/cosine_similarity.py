import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return a.dot(b) / (np.linalg.norm(a) * np.linalg.norm(b))


if __name__ == '__main__':
    a = np.array([3., 2., 1.])
    b = np.array([6., 4., 2.])
    c = np.array([3., 2., 2.])
    print(cosine_similarity(a, b))
    print(cosine_similarity(a, c))
