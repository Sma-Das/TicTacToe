from os import system
from itertools import starmap
from math import inf
# from random import choice


class Board(object):
    def __init__(self, player1="X", player2="O"):
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        self.player1 = player1
        self.player2 = player2
        self.EMPTY = " "

    def print_board(self):
        system('clear')
        for r in range(3):
            for c in range(3):
                print({1: self.player1, 0: self.EMPTY, -1: self.player2}[self.board[r][c]], end=" ")
                if c < 2:
                    print("| ", end="")
            if r < 2:
                print("\n", "--+---+--", sep="")
        print()

    def make_move(self, row, column, val):
        self.board[row][column] = val

    def check_winner(self, player):
        for row, column in zip(self.rows, self.columns):
            if sum(row) == 3 * player:
                return True
            elif sum(column) == 3 * player:
                return True

        left_diag = sum(starmap(
            lambda i, x: x[i], enumerate(self.board)
        ))
        if left_diag == 3 * player:
            return True

        right_diag = sum(starmap(
            lambda i, x: x[-1-i], enumerate(self.board)
        ))
        if right_diag == 3 * player:
            return True

        return False

    def evaluate_state(self, player1=1, player2=-1, draw=0):
        if self.check_winner(player1):
            return player1
        elif self.check_winner(player2):
            return player2
        elif self.remaining == 0:
            return draw
        else:
            return

    @property
    def rows(self):
        yield from self.board

    @property
    def columns(self):
        yield from [[self.board[r][column] for r in range(3)] for column in range(3)]

    @property
    def remaining(self):
        return 9-sum(map(lambda x: x.count(1) + x.count(-1), self.board))

    def valid_cells(self):
        if self.remaining == 0:
            return []
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == 0:
                    yield r, c

    def __iter__(self):
        yield from self.board

    def __getitem__(self, pos):
        row, column = pos
        return self.board[row][column]

    def __setitem__(self, pos, val):
        row, column = pos
        self.board[row][column] = val


class TicTacToe(object):

    def __init__(self, player="X", computer="O"):
        self.board = Board(player, computer)
        self.player = 1
        self.computer = -1
        self.EMPTY = 0

    @property
    def remaining(self):
        return self.board.remaining

    def set_move(self, row, column, player):
        if self.board[row, column]:
            return
        else:
            self.board[row, column] = player
            return True

    def check_winner(self, player):
        for row, column in zip(self.board.rows, self.board.columns):
            if sum(row) == 3 * player:
                return True
            elif sum(column) == 3 * player:
                return True

        left_diag = sum(starmap(
            lambda i, x: x[i], enumerate(self.board)
        ))
        if left_diag == 3 * player:
            return True

        right_diag = sum(starmap(
            lambda i, x: x[-1-i], enumerate(self.board)
        ))
        if right_diag == 3 * player:
            return True

        return False

    def complete(self):
        return self.remaining == 0 or self.check_winner(self.player) or self.check_winner(self.computer)

    def player_move(self):
        move = input("Enter row, column separated by a comma: ")
        move = move.split(',')
        try:
            if len(move) != 2:
                raise Exception("Please give correct input")
            row, column = int(move[0]), int(move[1])
            if not (isinstance(row, int) or isinstance(column, int)):
                raise Exception("Please give correct input")
        except Exception as e:
            print(e)
            self.player_move()
        else:
            if not self.set_move(row-1, column-1, self.player):
                self.player_move()

    def eval(self, state):
        if self.check_winner(self.player):
            return 1
        elif self.check_winner(self.computer):
            return -1
        elif self.remaining == 0:
            return 0
        else:
            return False

    def mini_max(self, state, depth, player):
        best = [-1, -1, -inf]
        if player == self.computer:
            best = [-1, -1, inf]

        if depth == 0 or self.complete():
            return [-1, -1, self.eval(state)]

        for r, c in state.valid_cells():
            state[r, c] = player
            score = self.mini_max(state, depth-1, -player)
            state[r, c] = 0
            score[0], score[1] = r, c

            if player == self.computer:
                best = min(best, score, key=lambda x: x[2])
            else:
                best = max(best, score, key=lambda x: x[2])

        return best

    def minimax(self, state, turn=0):
        result = [(-1, -1), state.evaluate_state()]
        print(result, "PRERES")
        if result[1] is not None:
            print(result, "RES")
            return result
        player = 1 if turn % 2 == 0 else -1
        best = [(-1, -1), player * inf]
        print(best)
        for row, column in state.valid_cells():
            state[row, column] = player
            score = self.minimax(state, turn+1)
            state[row, column] = 0
            score[0] = (row, column)
            best = {self.computer: min(score, best, key=lambda x: x[1]),
                    self.player: max(score, best, key=lambda x: x[1]), }[player]
        return best

    def computer_move(self):
        if self.remaining == 0 or self.complete():
            return

        if self.remaining == 9:
            r, c = 0, 0
        else:
            r, c, _ = self.mini_max(self.board, self.remaining, self.computer)

        self.set_move(r, c, self.computer)

    def main_loop(self):
        try:
            player = input("Would you like to go first? (y/n) ").lower()

            if player not in ['y', 'n', 'q']:
                self.main_loop()
            elif player == 'q':
                quit()

            if player == 'n':
                self.player, self.computer = self.computer, self.player
                self.computer_move()

            self.board.print_board()
            while not self.complete():
                self.player_move()
                self.computer_move()
                self.board.print_board()

            message = {
                1: "Player won!",
                0: "Draw!",
                -1: "AI won!",
            }[self.eval(self.board)]
            print(message)
        except (EOFError, KeyboardInterrupt):
            print("\nYeet")
            exit()


if __name__ == '__main__':
    game = TicTacToe()
    game.main_loop()
