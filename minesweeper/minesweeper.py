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
    def cell_info(self, cell, count): # either P or Not P
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
        
        # Add new sentence to knowledge base
        if undetermined_cells: # not empty
            self.knowledge.append(Sentence(undetermined_cells, new_count))
    
    ''' Let play the game and figure out inferences your own first '''
    # Added function
    # Each new inference might enable additional inferences => apply a recursion
    def make_inferences(self):
        while True:
            new_information = False
            
            # Check each sentence for known mines/safes
            for sentence in self.knowledge:
                # when you mark the cells, remove function will activate
                # create copies to avoid runtime error when iterating the KB
                known_mines = sentence.known_mines().copy() 
                known_safes = sentence.known_safes().copy()
                
                # Mark new mines
                for mine in known_mines:
                    if mine not in self.mines:
                        self.mark_mine(mine)
                        new_information = True # keep the recursion
                        
                # Mark new safes
                for safe in known_safes:
                    if safe not in self.safes:
                        self.mark_safe(safe)
                        new_information = True # keep the recursion
            
            # Step 5: Add new sentences from subset inference
            new_knowledge = []
            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:
                    if sentence1 != sentence2 and sentence1.cells and sentence2.cells:
                        if sentence1.cells.issubset(sentence2.cells):
                            new_cells = sentence2.cells - sentence1.cells
                            new_count = sentence2.count - sentence1.count
                            new_sentence = Sentence(new_cells, new_count)
                            
                            if new_sentence not in self.knowledge and new_cells:
                                new_knowledge.append(new_sentence)
                                new_information = True
                                
            # Add new sentences to knowledge base
            self.knowledge.extend(new_knowledge)
            
            # Stop if no new inferences or information were made
            if not new_information:
                break
    

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
        self.cell_info(cell, count)

        # Step 04: mark any additional cells as safe or as mines, if concluded based on the AI's KB
        # Step 05: add any new sentences to the AI's KB if they can be inferred from existing knowledge
        self.make_inferences()
        

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


