import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self): # unary constraints
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for v in self.domains:
            value_to_remove = set() # collect words to remove later
            
            for word in self.domains[v]:
                if len(word) != v.length:
                    value_to_remove.add(word) # don't remove directly to avoid modify the set's size while iterating over it
            
            # remove set of inconsistent words of variable v
            self.domains[v] -= value_to_remove

    def revise(self, x, y): # binary constraints
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        overlap = self.crossword.overlaps[x, y]
        if not overlap:
            return False
        
        i, j = overlap
        # if overlap, (i, j), where x's ith character overlaps y's jth character
        conflict = set()
        for w1 in self.domains[x]:
            # If there is NO word in y's domain that matches w1 at the overlap, mark w1 for removal
            if not any(w1[i] == w2[j] for w2 in self.domains[y]):
                conflict.add(w1)
            
            '''
            for w2 in self.domains[y]:
                if w1[i] == w2[j]:
                    break # exit the inner loop y, go to next iteration of outer loop x
            # No break occurred: no match found
            else: 
                conflict.add(w1)
            '''

        # update the values of variable x
        if conflict:
            self.domains[x] -= conflict
            return True
        return False
        
        
    def ac3(self, arcs=None): # adds all the arcs in the csp to a queue then iterates to revise the pairs of value
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Deques are sequence-like data types designed as a generalization of stacks and queues. 
        # They support memory-efficient and fast append and pop operations on both ends of the data structure.

        queue = list()
        if arcs is None:
            for var1 in self.domains:
                # for var2 in self.domains:
                for var2 in self.crossword.neighbors(var1):
                    if var1 != var2:
                        queue.append((var1, var2))
        else:
            queue = arcs
        
        while queue:
            x, y = queue.pop(0) # dequeue an arc from queue
            if self.revise(x,y):
                if len(self.domains[x]) == 0:
                    return False
                for z in (self.crossword.neighbors(x) - {y}):
                    queue.append((z,x)) # enqueue an arc to queue
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        for var in self.crossword.variables:
            if var not in assignment or not isinstance(assignment[var], str):
                return False
        return True
                
    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # all values are distinct => values of a set are always distinct
        if len(set(assignment.values())) != len(assignment): 
            return False

        for var in assignment:
            # every value is the correct length according to the variable's length = if one value's length is incorrect, False
            if var.length != len(assignment[var]):
                return False
        
            # no conflicts between neighboring variables = if one conflict happens, False
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment:
                    continue
                i, j = self.crossword.overlaps[var, neighbor]
                if assignment[var][i] != assignment[neighbor][j]:
                    return False

        # If satify all the constraints above
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        
        values_rule_out = {word: 0 for word in self.domains[var]}
        
        for word in self.domains[var]:
            n = 0
            for neighbor in self.crossword.neighbors(var):
                overlap = self.crossword.overlaps[var, neighbor]
                
                # pass if the assigned neighbors or word is not overlapped
                if neighbor in assignment or not overlap:
                    continue
                
                i, j = overlap
                for neighbor_word in self.domains[neighbor]:
                    if word[i] != neighbor_word[j]:
                        n += 1
            
            values_rule_out[word] = n
        
        return sorted(self.domains[var], key= values_rule_out.__getitem__)


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        # unassigned variables and their domain sizes
        unassigned_vars = {
            var: len(self.domains[var])
            for var in self.domains
            if var not in assignment
        }
        
         # Sort variables by domain size (MRV heuristic)
        sorted_list = sorted(unassigned_vars.keys(), key=unassigned_vars.__getitem__)

        # Check for ties
        tie_list = [sorted_list[0]]
        for var in sorted_list[1:]:
            if len(self.domains[var]) == len(self.domains[sorted_list[0]]):
                tie_list.append(var)
        
        # Break tie using degree heuristic
        if len(tie_list) == 1:
            return sorted_list[0]
        else:
            return max(tie_list, key=lambda var: len(self.crossword.neighbors(var)))



    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)

def test():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    
    # Test functions
    creator.enforce_node_consistency()
    
    # for var in creator.domains:
    #     print(f"{var} => {creator.domains[var]}")
    #     print(f"{var} => {crossword.neighbors(var)}")
    
    # for cell in crossword.overlaps:
    #     if crossword.overlaps[cell]:
    #         print(f"{cell} => {crossword.overlaps[cell]}")

    # x = Variable(1, 7, 'down', 7)
    # y = Variable(4, 4, 'across', 5)
    # print(f"x = {creator.domains[x]}")
    # print(f"y = {creator.domains[y]}")
    # print(f"overlap = {crossword.overlaps[x, y]}")
    
    # print(creator.revise(x,y))
    # print(f"revised x = {creator.domains[x]}")    

    # arcs = list()
    # for var1 in creator.domains:
    #     for var2 in creator.domains:
    #         if var1 == var2:
    #             continue
    #         arcs.append((var1, var2))
    # print(arcs[:3])
    # print(arcs.pop(0))

    # print(creator.domains)
    # x = Variable(2, 1, 'across', 12)
    # print(x)
    # print(crossword.neighbors(x))
    
    # creator.ac3()
    # print(creator.domains)

    # # pick a variable to test
    # var = next(iter(creator.crossword.variables))

    # # example partial assignment (empty)
    # assignment = {}

    # # test order_domain_values
    # ordered_values = creator.order_domain_values(var, assignment)
    # print(f"Domain values for {var} ordered by least constraining: {ordered_values}")    



if __name__ == "__main__":
    # main()
    test()
