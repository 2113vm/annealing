from typing import List

import numpy as np


class Solver:

    def __init__(self,
                 distance_matrix: np.ndarray,
                 min_temperature: float=0.01,
                 max_temperature: float=100,
                 alpha: float=0.98,
                 debug: bool=False):
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature
        self.alpha = alpha
        self.debug = debug
        self.current_path = list(range(distance_matrix.shape[0]))
        self.distance_matrix = distance_matrix

    def solve(self):
        t, i = self.max_temperature, 0
        while t > self.min_temperature:

            random_path = self.get_change_path(self.current_path.copy())
            fit_random_path = self.get_valuation(random_path)
            fit_current_path = self.get_valuation(self.current_path)

            if fit_current_path > fit_random_path:
                self.current_path = random_path
            else:
                # calculate probability of change current board
                p = np.exp(-(fit_random_path - fit_current_path) * 100 / t)

                if p > np.random.random():
                    self.current_path = random_path
                t = self.alpha * t
            i += 1

        if self.debug:
            print(f'iteration = {i}, temperature = {t}, fitness function = {fit_current_path}')

        return self.current_path

    def get_valuation(self, path: List[int]):
        """
        Calculate valuation of path
        :param path:
        :param distance_matrix:
        :return: sum distance for path
        """
        return sum(self.distance_matrix[path[index_vertex], path[index_vertex - 1]]
                   for index_vertex in range(len(path)))

    @staticmethod
    def get_change_path(path: List[int]):
        i, j = np.random.choice(path, 2, False)
        path[i], path[j] = path[j], path[i]
        return path


if __name__ == '__main__':

    # best solution 1 -> 3 -> 5 -> 2 -> 4 -> 1 => sum_path = 5
    distance_matrix = np.array([[0, 5, 1, 1, 5],
                                [5, 0, 5, 1, 1],
                                [1, 5, 0, 5, 1],
                                [1, 1, 5, 0, 5],
                                [5, 1, 1, 5, 0]])

    s = Solver(distance_matrix=distance_matrix, debug=True)
    print(s.solve())
