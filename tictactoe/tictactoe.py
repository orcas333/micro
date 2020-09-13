# Build a Two Player TicTacToe Game

# It needs to be able to accept input from the console

# It needs to be able to calculate whether there is a win
# It needs to be able to calculate show the board
# It needs to be able to keep track of the player

# Board
# -- stores a matrix of values containing 0 or 1
# Player
# Game

# User input check
# 1. Check valid integer input
# 2. Check that input spot is within bounds of the board
# 3. Check that there isn't a piece there already


class Game(object):
    def __init__(self, size):
        self.turn = 'X'
        self.board = Board(size, size)
        self.won = False

    def play(self):
        print("Welcome to TicTacToe!")
        self.board.print_board()

        while (not self.won):
            self.input_move()

        print(f"Player {self.turn} wins!")

    def alternate_turn(self):
        if self.turn == 'X':
            self.turn = 'O'
        else:
            self.turn = 'X'

    def accept_user_input(self):

        def user_input_validation(dimension):
            valid = False
            while not valid:
                try:
                    # Check that the input is an Integer. Reject all others.
                    input_val = int(input(f"{dimension}: "))

                    # Check that the input is within the bounds of the board
                    if input_val <= 0 or input_val > self.board.check_size():
                        print(
                            "Please input a position within the boundaries of the board")
                    else:
                        valid = True
                except:
                    print("Please enter an integer number row or column")

            return input_val

        # Check if the spot isn't currently occupied on the board
        valid_open_move = False
        while not valid_open_move:
            input_x = user_input_validation('Row')
            input_y = user_input_validation('Col')

            if not self.board.is_spot_occupied(input_x-1, input_y-1):
                valid_open_move = True
            else:
                print(
                    "That spot already has a piece in it. Please choose a different move.")

        return input_x, input_y

    def input_move(self):

        # Accept user input. Update the board state.
        print(f"Player {self.turn}, where would you like to go?")
        input_x, input_y = self.accept_user_input()
        self.board.update_board(self.turn, input_x - 1, input_y - 1)

        # Check whether someone has won. Then print the board.
        self.won = self.board.check_win(self.turn, input_x - 1, input_y - 1)
        self.board.print_board()

        # If nobody has won yet, alternate the turns
        if not self.won:
            self.alternate_turn()


class Board (object):
    def __init__(self, height, width):
        self.matrix = [['-'] * height for i in range(width)]
        self.board_state = {'row': {}, 'col': {}}
        self.init_board_state()

    def init_board_state(self):
        for i in range(len(self.matrix)):
            self.board_state["row"][i] = {'X': 0, 'O': 0}
            self.board_state["col"][i] = {'X': 0, 'O': 0}

    def is_valid_move(self, x, y):
        if self.matrix[x][y] == '-':
            return True
        else:
            return False

    def update_board(self, piece, x, y):
        if self.is_valid_move(x, y):
            self.matrix[x][y] = piece
            self.board_state['row'][x][piece] += 1
            self.board_state['col'][y][piece] += 1
        else:
            return False

    def is_spot_occupied(self, x, y):
        if self.matrix[x][y] == '-':
            return False
        else:
            return True

    def check_win(self, piece, x, y):
        if self.board_state["row"][x][piece] == len(self.matrix):
            return True
        elif self.board_state["col"][y][piece] == len(self.matrix):
            return True
        else:
            return False

    def print_board(self):
        for row in self.matrix:
            print(' | '.join(row))

    def check_size(self):
        return len(self.matrix)


if __name__ == "__main__":

    game = Game(3)
    game.play()
