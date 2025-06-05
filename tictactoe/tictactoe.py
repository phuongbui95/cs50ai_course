"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None

old_boards = []

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
    x_count = 0
    o_count = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == X:
                x_count += 1
            elif board[row][col] == O:
                o_count += 1

    # Remember X is always the first player
    return X if x_count == 0 or x_count == o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    all_actions = set()
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

    # udpate new action
    if action not in actions(board):
        raise ValueError(f"Invalid action: {action} is NOT EMPTY")

    # make a deep copy of the board first before making any changes.
    # deep copy the board to create a new board before adding new action to it
    new_board = deepcopy(board)
    new_board[action[0]][action[1]] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """      
    board_size = len(board)
    
    for player in [X, O]:
        # check rows
        for row in range(board_size):
            if all(cell == player for cell in board[row]):
                return player
                
        # check columns
        for col in range(board_size): 
            if all(board[row][col] == player for row in range(board_size)):
                return player
                
        # Check diagonals
        if all(board[i][i] == player for i in range(board_size)):
            return player
            
        if all(board[i][board_size - 1 - i] == player for i in range(board_size)):
            return player
            
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check for winner
    if winner(board) is not None:
        return True
        
    # Check whether board is full
    '''
    empty_count = 9
    for row in board:
        for cell in row:
            if cell is not EMPTY:
                empty_count -= 1
    if empty_count = 0:
        return True
    '''
    if all(cell is not EMPTY for row in board for cell in row):
        return True

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
    

# use recursive evaluation to check all steps ahead (not just 2 steps)
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    # This is the machine's turn
    """
    if terminal(board):
        return None

    current_player = player(board)
    
    def max_value(board):
        # condition to stop the recursion
        if terminal(board):
            return utility(board)
        ##
        v = float("-inf")
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
        return v

    def min_value(board):
        # condition to stop the recursion
        if terminal(board):
            return utility(board)
        ##
        v = float("inf")
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v

    possible_actions = actions(board)
    
    if current_player == X:
        # Maximizing player
        best_value = float("-inf")
        optimal_action = None
        for action in possible_actions:
            value = min_value(result(board, action))
            if value > best_value:
                best_value = value
                optimal_action = action
        return optimal_action
    else:
        # Minimizing player
        best_value = float("inf")
        optimal_action = None
        for action in possible_actions:
            value = max_value(result(board, action))
            if value < best_value:
                best_value = value
                optimal_action = action
        return optimal_action


# test functions
if __name__ == "__main__":  
    # Test player
    board = initial_state()
    print(f"Current player: {player(board)}")
    
    # Test actions
    # print(f"Possible actions: {actions(board)}")

    # Test result
    # print(f"New board: {result(board, (2,1))}") # done
    # print(f"Old board: {board_version}")
    # print(f"Current board: {board}")

    # Test winner
    # print(f"Winner: {winner(board)}")

    # Test terminal
    # print(f"Terminal: {terminal(board)}")

    # Test utility
    # print(f"Utility: {utility(board)}")

    # Test minimax
    # print(f"Minimax: {minimax(board)}")

    action = minimax(board)
    print(f"Optimal move: {action}")
    new_board = result(board, action)
    print("Resulting board:")
    for row in new_board:
        print(row)