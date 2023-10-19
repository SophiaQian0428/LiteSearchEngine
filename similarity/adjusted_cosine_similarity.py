import numpy as np

def adjusted_cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    mean_ab = np.mean(np.array([a, b]))
    a_ = a - mean_ab
    b_ = b - mean_ab
    return a_.dot(b_) / (np.linalg.norm(a_) * np.linalg.norm(b_))


if __name__ == '__main__':
    a = np.array([3., 2., 1.])
    b = np.array([6., 4., 2.])
    c = np.array([3., 2., 2.])
    print(adjusted_cosine_similarity(a, b))
    print(adjusted_cosine_similarity(a, c))
