
class Game:
    def __init__(self, board=None, dimensions=(19,19), side=1, moves=None):
        self.side = side
        if board:
            # initializing with board is not recommended unless if moves is also provided
            self.width = len(board[0])
            self.height = len(board)
            self.board = board
            self.moves = moves if moves else []
        else:
            self.width = dimensions[0]
            self.height = dimensions[1]
            self.init_board(dimensions)
            if moves:
                self.moves = moves
                current_side = 1
                for move in moves:
                    point = self.point_from_num(move)
                    self.place(point, current_side)
                    current_side = 2 if current_side == 1 else 1
            else:
                self.moves = []

    # Initializes a board (2d list)
    # with dimensions (width, height)
    def init_board(self, dimensions):
        self.board = []
        for _ in range(dimensions[1]):
            self.board.append([0] * dimensions[0])
    
    # Prints a formatted board
    def print_board(self):
        for row in self.board:
            print(' '.join(str(i) for i in row))
    
    # point: (x, y)
    def get_point(self, point):
        if self.point_is_valid(point):
            x, y = point
            return self.board[y][x]
        return -1

    # Set the point (x, y) to value
    def set_point(self, point, value):
        if self.point_is_valid(point):
            x, y = point
            self.board[y][x] = value
            return True
        return False
    
    # Places a piece at certain point, only if that point is empty
    # Also adds point num to moves
    def place(self, point, side):
        if self.get_point(point) == 0 and (side in [1,2]):
            if self.set_point(point, side):
                self.moves.append(self.point_num(point))
                return True
        return False
    
    # Returns whether the given point is within the board
    def point_is_valid(self, point):
        x, y = point
        return 0 <= y and y < self.height and 0 <= x and x < self.width

    # Checks whether the given side has won
    # TODO: Modify to return win coordinates
    def check_win(self, side=1):
        # Utility function used to check win
        # Iterates through points and checks if five in a row have value side
        # calc_point: lambda x,y,i: gets the point to check for given i
        def iter_points(x, y, calc_point):
            i = 0 # offset of point
            while self.get_point(calc_point(x, y, i)) == side:
                i += 1
                if i == 5:
                    return True
        
        for y in range(self.height):
            for x in range(self.width):
                # Horizontal
                if x+5 <= self.width:
                    if iter_points(x, y, lambda x, y, i: (x+i, y)):
                        return True
                # Vertical
                if y+5 <= self.height:
                    if iter_points(x, y, lambda x, y, i: (x, y+i)):
                        return True
                # Diagonal
                if x+5 <=self.width and y+5 <= self.height:
                    # top-left to bottom-right
                    if iter_points(x, y, lambda x, y, i: (x+i, y+i)):
                        return True
                    # bottom-left to top-right
                    if iter_points(x, y, lambda x, y, i: (x+i, y+4-i)):
                        return True
        return False

    def point_num(self, point):
        x, y = point
        return y * self.width + x

    def point_from_num(self, point_num):
        x = point_num % self.width
        y = int(point_num / self.width)
        return (x, y)

    # Outputs the current game state as a string to be saved
    # Format: win(0/1/2) width height len(moves) point1_num point2_num ...
    def game_str(self):
        win_str = '0'
        if self.check_win(1):
            win_str = '1'
        elif self.check_win(2):
            win_str = '2'
        moves_str = ' '.join(str(move) for move in self.moves)
        return ' '.join([win_str, str(self.width), str(self.height), str(len(self.moves)), moves_str])
    
    # Load from saved game_str using above method
    @staticmethod
    def load_from_str(game_str):
        data = game_str.split(' ')
        if len(data) < 4:
            return None
        width = int(data[1])
        height = int(data[2])
        moves = [int(move_str) for move_str in data[4:]]
        side = 1 if len(moves) % 2 == 0 else 2
        return Game(dimensions=(width, height), side=side, moves=moves)
