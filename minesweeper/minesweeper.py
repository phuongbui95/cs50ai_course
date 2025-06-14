import itertools # https://docs.python.org/3/library/itertools.html
import random

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8): # if not inputting height, width, mines, automatically use 8,8,8

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False) # return boolean
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines: # self.mines is a set of value, # mines is a number
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]: # if False
                self.mines.add((i, j))
                self.board[i][j] = True # return another boolean value

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    # compare 2 objects then return a boolean value
    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    # under what circumstances do you know for sure that a sentence’s cells are mines?
    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return self.cells if len(self.cells) == self.count else set()

    # under what circumstances do you know for sure that a sentence’s cells are safe?
    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """ 
        return self.cells if self.count == 0 else set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        # check if cell in the sentence
        if cell in self.cells: 
            # Update both sides of the sentence
            ## Right side: cell is no longer in the sentence
            self.cells.remove(cell)
            ## Left side: decrease the count in the sentence
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        # check if cell in the sentence
        if cell in self.cells: 
            # Update 
            ## cell is no longer in the sentence
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell): # P
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell): # not P
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    # Added function => to identify the coordinates of neighboring cells
    def nearby_cells(self, cell):
        neighboring_cells = set()
        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                # Update count if cell in bounds
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighboring_cells.add((i, j))
        # expected result
        return neighboring_cells
    
    # Added function
    def new_cells_mines(self, cell, count): # either multiple P or multiple Not P
        neighboring_cells = self.nearby_cells(cell)
        undetermined_cells = set()
        new_count = count
        
        for neighboring_cell in neighboring_cells:
            if neighboring_cell in self.mines: # surely a mine (overlapped cell)
                new_count -= 1 # Adjust count
            elif neighboring_cell in self.safes: # surely safe (overlapped cell)
                continue
            else: # not yet known to be either safe or mines 
                undetermined_cells.add(neighboring_cell)
        return (undetermined_cells, new_count)
    
    # Added function
    def inference_from_knowledge(self):
        # a temporary list for new sentences to avoid modifying the AI's KB while iterating
        new_knowledge = []
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence1 != sentence2 and sentence1.cells and sentence2.cells:
                    if sentence1.cells.issubset(sentence2.cells):
                        new_cells = sentence2.cells - sentence1.cells
                        new_count = sentence2.count - sentence1.count
                        
                        # infer safe cells when given new information: Done
                        if new_count == 0:
                            for new_cell in new_cells:
                                self.mark_safe(new_cell)          

                        # infer mine when given new information: Not Yet
                        # if len(new_cells) == new_count:
                        #     for cell in new_cells:
                        #         self.mark_mine(cell)

                        # Add new sentence to AI's KB from inference
                        if new_cells: # not empty set
                            new_sentence = Sentence(new_cells, new_count)
                            if new_sentence not in self.knowledge:
                                new_knowledge.append(new_sentence)
        return new_knowledge

    def add_knowledge(self, cell, count):
        """
        ### IMPORTANT
        Called when the Minesweeper board tells us, 
        for a given safe cell, 
        how many neighboring cells have mines in them.
        ###

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        
        # Step 01: mark the cell as a move that has been made
        self.moves_made.add(cell)
        
        # Step 02: mark the cell as safe, otherwise the mine is activated and player lost the game.
        self.mark_safe(cell)
        
        # Step 03: add a new sentence to the AI's KB based on the value of `cell` and `count`
        new_cells_mines = self.new_cells_mines(cell, count)
        new_sentence = Sentence(new_cells_mines[0], new_cells_mines[1])
        self.knowledge.append(new_sentence)

        # Step 04: mark any additional cells as safe or as mines, if concluded based on the AI's KB
        for sentence in self.knowledge:
            # Create copies to avoid runtime errors when iterating the KB
            known_mines = sentence.known_mines().copy()
            known_safes = sentence.known_safes().copy()      
            # Mark all known mines
            for mine in known_mines:
                self.mark_mine(mine)
            # Mark all known safe cells
            for safe in known_safes:
                self.mark_safe(safe)
        
        # Step 05: add any new sentences to the AI's KB if they can be inferred from existing knowledge
        self.knowledge.extend(inference_from_knowledge())
        

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # return 1 safe cell to make
        for safe_cell in self.safes:
            if safe_cell not in self.moves_made:
                return safe_cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # return 1 random cell to make
        
        # All possible moves
        ''' Other script:
            moves = set(itertools.product(range(self.height), range(self.width)))
        '''
        moves = set()
        for i in range(self.height):
            for j in range(self.width):
                moves.add((i, j))

        # Remove all chosen moves and known to be mines
        # set1 - set2 means: Return all elements in set1 that are NOT in set2.
        moves_to_choose = moves - (self.mines | self.moves_made) # python sets: A - B - C == A - (B | C)

        # Return random moves
        return random.choice(list(moves_to_choose)) if moves_to_choose else None


