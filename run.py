import mini
import time
import sys

file_name = 'test.mini'

# get the file name from the user as a command line argument
#file_name = sys.argv[1]
if file_name == None:
    print("No file name provided")
    exit()
if file_name[-5:] != ".mini":
    print("Invalid file name. File name must end with .mini")
    exit()




def run_lexer():
    text = ""
    with open(file_name, 'r') as file:
        text = file.read()

    if text.strip() == "":
        return
    result, error = mini.run_lexer(file_name, text)

    if error:
        print(error.as_string())
    else:
        for token in result:
            print(token)


def run_parser():
    text = ""
    with open(file_name, 'r') as file:
        text = file.read()

    if text.strip() == "":
        return
    result, error = mini.run_parser(file_name, text)

    if error:
        print(error.as_string())
    else:
        print(result)
        
def run_icg():
    text = ""
    with open(file_name, 'r') as file:
        text = file.read()

    if text.strip() == "":
        return
    result, error = mini.run_intermediate_code_generator(file_name, text)

    if error:
        print(error.as_string())
    else:
        print(result)


# Calculate Run Time
lexer_start_time = time.time()
print("===============================================================================================")
run_lexer()

lexer_finish_time = time.time()

lexer_total_run_time = lexer_finish_time - lexer_start_time
print("===============================================================================================")
print("\n", file_name, "Mini Lexer runs in:",
      lexer_total_run_time, "seconds")
print("===============================================================================================")
print("\n\n")

parser_start_time = time.time()
print("\n\n")
print("===============================================================================================")
run_parser()

parser_finish_time = time.time()

parser_total_run_time = parser_finish_time - parser_start_time
print("\n", file_name, "Mini Parser runs in:",
      parser_total_run_time, "seconds")

icg_start_time = time.time()
print("===============================================================================================")
run_icg()

icg_finish_time = time.time()
icg_total_run_time = icg_finish_time - icg_start_time
print("=====================================================================")
print("\n", file_name, "Mini Intermediate Code Generator runs in:", icg_total_run_time, "seconds")