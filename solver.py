from typing import List

import numpy as np


class Solver:

    def __init__(self,
                 min_temperature: float=0.01,
                 max_temperature: float=100,
                 alpha: float=0.98,
                 debug: bool=False):
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature
        self.alpha = alpha
        self.current_board = list(range(0, 8))
        self.debug = debug

    def solve(self):
        t, i = self.max_temperature, 0
        while t > self.min_temperature:

            random_board = self.get_change_board(self.current_board.copy())
            fit_random_board = self.get_valuation(random_board)
            fit_current_board = self.get_valuation(self.current_board)

            if fit_random_board == 0:
                self.current_board = random_board
                fit_current_board = fit_random_board
                break

            if fit_current_board > fit_random_board:
                self.current_board = random_board
            else:
                # calculate probability of change current board
                p = np.exp(-(fit_random_board - fit_current_board) * 100 / t)

                if p > np.random.random():
                    self.current_board = random_board
                t = self.alpha * t
            i += 1

        if self.debug:
            print(f'iteration = {i}, temperature = {t}, fitness function = {fit_current_board}')

        return self.visualization(self.current_board)

    @staticmethod
    def get_change_board(position: List[int]):
        i, j = np.random.choice(position, 2, False)
        position[i], position[j] = position[j], position[i]
        return position

    def get_valuation(self, position: List[int]):
        """
        Calculate fitness function
        :param position: list positions of queens
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
    s = Solver(debug=True)
    print(s.solve())
