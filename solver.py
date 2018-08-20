from typing import List

import numpy as np


class Solver:

    def __init__(self,
                 min_temperature: float=0,
                 max_temperature: float=100,
                 alpha: float=0.95,
                 max_iter: int=1000):
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature
        self.alpha = alpha
        self.current_board = list(range(0, 8))
        self.max_iter = max_iter

    def solve(self):
        t, i = self.max_temperature, 0
        while t > self.min_temperature and i < self.max_iter:

            random_board = self.get_change_board(self.current_board.copy())
            fit_random_board = self.get_valuation(random_board)
            fit_current_board = self.get_valuation(self.current_board)

            if fit_random_board == 0:
                self.current_board = random_board
                break

            if fit_current_board > fit_random_board:
                self.current_board = random_board
            else:
                p = np.exp(- (fit_random_board - fit_current_board) * 100 / t)

                if p > np.random.random():
                    self.current_board = random_board
                t = self.alpha * t
            i += 1
        return self.visualization(self.current_board)

    @staticmethod
    def get_change_board(position: List[int]):
        i, j = np.random.choice(position, 2, False)
        position[i], position[j] = position[j], position[i]
        return position

    def get_valuation(self, position: List[int]):
        """
        Calculate fitness function
        :param position: position of queens
        :return: int value of function
        """
        count = 0
        for index_queen_i in range(8):
            for index_queen_j in range(index_queen_i + 1, 8):
                if self.is_vertical_or_diagonal_wrong(position, index_queen_i, index_queen_j):
                    count += 1
        return count

    @staticmethod
    def is_vertical_or_diagonal_wrong(position, i, j):
        return (position[i] == position[j]) or (abs(i-j) == abs(position[i] - position[j]))

    @staticmethod
    def visualization(position: List[int]):
        return ''.join([''.join([' * ' * p, ' Q ', ' * ' * (7 - p), '\n']) for p in position])


if __name__ == '__main__':
    s = Solver(max_iter=100000, alpha=0.98)
    print(s.solve())
