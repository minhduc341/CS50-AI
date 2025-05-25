import itertools
import random
import copy

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

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

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return self.cells
        else:
            return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.discard(cell)
            self.count -= 1
        else:
            pass

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.discard(cell)
        else:
            pass  


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

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

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
        #1) mark the cell as a move that has been made
        self.moves_made.add(cell)

        #2) mark the cell as safe
        self.mark_safe(cell)

        '''
        3) add a new sentence to the AI's knowledge base
           based on the value of `cell` and `count`
        '''
            # create a list of nearby cells
        neighbors = list()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # ignore the cell itself
                if i == cell[0] and j == cell[1]:
                    continue
                # Add neighboring cell to set only if it's in bounds
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbors.append((i, j))

        new_sentence = Sentence(neighbors, count)
        
            # ignore cells that are known to be safe or mine
        for safe in self.safes:
            new_sentence.mark_safe(safe)
        for mine in self.mines:
            new_sentence.mark_mine(mine)
            # add new sentence to knowledge if it is not empty
        if len(new_sentence.cells) != 0:
            self.knowledge.append(new_sentence)    

        '''
        4) mark any additional cells as safe or as mines
           if it can be concluded based on the AI's knowledge base
        '''

        new_safes = set()
        new_mines = set()
        if len(self.knowledge) != 0:
            for sentence in self.knowledge:
                if sentence.known_safes() != None:
                    for safe in sentence.known_safes():
                        new_safes.add(safe)
                if sentence.known_mines() != None:
                    for mine in sentence.known_mines():
                        new_mines.add(mine)
                    

            if new_safes:
                for cell in new_safes:
                    self.mark_safe(cell)
            if new_mines:
                for cell in new_mines:
                    self.mark_mine(cell)

        '''
        5) add any new sentences to the AI's knowledge base
           if they can be inferred from existing knowledge
        '''
        new_cells = set()
        for sentence_1 in self.knowledge:
            for sentence_2 in self.knowledge:
                if sentence_1 != sentence_2:
                    if sentence_1.cells.issubset(sentence_2.cells):
                        new_cells = sentence_2.cells - sentence_1.cells
                        new_count = sentence_2.count - sentence_1.count
                    if new_cells: #ignore empty cells
                        new_sentence = Sentence(new_cells, new_count)
                        if (new_sentence not in self.knowledge):
                            self.knowledge.append(new_sentence)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_move = self.safes - self.moves_made
        if not safe_move:
            return None
        return safe_move.pop()

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        all_moves = set()
        for i in range(self.height):
            for j in range(self.width):
                all_moves.add((i,j))
        moves_left = all_moves - self.moves_made - self.mines

        # Return a ramdom cell from moves_left if not empty
        if not moves_left:
            return None
        return random.choice(tuple(moves_left))