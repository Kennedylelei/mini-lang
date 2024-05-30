from error import *
from position import *
from constants import *
from lexer import *
from parser_ import *

"""Mini
        Description:
            This is the main file of the Mini programming language.
            It puts together the lexer, parser, and intermediate code generator.
            It contains the following:
                1. IntermediateCodeGenerator class
                2. run_lexer function
                3. run_parser function
                4. run_intermediate_code_generator function

"""

# ===============================================================================
# INTERMEDIATE CODE GENERATOR
# ===============================================================================
class IntermediateCodeGenerator:
    def __init__(self, ast):
        self.temp_counter = 0
        self.ast = ast

    def get_next_temp_var(self):
        self.temp_counter += 1
        return self.temp_counter - 1

    def get_current_temp(self):
        return self.temp_counter - 1

    def generate_intermediate_code(self):
        if self.ast == None:
            return ''
        return self.ast.get_ic(self.get_next_temp_var, self.get_current_temp)


# ===============================================================================
# RUN
# ===============================================================================


def run_lexer(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    return tokens, error


def run_parser(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    return ast.node, ast.error


def run_intermediate_code_generator(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    # Generate Intermediate Code
    icg = IntermediateCodeGenerator(ast.node)

    return icg.generate_intermediate_code(), ast.error

#######################################
# RUN
#######################################

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()

    return ast.node, ast.error