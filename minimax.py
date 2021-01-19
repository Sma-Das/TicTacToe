from math import inf
from dataclasses import dataclass
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


@dataclass
class Player:
    COMP: int = 1
    PLAYER: int = -1
    EMPTY: int = 0


def valid_cells(board):
    for row in range(3):
        for column in range(3):
            if board[row][column] == 0:
                yield row, column


def check_winner(state, player) -> bool:
    for row in state:
        if sum(row) == 3 * player:
            return True
    for row in range(3):
        if sum((state[column][row] for column in range(3))) == 3 * player:
            return True
    left, right = 0, 0
    for i in range(3):
        left += state[i][i]
        right += state[i][2-i]
    if left == 3 * player or right == 3 * player:
        return True
    return False


def evaluate_state(state, player1, player2, curr_play=None) -> Player:
    if check_winner(state, player1):
        return player1
    elif check_winner(state, player2):
        return player2
    elif any([Player.EMPTY not in row for row in state]):
        return Player.EMPTY
    elif not curr_play:
        return
    else:
        return -inf * curr_play


def minimax(state: list[list[int]], move=0) -> list:
    curr_play = Player.COMP if move % 2 == 0 else Player.PLAYER

    best_move = [(-1, -1), evaluate_state(state, Player.PLAYER, Player.COMP, curr_play)]

    for row, column in valid_cells(state):
        state[row][column] = curr_play
        score = [(row, column), minimax(state, move+1)[1]]
        state[row][column] = 0
        best_move = max(score, best_move, key=lambda x: x[1] * curr_play)

    return best_move


tempboard = [
    [1, -1, 1],
    [1, -1, 1],
    [0, 0, -1],
]
print(evaluate_state([[0, 1, 0], [-1, 1, 0], [-1, 1, 0]], Player.PLAYER, Player.COMP))
print(minimax(tempboard, 1))
