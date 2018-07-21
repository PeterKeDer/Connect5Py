
class Game:
    def __init__(self, board=None, size=19, moves=None):
        if board:
            # initializing with board is not recommended unless if moves is also provided
            self.size = len(board)
            self.board = board
            self.moves = moves if moves else []
        else:
            self.size = size
            self.init_board(size)
            if moves:
                self.moves = moves
                current_side = 1
                for move in moves:
                    point = self.point_from_num(move)
                    self.place(point, current_side)
                    current_side = 2 if current_side == 1 else 1
            else:
                self.moves = []

    def init_board(self, size):
        """Initializes a board (2d list) with dimensions (width, height)"""
        self.board = []
        for _ in range(size):
            self.board.append([0] * size)

    def print_board(self):
        """Prints out a formatted board"""
        for row in self.board:
            print(' '.join(str(i) for i in row))

    def get_point(self, point):
        if self.point_is_valid(point):
            x, y = point
            return self.board[y][x]
        return -1

    def set_point(self, point, value):
        """Set the point (x, y) to value"""
        if self.point_is_valid(point):
            x, y = point
            self.board[y][x] = value
            return True
        return False

    def place(self, point, side):
        """Places a piece at certain point, only if that point is empty"""
        if self.get_point(point) == 0 and (side in [1, 2]):
            if self.set_point(point, side):
                self.moves.append(self.point_num(point))
                return True
        return False

    def point_is_valid(self, point):
        """Returns whether the given point is within the board"""
        x, y = point
        return 0 <= y < self.size and 0 <= x < self.size

    def check_game_status(self):
        """Checks the status of the game. -1: board filled. 0: nothing. 1/2: won"""
        # Check win
        if self.check_win(1):
            return 1
        if self.check_win(2):
            return 2
        # Check if board is full
        is_full = True
        for y in range(self.size):
            for x in range(self.size):
                if self.get_point((x, y)) == 0:
                    is_full = False
                    break
        if is_full:
            return -1
        return 0

    def check_win(self, side=1):
        """Checks whether the given side has won"""
        # Utility function used to check win
        # Iterates through points and checks if five in a row have value side
        # calc_point: lambda x,y,i: gets the point to check for given i
        def iter_points(x, y, calc_point):
            i = 0  # offset of point
            while self.get_point(calc_point(x, y, i)) == side:
                i += 1
                if i == 5:
                    return True

        for y in range(self.size):
            for x in range(self.size):
                # Horizontal
                if x + 5 <= self.size:
                    if iter_points(x, y, lambda x1, y1, i: (x1 + i, y1)):
                        return True
                # Vertical
                if y + 5 <= self.size:
                    if iter_points(x, y, lambda x1, y1, i: (x1, y1 + i)):
                        return True
                # Diagonal
                if x + 5 <= self.size and y + 5 <= self.size:
                    # top-left to bottom-right
                    if iter_points(x, y, lambda x1, y1, i: (x1 + i, y1 + i)):
                        return True
                    # bottom-left to top-right
                    if iter_points(x, y, lambda x1, y1, i: (x1 + i, y1 + 4 - i)):
                        return True
        return False

    def point_num(self, point):
        x, y = point
        return y * self.size + x

    def point_from_num(self, point_num):
        x = point_num % self.size
        y = int(point_num / self.size)
        return x, y

    def get_current_side(self):
        """Returns the current side (1 or 2)"""
        return 1 if len(self.moves) % 2 == 0 else 2

    def game_str(self):
        """
        Outputs the current game state as a string to be saved
        Format: win(0/1/2) size len(moves) point1_num point2_num ...
        """
        win_str = '0'
        if self.check_win(1):
            win_str = '1'
        elif self.check_win(2):
            win_str = '2'
        moves_str = ' '.join(str(move) for move in self.moves)
        return ' '.join([win_str, str(self.size), str(len(self.moves)), moves_str])

    @staticmethod
    def load_from_str(game_str):
        """Load from saved game_str"""
        data = game_str.split(' ')
        if len(data) < 4:
            return None
        size = int(data[1])
        moves = [int(move_str) for move_str in data[3:]]
        return Game(size=size, moves=moves)
