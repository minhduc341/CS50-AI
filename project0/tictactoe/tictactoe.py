"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_X = 0
    count_O = 0

    for row in board:
        count_X += row.count(X)
        count_O += row.count(O)
    
    if count_X <= count_O:
        return X
    else: return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions =set()
    for row in range(3):
        for column in range(3):
            if board[row][column] == EMPTY:
                possible_actions.add((row,column))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    new_board = copy.deepcopy(board)

    if board[i][j] != None:
        raise Exception
    else:
        new_board[i][j] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #defined winning conditions
    win_conditions = [[(0, 0), (0, 1), (0, 2)],
                      [(1, 0), (1, 1), (1, 2)],
                      [(2, 0), (2, 1), (2, 2)],
                      [(0, 0), (1, 0), (2, 0)],
                      [(0, 1), (1, 1), (2, 1)],
                      [(0, 2), (1, 2), (2, 2)],
                      [(0, 0), (1, 1), (2, 2)],
                      [(0, 2), (1, 1), (2, 0)]]

    #Check if current board is combination of any of the defined winning conditions
    for condition in win_conditions:
        checks_X = 0
        checks_O = 0
        for i, j in condition:
            if board[i][j] == X:
                checks_X += 1
            if board[i][j] == O:
                checks_O += 1
        if checks_X == 3:
            return X
        if checks_O == 3:
            return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if (winner(board) != None) or (not actions(board)):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    # Optimization the first move for the Computer
    if board == initial_state():
        return 1, 1
    
    if player(board) == X:
        best_val = -math.inf
        # Look for the best action
        for action in actions(board):
            max_val = min_value(result(board, action))
            if max_val > best_val:
                best_val = max_val
                best_action = action
    
    elif player(board) == O:
        best_val = math.inf
        for action in actions(board):
            min_val = max_value(result(board, action)) 
            if min_val < best_val:
                best_val = min_val
                best_action = action

    return best_action 

def max_value(board):
    """
    Returns the maximum utility of the current board.
    """
    if terminal(board):
        return utility(board)
    value = -math.inf
    for action in actions(board):
        value = max(value, min_value(result(board,action)))
    return value

def min_value(board):
    """
    Returns the minimum utility of the current board.
    """
    if terminal(board):
        return utility(board)
    value = math.inf
    for action in actions(board):
        value = min(value, max_value(result(board,action)))
    return value
    

