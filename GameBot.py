import random
import math
import numpy as np

from Game import Game


class GameBot:
    """Simple AI for Connect5. Moves are entirely dependent on current state of the board"""

    def __init__(self, game, side):
        self.game = game
        self.side = side

        # Init win conditions
        # Each individual element in win_conditions represents number of pieces of side occupied for
        #   a certain "win condition" (5 consecutive pieces)
        # If that win condition contains pieces of other side (not possible to win), it will be -1
        # To access win conditions for (x, y), use win_conditions[x][y][n]
        #   where n is the orientation (0 ~ 3)
        # Orientations: 0 - horizontal, 1 - SE, 2 - vertical, 3 - SW
        shape = game.size, game.size, 4  # 4 different orientations
        self.win_conditions = np.zeros(shape, dtype=int)
        self.lose_conditions = np.zeros(shape, dtype=int)  # for opponent
        self.init_conditions()

    def init_conditions(self):
        # Set all unreachable conditions (on edge) to -1
        for x in range(self.game.size - 4, self.game.size):
            for y in range(self.game.size):
                self.win_conditions[x][y][0] = -1
                self.win_conditions[x][y][1] = -1
                self.lose_conditions[x][y][0] = -1
                self.lose_conditions[x][y][1] = -1

        for y in range(self.game.size - 4, self.game.size):
            for x in range(self.game.size):
                self.win_conditions[x][y][1] = -1
                self.win_conditions[x][y][2] = -1
                self.win_conditions[x][y][3] = -1
                self.lose_conditions[x][y][1] = -1
                self.lose_conditions[x][y][2] = -1
                self.lose_conditions[x][y][3] = -1

        for x in range(4):
            for y in range(self.game.size):
                self.win_conditions[x][y][3] = -1
                self.lose_conditions[x][y][3] = -1

        # Set up conditions for existing moves on board
        if len(self.game.moves) == 0:
            # No moves are currently on board
            return
        for y in range(self.game.size):
            for x in range(self.game.size):
                value = self.game.get_point((x, y))
                if value == 0:
                    continue
                elif value == self.side:
                    # Increment all conditions affected by this move by 1, and set lose to -1
                    for x1, y1, n in self.get_affected_conditions((x, y)):
                        if self.win_conditions[x1][y1][n] != -1:
                            self.win_conditions[x1][y1][n] += 1
                        self.lose_conditions[x1][y1][n] = -1
                else:
                    # Set all conditions affected to -1, and increment lose condition
                    for x1, y1, n in self.get_affected_conditions((x, y)):
                        self.win_conditions[x1][y1][n] = -1
                        if self.lose_conditions[x1][y1][n] != -1:
                            self.lose_conditions[x1][y1][n] += 1

    def get_affected_conditions(self, point):
        """Returns an array of the win conditions (x, y, n) affected by point"""
        x, y = point
        affected = []

        # Min / max offset available for x, y
        x_min_offset = max(0, 5 - (self.game.size - x))
        x_max_offset = min(4, x)
        y_min_offset = max(0, 5 - (self.game.size - y))
        y_max_offset = min(4, y)

        # Horizontal
        for offset in range(x_min_offset, x_max_offset + 1):
            affected.append((x - offset, y, 0))
        # South East
        for offset in range(max(x_min_offset, y_min_offset), min(x_max_offset, y_max_offset) + 1):
            affected.append((x - offset, y - offset, 1))
        # Vertical
        for offset in range(y_min_offset, y_max_offset + 1):
            affected.append((x, y - offset, 2))
        # South West
        for offset in range(max(4 - x_max_offset, y_min_offset), min(4 - x_min_offset, y_max_offset) + 1):
            affected.append((x + offset, y - offset, 3))
        return affected

    def new_move(self, point, side):
        """Updates win and lose conditions with latest move"""
        for x, y, n in self.get_affected_conditions(point):
            if side == self.side:
                if self.win_conditions[x][y][n] != -1:
                    self.win_conditions[x][y][n] += 1
                self.lose_conditions[x][y][n] = -1
            else:
                if self.lose_conditions[x][y][n] != -1:
                    self.lose_conditions[x][y][n] += 1
                self.win_conditions[x][y][n] = -1

    def get_next_move(self):
        """Returns (x, y) for next move, or None if not bot's turn"""
        if self.side != self.game.get_current_side():
            return None

        best_points = []
        highest = 0
        for y in range(self.game.size):
            for x in range(self.game.size):
                if self.game.get_point((x, y)) == 0:
                    # Point is blank - can place
                    score = self.get_score((x, y))
                    if score > highest:
                        highest = score
                        best_points = [(x, y)]
                    elif score == highest:
                        best_points.append((x, y))

        if len(best_points) == 0:
            return None  # no points

        return random.choice(best_points)

    def get_score(self, point):
        """Returns score of given point (x, y). Higher the better"""
        win_scores = [0, 10, 50, 200, 1000, math.inf]
        lose_scores = [0, 10, 50, 200, 1000, 10000]
        score = 0
        for x, y, n in self.get_affected_conditions(point):
            score += win_scores[self.win_conditions[x][y][n] + 1]
            score += lose_scores[self.lose_conditions[x][y][n] + 1]
        return score


def main():
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 2, 2, 2, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    bot = GameBot(Game(board=board, moves=[1, 1]), 1)
    print(bot.get_next_move())


if __name__ == '__main__':
    main()
