from Game import Game


# Command line controller for Game
class GameController:
    def __init__(self):
        self.game = Game()
        self.current_side = 1
        self.new_game()

    def new_game(self, size):
        self.game = Game(size=size)
        self.current_side = 1
        self.start_game()
        
    def start_game(self):
        while True:
            self.game.print_board()
            point = self.get_input()
            while not self.game.place(point, self.current_side):
                print('Cannot place a piece there.')
                point = self.get_input()
            if self.game.check_win(self.current_side):
                self.game.print_board()
                print('Win: ' + str(self.current_side))
                break
            self.toggle_side()
            print(self.game.game_str())
    
    def toggle_side(self):
        self.current_side = 2 if self.current_side == 1 else 1

    def get_input(self):
        print('Enter point (x and y separated by space)')
        user_input = input().split(' ')
        return int(user_input[0]), int(user_input[1])
