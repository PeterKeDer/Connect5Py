
filename = 'GameData.txt'


# Returns list of game_str saved in file
def load_games():
    f = open(filename, 'r')
    lines = f.read().splitlines()
    f.close()
    return lines


def save_game(game_str):
    f = open(filename, 'a')
    f.write(game_str + '\n')
    f.close()
