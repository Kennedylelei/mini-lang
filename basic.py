from error import *
from position import *
from constants import *
from lexer import *
from parser import *



#######################################
# RUN
#######################################

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error