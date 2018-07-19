from tkinter import *

from Game import Game
from GameBot import GameBot

# Graphic Constants
canvas_size = 600
panel_height = 100
line_width = 1
piece_size = 0.8  # compared to calculated line_space

board_color = '#dddddd'
line_color = 'black'
piece1_color = 'black'
piece2_color = 'white'


class GameWindow(Frame):
    def __init__(self, master=None, play_bot=False, bot_init=None):
        """
        bot_init: lambda game, side: SomeBot()
        Bot requirements:
            .get_next_move() -> (x, y)  # computes next move
            .new_move(point, side)  # indicates a piece was placed
            .side: int  # 1 or 2
        """

        Frame.__init__(self, master)

        # Configure master widget
        self.master = master
        self.master.title('Connect 5')

        # Init canvas
        self.canvas = Canvas(self, width=canvas_size, height=canvas_size, bg=board_color)
        self.canvas.bind('<Button-1>', self.click_handler)  # binds click event to handler
        self.canvas.pack()

        # Init panel label
        self.panel_label = Label(self, text='Hello!', font=('Arial', 36))
        self.panel_label.pack()

        # Init restart button
        restart_button = Button(self, text='Restart', padx=10, pady=6, command=lambda: self.new_game())
        restart_button.pack()

        # Init computed canvas data
        self.board_size = 0
        self.line_space = 0

        # Init game logic
        self.current_side = 1
        self.game_status = 0
        self.game = Game()

        # Init bot
        if bot_init and play_bot:
            self.play_bot = True
            self.bot_init = bot_init
            self.bot = bot_init(self.game, 2)
        else:
            self.play_bot = False

        # Start new game
        self.new_game()

        # Finish init
        self.pack(fill=BOTH, expand=1)

    def new_game(self, game=None):
        """Starts new game or load game"""
        if game:
            self.game = game
        else:
            self.game = Game()
            if self.play_bot:
                self.bot = self.bot_init(self.game, 2)

        # Updates game logic
        self.current_side = 1 if len(self.game.moves) % 2 == 0 else 2
        self.game_status = self.game.check_game_status()  # should be 0

        # Compute canvas data
        self.board_size = self.game.size
        self.line_space = (canvas_size - self.game.size * line_width) / (self.board_size + 1)

        # Draw
        self.canvas.delete(ALL)
        self.draw_lines()
        self.draw_pieces()
        self.update_panel()

    def draw_lines(self):
        """Draw board lines"""
        for i in range(self.board_size):
            distance = (self.line_space + line_width) * i + self.line_space  # distance from line to board edge

            self.canvas.create_line(self.line_space, distance, canvas_size - self.line_space, distance, fill=line_color)
            self.canvas.create_line(distance, self.line_space, distance, canvas_size - self.line_space, fill=line_color)

    def draw_pieces(self):
        """Draw board pieces, if any exist"""
        for i in range(len(self.game.moves)):
            point = self.game.point_from_num(self.game.moves[i])
            side = 1 if i % 2 == 0 else 2
            self.draw_piece(point, side)

    def draw_piece(self, point, side):
        """Draws a piece on canvas"""
        board_x, board_y = point
        # x, y are the center of the circle
        x = board_x * (self.line_space + line_width) + self.line_space
        y = board_y * (self.line_space + line_width) + self.line_space

        o = (piece_size / 2) * self.line_space  # offset from center of circle to edge
        color = piece1_color if side == 1 else piece2_color
        self.canvas.create_oval(x - o, y - o, x + o, y + o, fill=color, outline=color)

    def place_piece(self, point):
        """Places a piece on the board and also the game. Returns False if unable to place at point"""
        if self.game.place(point, self.current_side):
            self.draw_piece(point, self.current_side)  # draws piece on canvas

            # Update bot conditions if necessary
            if self.play_bot:
                self.bot.new_move(point, self.current_side)

            # Check whether game is finished
            self.game_status = self.game.check_game_status()
            if self.game_status == 0:
                # Continues game
                self.current_side = 1 if self.current_side == 2 else 2  # toggles side
                self.update_panel()

                # Get bot move and update if necessary
                if self.play_bot and self.current_side == self.bot.side:
                    next_point = self.bot.get_next_move()
                    self.place_piece(next_point)

            else:
                self.finished()

            return True
        else:
            return False

    def click_handler(self, event):
        """Handles click event on canvas"""
        if self.game_status == 0 and 0 <= event.x <= canvas_size and 0 <= event.y <= canvas_size:
            # Compute board_x and board_y
            board_x = int((event.x - self.line_space) / (self.line_space + line_width) + 0.5)
            board_y = int((event.y - self.line_space) / (self.line_space + line_width) + 0.5)
            self.place_piece((board_x, board_y))

    def update_panel(self):
        """Updates the panel text based on status"""
        if self.game_status == -1:
            # Board full - tie
            self.panel_label.config(text='Tie')
        elif self.game_status == 1:
            self.panel_label.config(text='Player 1 Wins')
        elif self.game_status == 2:
            self.panel_label.config(text='Player 2 Wins')
        else:
            if self.current_side == 1:
                self.panel_label.config(text='Next Turn: Player 1')
            else:
                self.panel_label.config(text='Next Turn: Player 2')

    def finished(self):
        """Called when game is finished"""
        self.update_panel()


def main():
    root = Tk()
    geometry = str(canvas_size) + 'x' + str(canvas_size + panel_height)
    root.geometry(geometry)

    app = GameWindow(root, play_bot=True, bot_init=GameBot)

    root.mainloop()


if __name__ == '__main__':
    main()
