"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None

board_version = []

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, X, EMPTY],
            [O, X, O],
            [EMPTY, X, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Count the number of X's and O's on the board
    x_count = 0
    o_count = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == X:
                x_count += 1
            elif board[row][col] == O:
                o_count += 1

    # Remember X is always the first player
    if not terminal(board):
        return X if x_count == 0 or x_count == o_count else O
    return None


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    all_actions = set()
    if not terminal(board): # game is in progress
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == EMPTY:
                    all_actions.add((row,col)) 

    return all_actions            


# actions function is needed
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    # remember to make a deep copy of board before going to the next change.
    """

    # deep copy the board before adding new action
    original_board = deepcopy(board)
    board_version.append(original_board)

    # udpate new action
    if action not in actions(board):
        raise ValueError(f"Invalid action: {action}")
    else:
        actions(board).remove(action)
        board[action[0]][action[1]] = player(board)

    return board

# result function is needed
def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Count the number of X's and O's on the board
    
    
    # if winner, else none
    # start to track from the last element of the board's result
    current_player = player(board)
    checking_player = O
    if current_player == O:
        checking_player = X

    board_size = len(board)
    if not terminal(board):
        # check the row
        for row in range(len(board)):
            if all(cell == potential_winner for cell in board[row]):
                return checking_player
        # check the column
        for col in range(len(board[0])): # only 3
            if all(board[row][col] == checking_player for row in range(board_size)):
                return checking_player
        # Check primary diagonal
        if all(board[i][i] == checking_player for i in range(board_size)):
            return checking_player
        # Check secondary diagonal
        if all(board[i][board_size - 1 - i] == checking_player for i in range(board_size)):
            return checking_player
        # Tie
        return None
    return None


    # raise NotImplementedError

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    return False #just to pass for testing other functions
    # raise NotImplementedError


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


# test functions
if __name__ == "__main__":
    # Test player
    board = initial_state()
    print(f"Current player: {player(board)}")
    
    # Test actions
    print(f"Possible actions: {actions(board)}")

    # Test result
    print(f"New board: {result(board, (1,1))}")
    print(f"Old board: {board_version}")
    print(f"Current board: {board}")

    
    # Test winner
    print(f"Winner: {winner(board)}")