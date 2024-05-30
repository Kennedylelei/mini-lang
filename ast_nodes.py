from lexer import *


class NumberNode:
    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'

    def get_ic(self, get_next_temp_var, get_current_temp):
        return f't{get_next_temp_var()} = {self.tok.value}\n'


class StringNode:
    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'

    def get_ic(self, get_next_temp_var, get_current_temp):
        return f't{get_next_temp_var()} = "{self.tok.value}"\n'


class ListNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes

        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'{self.element_nodes}'

    def get_ic(self, get_next_temp_var, get_current_temp):
        code_statements = ''

        for node in self.element_nodes:
            code_statements += node.get_ic(get_next_temp_var, get_current_temp)
        return code_statements


class VarAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

    def __repr__(self):
        return f'{self.var_name_tok}'

    def get_ic(self, get_next_temp_var, get_current_temp):
        return f't{get_next_temp_var()} = {self.var_name_tok.value}\n'


class VarAssignNode:
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end

        # Token definition for the representation function
        self.var_token = Token(TT_KEYWORD, 'VAR')

    def __repr__(self):
        return f'{self.var_token} {self.var_name_tok} {TT_EQ} {self.value_node}'

    def get_ic(self, get_next_temp_var, get_current_temp):
        return f'{self.value_node.get_ic(get_next_temp_var, get_current_temp)}{self.var_name_tok.value} = t{get_current_temp()}\n'


class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'

    def get_ic(self, get_next_temp_var, get_current_temp):
        left_code = self.left_node.get_ic(get_next_temp_var, get_current_temp)
        temp_left_code = get_current_temp()

        right_code = self.right_node.get_ic(
            get_next_temp_var, get_current_temp)
        temp_right_code = get_current_temp()

        op = self.op_symbol_converter()
        return f'{left_code}{right_code}t{get_next_temp_var()} = t{temp_left_code} {op} t{temp_right_code}\n'

    def op_symbol_converter(self):
        if self.op_tok.type == TT_PLUS:
            return '+'
        elif self.op_tok.type == TT_MINUS:
            return '-'
        elif self.op_tok.type == TT_DIV:
            return '/'
        elif self.op_tok.type == TT_MUL:
            return '*'
        elif self.op_tok.type == TT_POW:
            return '^'
        elif self.op_tok.type == TT_EE:
            return '=='
        elif self.op_tok.type == TT_NE:
            return '!='
        elif self.op_tok.type == TT_LT:
            return '<'
        elif self.op_tok.type == TT_GT:
            return '>'
        elif self.op_tok.type == TT_LTE:
            return '<='
        else:
            return '>='


class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'

    def get_ic(self, get_next_temp_var, get_current_temp):
        node_code = self.node.get_ic(get_next_temp_var, get_current_temp)
        temp_node_code = get_current_temp()

        if self.op_tok.type == TT_MINUS:
            return f'{node_code}t{get_next_temp_var()} = -t{temp_node_code}\n'
        else:
            return f'{node_code}t{get_next_temp_var()} = +t{temp_node_code}\n'


class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (
            self.else_case or self.cases[len(self.cases) - 1])[0].pos_end

        # Token definition for the representation function
        self.if_token = Token(TT_KEYWORD, 'IF')
        self.else_token = Token(TT_KEYWORD, 'ELSE')
        self.then_token = Token(TT_KEYWORD, 'THEN')
        self.elif_token = Token(TT_KEYWORD, 'ELIF')

    def __repr__(self):
        if self.else_case is not None:
            # Start with the IF keyword and its condition
            res = f"{self.if_token}, {self.cases[0][0]}"

            # Add the THEN keyword and its statement
            res += f", {self.then_token}, {self.cases[0][1]}"

            # Add all the ELIF keywords, their conditions, and their statements
            for case in self.cases[1:]:
                res += f", {self.elif_token}, {case[0]}"
                res += f", {self.then_token}, {case[1]}"

            # Add the ELSE keyword and its statement
            res += f"{self.else_token}, {self.else_case}"

        else:
            # Start with the IF keyword and its condition
            res = f"{self.if_token}, {self.cases[0][0]}"

            # Add the THEN keyword and its statement
            res += f", {self.then_token}, {self.cases[0][1]}"

            # Add all the ELIF keywords and their conditions
            for case in self.cases[1:]:
                res += f", {self.elif_token}, {case[0]}"
                res += f", {self.then_token}, {case[1]}"

            # Add the ELSE keyword and its statement
            # res += f"{self.else_token}, {self.else_case}"
        return res

    def get_ic(self, get_next_temp_var, get_current_temp):
        code = ''

        if self.else_case is not None:
            # Start with the IF keyword and its condition
            condition_code = self.cases[0][0].get_ic(
                get_next_temp_var, get_current_temp)
            temp_condition_code = get_current_temp()
            label = get_next_temp_var()
            body_code = self.cases[0][1].get_ic(
                get_next_temp_var, get_current_temp)

            code += f'{condition_code} if !t{temp_condition_code} goto L{label} \n{body_code} L{label}:\n'

            # Add all the ELIF keywords, their conditions, and their statements
            for case in self.cases[1:]:
                condition_code = case[0].get_ic(
                    get_next_temp_var, get_current_temp)
                temp_condition_code = get_current_temp()
                label = get_next_temp_var()
                body_code = case[1].get_ic(
                    get_next_temp_var, get_current_temp)

                code += f'{condition_code} if !t{temp_condition_code} goto L{label} \n{body_code} L{label}:\n'

            # Add the ELSE keyword and its statement
            else_code = self.else_case[0].get_ic(
                get_next_temp_var, get_current_temp)
            code += f'{else_code}'
        else:
            # Start with the IF keyword and its condition
            condition_code = self.cases[0][0].get_ic(
                get_next_temp_var, get_current_temp)
            temp_condition_code = get_current_temp()
            label = get_next_temp_var()
            body_code = self.cases[0][1].get_ic(
                get_next_temp_var, get_current_temp)

            code += f'{condition_code} if !t{temp_condition_code} goto L{label} \n{body_code} L{label}:\n'

            # Add all the ELIF keywords and their conditions
            for case in self.cases[1:]:
                condition_code = case[0].get_ic(
                    get_next_temp_var, get_current_temp)
                temp_condition_code = get_current_temp()
                label = get_next_temp_var()
                body_code = case[1].get_ic(
                    get_next_temp_var, get_current_temp)

                code += f'{condition_code} if !t{temp_condition_code} goto L{label} \n{body_code} L{label}:\n'
        return code
        # condition_code = self.cases[0][0].get_ic(
        #     get_next_temp_var, get_current_temp)
        # temp_condition_code = get_current_temp()
        # label = get_next_temp_var()
        # body_code = self.cases[0][1].get_ic(
        #     get_next_temp_var, get_current_temp)

        # code += f'{condition_code} if !t{temp_condition_code} goto L{label} \n{body_code} L{label}:\n'

        # return code


class ForNode:
    def __init__(self, var_name_tok, start_value_node, end_value_node, step_value_node, body_node, should_return_null):
        self.var_name_tok = var_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node
        self.should_return_null = should_return_null

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.body_node.pos_end

        # Token definition for the representation function
        self.for_token = Token(TT_KEYWORD, 'FOR')
        self.to_token = Token(TT_KEYWORD, 'TO')
        self.then_token = Token(TT_KEYWORD, 'THEN')
        self.step_token = Token(TT_KEYWORD, 'STEP')

    def __repr__(self):
        res = f"{self.for_token}, {self.var_name_tok}, {self.to_token}, {self.end_value_node}, {self.step_token}, {self.step_value_node}, {self.then_token}, {self.body_node}"
        return res

    def get_ic(self, get_next_temp_var, get_current_temp):
        code = ''

        variable_name_token_name = self.var_name_tok.value

        start_value_code = self.start_value_node.get_ic(
            get_next_temp_var, get_current_temp)
        temp_start_value_code = get_current_temp()

        end_value_code = self.end_value_node.get_ic(
            get_next_temp_var, get_current_temp)
        temp_end_value_code = get_current_temp()

        if self.step_value_node:
            step_value_code = self.step_value_node.get_ic(
                get_next_temp_var, get_current_temp)
            temp_step_value_code = get_current_temp()

        loop_start_label = get_next_temp_var()
        loop_end_label = get_next_temp_var()

        code += f'\n {loop_start_label}: \n'

        code += f'{start_value_code}\n'
        code += f'{start_value_code} t{temp_start_value_code} = {variable_name_token_name} \n'
        code += f'{end_value_code}\n'
        if self.step_value_node:
            code += f'{step_value_code} t{temp_step_value_code} = {variable_name_token_name} \n'

        code += f'if t{temp_start_value_code} > t{temp_end_value_code} goto L{loop_end_label} \n'

        body_code = self.body_node.get_ic(
            get_next_temp_var, get_current_temp)
        code += body_code

        if self.step_value_node:
            code += f'{variable_name_token_name} = {variable_name_token_name} + t{temp_step_value_code} \n'
        else:
            code += f'{variable_name_token_name} = {variable_name_token_name} + 1 \n'

        code += f'goto L{loop_start_label} \n'

        code += f'\n {loop_end_label}: \n'

        return code


class WhileNode:
    def __init__(self, condition_node, body_node, should_return_null):
        self.condition_node = condition_node
        self.body_node = body_node
        self.should_return_null = should_return_null

        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end

        # Token defintion for the representation function
        self.while_token = Token(TT_KEYWORD, 'WHILE')
        self.then_token = Token(TT_KEYWORD, 'THEN')

    def __repr__(self):
        res = f"{self.while_token}, {self.condition_node}, {self.then_token}, {self.body_node}"
        return res

    def get_ic(self, get_next_temp_var, get_current_temp):
        code = ''

        condition_code = self.condition_node.get_ic(
            get_next_temp_var, get_current_temp)
        temp_condition_code = get_current_temp()

        loop_start_label = get_next_temp_var()
        loop_end_label = get_next_temp_var()

        code += f'\n{loop_start_label}:\n'

        code += f'{condition_code}t{get_next_temp_var()} = t{temp_condition_code}\n'
        code += f'if !t{get_current_temp()} goto {loop_end_label}\n'

        body_code = self.body_node.get_ic(get_next_temp_var, get_current_temp)
        temp_body_code = get_current_temp()

        code += f'{body_code}t{get_next_temp_var()} = t{temp_body_code}\n'

        code += f'goto {loop_start_label}\n'
        code += f'{loop_end_label}:\n\n'

        return code


class FuncDefNode:
    def __init__(self, var_name_tok, arg_name_toks, body_node, should_auto_return):
        self.var_name_tok = var_name_tok
        self.arg_name_toks = arg_name_toks
        self.body_node = body_node
        self.should_auto_return = should_auto_return

        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_name_toks) > 0:
            self.pos_start = self.arg_name_toks[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end

        # Token definition for the representation function
        self.fun_token = Token(TT_KEYWORD, 'FUN')

    def __repr__(self):
        return f"{self.fun_token}, {self.var_name_tok}, {self.arg_name_toks}, {self.body_node}"

    def get_ic(self, get_next_temp_var, get_current_temp):
        code = ''
        func_name = self.var_name_tok.value if self.var_name_tok else None

        if func_name:
            code += f'\n\nfunc_start {func_name}\n'
        else:
            code += f'\n\nfunc_start\n'

        for arg_name_tok in self.arg_name_toks:
            code += f'arg {arg_name_tok.value}\n'

        body_code = self.body_node.get_ic(get_next_temp_var, get_current_temp)
        temp_body_code = get_current_temp()

        # code += f'{body_code} t{get_next_temp_var()} = t{temp_body_code}\n'
        code += f'{body_code}\n'

        if self.should_auto_return:
            code += f'RETURN t{get_current_temp()}\n'

        code += f'func_end\n\n\n'

        return code


class CallNode:
    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

        self.pos_start = self.node_to_call.pos_start

        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[len(self.arg_nodes) - 1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end

        # Token definition for the representation function
        self.open_paren_token = Token(TT_LPAREN, '(')
        self.close_paren_token = Token(TT_RPAREN, ')')
        self.comma_token = Token(TT_COMMA, ',')
        # self.dot_token = Token(TT_DOT, '.')
        self.arrow_token = Token(TT_ARROW, '->')

    def __repr__(self):
        return f"{self.node_to_call}, {self.open_paren_token}, {self.arg_nodes}, {self.close_paren_token}"

    def get_ic(self, get_next_temp_var, get_current_temp):
        arg_nodes_ic = ''
        arg_nodes_temps = ''

        for arg_node in self.arg_nodes:
            arg_nodes_ic += arg_node.get_ic(get_next_temp_var,
                                            get_current_temp)
            arg_nodes_temp = get_current_temp()

            if arg_nodes_temps == '':
                arg_nodes_temps += f't{arg_nodes_temp}'
            else:
                arg_nodes_temps += f', t{arg_nodes_temp}'

        return f'{arg_nodes_ic} CALL {self.node_to_call.var_name_tok.value} {arg_nodes_temps}\n'


class ReturnNode:
    def __init__(self, node_to_return, pos_start, pos_end):
        self.node_to_return = node_to_return

        self.pos_start = pos_start
        self.pos_end = pos_end

        # Token definition for the representation function
        self.return_token = Token(TT_KEYWORD, 'RETURN')

    def __repr__(self):
        return f"{self.return_token}, {self.node_to_return}"

    def get_ic(self, get_next_temp_var, get_current_temp):
        return f'{self.node_to_return.get_ic(get_next_temp_var, get_current_temp)} RETURN t{get_current_temp()}\n'


class ContinueNode:
    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end

        # Token definition for the representation function
        self.continue_token = Token(TT_KEYWORD, 'CONTINUE')

    def __repr__(self):
        return f"{self.continue_token}"

    def get_ic(self, get_next_temp_var, get_current_temp):
        code = ''
        code += f'goto {get_next_temp_var()}\n\n'
        code += f'{get_current_temp()}:\n'
        return code


class BreakNode:
    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end

        # Token definition for the representation function
        self.break_token = Token(TT_KEYWORD, 'BREAK')

    def __repr__(self):
        return f"{self.break_token}"

    def get_ic(self, get_next_temp_var, get_current_temp):
        code = ''
        code += f'goto {get_next_temp_var()}\n\n'
        code += f'{get_current_temp()}:\n\n'
        return code