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


###
# Computer Player
##
# Use Cases
# 1. Before the game, prompt whether human or computer
# 2. No user input for the computer, user should see themselves
# 3. No difficulty levels

##
import random


class Game(object):
    def __init__(self, size):
        self.turn = 'X'
        self.board = Board(size, size)
        self.game_end = False
        self.won = False
        self.stalemate = False
        self.bot = None

    def play(self):
        print("Welcome to TicTacToe!")
        print("------")
        self.board.print_board()

        # Prompt for player or computer
        bot_or_human_val = self.accept_user_input_bot_or_human()
        if bot_or_human_val == 2:
            self.bot = Bot(self.board.check_size())

        while (not self.game_end):
            self.move()

        if self.won == True:
            print(f"Player {self.turn} wins!")

        if self.stalemate == True and self.won == False:
            print(f"Stalemate! Nobody wins!")

    def alternate_turn(self):
        if self.turn == 'X':
            self.turn = 'O'
        else:
            self.turn = 'X'

    def accept_user_input_bot_or_human(self):
        # Prompt for player or computer
        print("Would you like to play against (1) another player or (2) computer?")

        valid = False
        while not valid:
            try:
                # Check that the input is an Integer. Reject all others.
                input_val = int(input(f"Please input 1 or 2: "))
                # Check that the input is within the bounds of the board
                if input_val not in [1, 2]:
                    print("Please enter an integer 1 or 2")
                else:
                    valid = True
            except:
                print("Please enter an integer 1 or 2")

        return input_val

    def accept_user_input_move(self, dimension):
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

    def prompt_human_for_input(self):
        # Check if the spot isn't currently occupied on the board
        valid_open_move = False
        while not valid_open_move:
            input_x = self.accept_user_input_move('Row')
            input_y = self.accept_user_input_move('Col')

            if not self.board.is_spot_occupied(input_x-1, input_y-1):
                valid_open_move = True
            else:
                print(
                    "That spot already has a piece in it. Please choose a different move.")

        return input_x, input_y

    def prompt_bot_for_input(self):
        valid_open_move = False
        while not valid_open_move:
            input_x, input_y = self.bot.make_move()
            print(
                f'The computer chooses to move to row: {input_x} and col: {input_y}')

            if not self.board.is_spot_occupied(input_x-1, input_y-1):
                valid_open_move = True
            else:
                print(
                    "That spot already has a piece in it. Please choose a different move.")

        return input_x, input_y

    def get_input_move(self):

        if self.bot == None:
            return self.prompt_human_for_input()

        else:
            if self.turn == 'O':
                return self.prompt_bot_for_input()
            elif self.turn == 'X':
                return self.prompt_human_for_input()

    def move(self):

        # Accept user input. Update the board state.
        print(f"Player {self.turn}, where would you like to go?")
        input_x, input_y = self.get_input_move()
        self.board.update_board(self.turn, input_x - 1, input_y - 1)

        # Check whether someone has won. Then print the board.
        self.board.print_board()

        # Check for end game conditions
        self.won = self.board.check_win(self.turn, input_x - 1, input_y - 1)
        if self.won:
            self.game_end = True

        self.stalemate = self.board.check_stalemate()

        if self.stalemate:
            self.game_end = True

        # If nobody has won yet, alternate the turns
        if not self.game_end:
            self.alternate_turn()


class Board (object):
    def __init__(self, height, width):
        self.matrix = [['-'] * height for i in range(width)]
        self.board_state = {'row': {},
                            'col': {},
                            'diag': None,
                            'diag_r': None,
                            'total_moves': 0}
        self.init_board_state()

    def init_board_state(self):
        for i in range(len(self.matrix)):
            self.board_state["row"][i] = {'X': 0, 'O': 0}
            self.board_state["col"][i] = {'X': 0, 'O': 0}

        self.board_state["diag"] = {'X': 0, 'O': 0}
        self.board_state["diag_r"] = {'X': 0, 'O': 0}

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
            if x == y:
                self.board_state["diag"][piece] += 1
            if x + y == len(self.matrix):
                self.board_state["diag_r"][piece] += 1

            self.board_state["total_moves"] += 1
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
        elif self.board_state["diag"][piece] == len(self.matrix):
            return True
        elif self.board_state["diag_r"][piece] == len(self.matrix):
            return True
        else:
            return False

    def check_stalemate(self):
        if self.board_state['total_moves'] >= (len(self.matrix) ** 2):
            return True
        else:
            return False

    def print_board(self):
        for row in self.matrix:
            print(' | '.join(row))

    def check_size(self):
        return len(self.matrix)


class Bot(object):
    def __init__(self, size):
        self.max = size

    def make_move(self):
        input_x = random.randint(1, self.max)
        input_y = random.randint(1, self.max)
        return input_x, input_y


if __name__ == "__main__":

    game = Game(3)
    game.play()
