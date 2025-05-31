"""
Tic Tac Toe Player
"""

import math

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
    # Count the number of X's and O's on the board
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    
    # Remember X is always the first player
    if terminal(board) == False: # game is NOT over
        return X if x_count == 0 or x_count == o_count else return O
    
    return
    # raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    available_actions = set()
    if terminal(board) == False: # game is in progress
        for i,j in enumerate(board):
            available_actions.add((i,j)) if board[i][j] == EMPTY

    return available_actions            
    # raise NotImplementedError


# actions function is needed
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    # remember to make a deep copy of board before going to the next change.
    """

    # deep copy the board before adding new action

    # udpate new action = the last element of the actions set

    raise NotImplementedError

# result function is needed
def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Count the number of X's and O's on the board
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    empty_count = sum(row.count(EMPTY) for row in board)
    
    # if winner, else none
    # X is the winner (x_count>=3)
    # O is the winner (o_count>=3)


    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    # This is the machine's turn
    """
    raise NotImplementedError
