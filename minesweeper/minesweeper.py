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

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell): 
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def nearby_cells(self, cell):
        neighboring_cells = set()
        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                neighboring_cells.add(i,j)
        
        return neighboring_cells

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
        
        # mark the cell as a move that has been made
        self.moves_made.add(self.cell)
        
        # mark the cell as safe
        mark_safe(self.cell)
        
        # add a new sentence to the AI's knowledge base based on the value of `cell` and `count`
        neighboring_cells = nearby_cells(self.cell)
        # Be sure to only include cells whose state is still undetermined in the sentence.
        undetermined_cells = set()
        for cell in neighboring_cells:
            if cell not in (self.mines or self.safe):
                undetermined_cells.add(cell)

        new_sentence = Sentence(undetermined_cells, self.count)
        self.knowledge.append(new_sentence)

        # mark any additional cells as safe or as mines, 
        # if it can be concluded based on the AI's knowledge base
        if len(new_sentence.known_mines) > 0:
            mined_cells = new_sentence.cells
            self.mines.add(new_sentence.cells)
            for sentence in self.knowledge:
                cells_to_track = sentence.cells
                cells_to_track.remove(mined_cells) 
        elif len(new_sentence.known_safes) > 0:
            safe_cells = new_sentence.cells
            self.safes.add(new_sentence.cells)
        
        # add any new sentences to the AI's knowledge base
        # if they can be inferred from existing knowledge
        

        # raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        raise NotImplementedError

# test
if __name__ == "__main__":  
    mineObject = Minesweeper()
    # print out the board
    mineObject.print()

    postions_of_mine = mineObject.mines
    print(f"Mines: {postions_of_mine}")
    check_cell = next(iter(postions_of_mine))
    print(f"Checking cell: {check_cell}")
    # print(f"New set of Mines?: {postions_of_mine}")
    print(f"Is_mine:{mineObject.is_mine(check_cell)}")
    # print(f"Mines found: {mineObject.mines_found}")
    print(f"Nearby mines: {mineObject.nearby_mines(check_cell)}")

    sentence = Sentence({(2,1),(3,6)},3)
    print(f"Sentence: {sentence}")
