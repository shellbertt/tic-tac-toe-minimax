from math import inf as infinity
from random import choice
from random import seed as randomseed       # Paul Lu
import platform
import time
from os import system

"""
An implementation of Minimax AI Algorithm in Tic Tac Toe,
using Python.
This software is available under GPL license.
Author: Clederson Cruz
Year: 2017
License: GNU GENERAL PUBLIC LICENSE (GPL)

CMPUT 274, 2020 Fall Term, Weekly Exercise #6 Object Oriented Minimax, by:
Kaaden RumanCam
CCID: 1664694
"""


def clean():
    """
    Clears the console
    """
    # Paul Lu.  Do not clear screen to keep output human readable.
    print()
    return

    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


class C274:  # From Assignment #1
    def __init__(self):
        self.type = str(self.__class__)
        return

    def __str__(self):
        return(self.type)

    def __repr__(self):
        s = "<%d> %s" % (id(self), self.type)
        return(s)


class Tictactoe(C274):
    def __init__(self):
        super().__init__()
        self.HUMAN = -1
        self.COMP = +1
        self.board = Board(self.HUMAN, self.COMP)

    def play(self):
        # Paul Lu.  Set the seed to get deterministic behaviour for each run.
        #       Makes it easier for testing and tracing for understanding.
        randomseed(274 + 2020)

        clean()
        h_choice = ''  # X or O
        c_choice = ''  # X or O
        first = ''  # if human is the first

        # Human chooses X or O to play
        while h_choice != 'O' and h_choice != 'X':
            try:
                print('')
                h_choice = input('Choose X or O\nChosen: ').upper()
            except (EOFError, KeyboardInterrupt):
                print('Bye')
                exit()
            except (KeyError, ValueError):
                print('Bad choice')

        # Setting computer's choice
        if h_choice == 'X':
            c_choice = 'O'
        else:
            c_choice = 'X'

        # Human may starts first
        clean()
        while first != 'Y' and first != 'N':
            try:
                first = input('First to start?[y/n]: ').upper()
            except (EOFError, KeyboardInterrupt):
                print('Bye')
                exit()
            except (KeyError, ValueError):
                print('Bad choice')

        # Main loop of this game
        while len(self.board.empty_cells(self.board.get_board(
            ))) > 0 and not self.board.game_over(self.board.get_board()):

            if first == 'N':
                self.ai_turn(c_choice, h_choice)
                first = ''

            self.human_turn(c_choice, h_choice)
            self.ai_turn(c_choice, h_choice)

        # Game over message
        clean()
        if self.board.wins(self.board.get_board(), self.HUMAN):
            print(f'Human turn [{h_choice}]')
            self.board.render(self.board.get_board(), c_choice, h_choice)
            print('YOU WIN!')
        elif self.board.wins(self.board.get_board(), self.COMP):
            print(f'Computer turn [{c_choice}]')
            self.board.render(self.board.get_board(), c_choice, h_choice)
            print('YOU LOSE!')
        else:
            self.board.render(self.board.get_board(), c_choice, h_choice)
            print('DRAW!')

    def minimax(self, state, depth, player):
        """
        AI function that choice the best move
        :param state: current state of the board
        :param depth: node index in the tree (0 <= depth <= 9),
        but never nine in this case (see iaturn() function)
        :param player: an human or a computer
        :return: a list with [the best row, best col, best score]
        """
        if player == self.COMP:
            best = [-1, -1, -infinity]
        else:
            best = [-1, -1, +infinity]

        if depth == 0 or self.board.game_over(state):
            score = self.board.evaluate(state)
            return [-1, -1, score]

        for cell in self.board.empty_cells(state):
            x, y = cell[0], cell[1]
            state[x][y] = player
            score = self.minimax(state, depth - 1, -player)
            state[x][y] = 0
            score[0], score[1] = x, y

            if player == self.COMP:
                if score[2] > best[2]:
                    best = score  # max value
            elif score[2] < best[2]:
                    best = score  # min value

        return best

    def ai_turn(self, c_choice, h_choice):
        """
        It calls the minimax function if the depth < 9,
        else it choices a random coordinate.
        :param c_choice: computer's choice X or O
        :param h_choice: human's choice X or O
        :return:
        """
        depth = len(self.board.empty_cells(self.board.get_board()))
        if depth == 0 or self.board.game_over(self.board.get_board()):
            return

        clean()
        print(f'Computer turn [{c_choice}]')
        self.board.render(self.board.get_board(), c_choice, h_choice)

        if depth == 9:
            x = choice([0, 1, 2])
            y = choice([0, 1, 2])
        else:
            move = self.minimax(self.board.get_board(), depth, self.COMP)
            x, y = move[0], move[1]

        self.board.set_move(x, y, self.COMP)
        # Paul Lu.  Go full speed.
        # time.sleep(1)

    def human_turn(self, c_choice, h_choice):
        """
        The Human plays choosing a valid move.
        :param c_choice: computer's choice X or O
        :param h_choice: human's choice X or O
        :return:
        """
        depth = len(self.board.empty_cells(self.board.get_board()))
        if depth == 0 or self.board.game_over(self.board.get_board()):
            return

        # Dictionary of valid moves
        move = -1
        moves = {
            1: [0, 0], 2: [0, 1], 3: [0, 2],
            4: [1, 0], 5: [1, 1], 6: [1, 2],
            7: [2, 0], 8: [2, 1], 9: [2, 2],
        }

        clean()
        print(f'Human turn [{h_choice}]')
        self.board.render(self.board.get_board(), c_choice, h_choice)

        while move < 1 or move > 9:
            try:
                move = int(input('Use numpad (1..9): '))
                coord = moves[move]
                can_move = self.board.set_move(coord[0], coord[1], self.HUMAN)

                if not can_move:
                    print('Bad move')
                    move = -1
            except (EOFError, KeyboardInterrupt):
                print('Bye')
                exit()
            except (KeyError, ValueError):
                print('Bad choice')


class Board(C274):
    def __init__(self, human, comp):
        super().__init__()
        self.__board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        self.HUMAN = human
        self.COMP = comp

    def __str__(self, state, player1, player2):
        '''(Are docstrings necessary for these types of methods?)
        Returns string representation of the object
        player1: symbol representing first player.
        player2: symbol representing second player.
        state: optional board state
        '''
        '''Going with "Quantum Chris" for the adding arguments:
            https://stackoverflow.com/questions/40600268/how-do-i-use-repr-with-
            multiple-arguments#40600544
            Is Quantum Chris correct?
        '''
        chars = {
            -1: player2,
            +1: player1,
            0: ' '
        }
        str_line = '---------------'

        output = '\n' + str_line + '\n'
        for row in state:
            for cell in row:
                symbol = chars[cell]
                output += f'| {symbol} |'
            output += '\n' + str_line + '\n'
        return output

    def __repr__(self, state, player1, player2):
        '''Returns string representation of the object
        player1: symbol representing first player.
        player2: symbol representing second player.
        state: optional board state
        '''
        '''I'm not sure how to format below so it meets the line length
        requirement; suggestions?
        '''
        return self.__str__(player1, player2, state) + '\nHuman: ' + player2 + '\nComputer: ' + player1

    def get_board(self):
        """
        Gets the board.
        :return: An array representing the board.
        (Is a docstring necessary if the method is really simple?)
        """
        return self.__board

    def evaluate(self, state):
        """
        Function to heuristic evaluation of state.
        :param state: the state of the current board
        :return: +1 if the computer wins; -1 if the human wins; 0 draw
        """
        if self.wins(state, self.COMP):
            score = +1
        elif self.wins(state, self.HUMAN):
            score = -1
        else:
            score = 0

        return score

    def wins(self, state, player):
        """
        This function tests if a specific player wins. Possibilities:
        * Three rows    [X X X] or [O O O]
        * Three cols    [X X X] or [O O O]
        * Two diagonals [X X X] or [O O O]
        :param state: the state of the current board
        :param player: a human or a computer
        :return: True if the player wins
        """
        win_state = [
            [state[0][0], state[0][1], state[0][2]],
            [state[1][0], state[1][1], state[1][2]],
            [state[2][0], state[2][1], state[2][2]],
            [state[0][0], state[1][0], state[2][0]],
            [state[0][1], state[1][1], state[2][1]],
            [state[0][2], state[1][2], state[2][2]],
            [state[0][0], state[1][1], state[2][2]],
            [state[2][0], state[1][1], state[0][2]],
        ]
        if [player, player, player] in win_state:
            return True
        else:
            return False

    def game_over(self, state):
        """
        This function test if the human or computer wins
        :param state: the state of the current board
        :return: True if the human or computer wins
        """
        return self.wins(state, self.HUMAN) or self.wins(state, self.COMP)

    def empty_cells(self, state):
        """
        Each empty cell will be added into cells' list
        :param state: the state of the current board
        :return: a list of empty cells
        """
        cells = []

        for x, row in enumerate(state):
            for y, cell in enumerate(row):
                if cell == 0:
                    cells.append([x, y])

        return cells

    def valid_move(self, x, y):
        """
        A move is valid if the chosen cell is empty
        :param x: X coordinate
        :param y: Y coordinate
        :return: True if the board[x][y] is empty
        """
        if [x, y] in self.empty_cells(self.get_board()):
            return True
        else:
            return False

    def set_move(self, x, y, player):
        """
        Set the move on board, if the coordinates are valid
        :param x: X coordinate
        :param y: Y coordinate
        :param player: the current player
        """
        if self.valid_move(x, y):
            self.get_board()[x][y] = player
            return True
        else:
            return False

    def render(self, state, c_choice, h_choice):
        """
        Print the board on console
        :param state: current state of the board
        """
        print(self.__str__(state, c_choice, h_choice))


def main():
    """
    Main function that calls all functions
    """
    game = Tictactoe()
    game.play()


if __name__ == '__main__':
    main()
