from Game import Game
from GameBot import GameBot


# Command line controller for Game
class GameController:
    def __init__(self, bot_init=None, bot_side=2):
        self.game = Game()
        self.current_side = 1

        if bot_init is not None:
            self.bot_init = bot_init
            self.bot_side = bot_side
            self.bot = bot_init(self.game, self.bot_side)

    def new_game(self, size):
        self.game = Game(size=size)
        self.current_side = 1

        if self.bot_init is not None:
            self.bot = self.bot_init(self.game, self.bot_side)

        self.start_game()
        
    def start_game(self):
        while True:
            self.game.print_board()
            point = self.get_input()
            while not self.game.place(point, self.current_side):
                print('Cannot place a piece there.')
                point = self.get_input()

            if self.bot is not None:
                self.bot.new_move(point, self.current_side)

            if self.game.check_win(self.current_side):
                self.game.print_board()
                print('Win: ' + str(self.current_side))
                break
            self.toggle_side()
            print('=' * (self.game.size * 2 - 1))
    
    def toggle_side(self):
        self.current_side = 2 if self.current_side == 1 else 1

    def get_input(self):
        if self.current_side != self.bot_side:
            print('Enter point (x and y separated by space)')
            user_input = input().split(' ')
            return int(user_input[0]), int(user_input[1])
        else:
            return self.bot.get_next_move()


if __name__ == '__main__':
    controller = GameController(bot_init=GameBot, bot_side=1)
    controller.new_game(size=15)
