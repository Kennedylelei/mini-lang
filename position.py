"""Position class
    
    Tracks the position of the current character in the input string.
    
    Attributes:
        idx (int): Index of the current character
        ln (int): Line number of the current character
        col (int): Column number of the current character
        fn (str): File name
        ftxt (str): File text    

    Returns:
        Position: A Position object
"""

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)