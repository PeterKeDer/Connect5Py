from Game import Game
from GameController import GameController
import GameIO

# # Use GameController to play in the command line
# controller = GameController()

# To train, probably directly use Game instance
# game = Game()
# game.print_board()
# game.place((7, 7), 1) # places 1 at (7, 7)
# if game.check_win(1):
#   # ...
#   pass
# game.place((8, 8), 2)
# if game.check_win(2):
#   # ...
#   pass
# # ...

# # Loading a Game instance from saved game_str
# game_str = '0 19 4 140 160 180 200' # this should be loaded from a saved file
# game = Game.load_from_str(game_str)
# game.print_board()
# ...

# Loading and saving games into a txt file using GameIO
# games = [
#     '0 19 4 140 160 180 200',
#     '0 19 5 140 160 180 200 300',
#     '0 15 4 120 160 180 190'
# ]
# for game_str in games:
#     GameIO.save_game(game_str)

# loaded_games = GameIO.load_games()
# for game_str in loaded_games:
#     game = Game.load_from_str(game_str)
#     # ... do stuffs with game
