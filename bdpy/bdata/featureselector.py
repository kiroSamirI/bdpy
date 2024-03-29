"""
Feature selector class

This file is a part of BdPy
"""


class FeatureSelector(object):
    """
    Feature selector class

    Parameters
    ----------
    expression : str
        Selection command

    Attributes
    ----------
    expression : str
        Selection command
    token : tuple
        Tokens
    rpn : tuple
        Tokens in reversed polish notation
    """

    ## Class variables #####################
    signs = ('(', ')')
    operators = ('=', '|', '&', '@')

    __op_order = {'='   : 10,
                  '|'   : 5,
                  '&'   : 5,
                  '@'   : 3,
                  '('   : -1,
                  ')'   : -1}


    ## Methods #############################

    def __init__(self, expression):
        self.expression = expression
        self.token = self.lexical_analysis(self.expression)
        self.rpn = self.parse(self.token)

        self.index = None


    def lexical_analysis(self, expression):
        """Lexical analyser"""

        str_buf = ''
        output_buf = []

        for i in expression:
            if i == ' ':
                # Ignore a white-space
                continue
            elif self.signs.count(i) or self.operators.count(i):
                if len(str_buf) > 0:
                    output_buf.append(str_buf)
                    str_buf = ''

                output_buf.append(i)
            else:
                str_buf += i

        if len(str_buf) > 0:
            output_buf.append(str_buf)
            str_buf = ''

        return tuple(output_buf)


    def parse(self, token_list):
        """Parser for selection command"""

        out_que = []
        op_stack = []

        for token in token_list:

            if self.operators.count(token):
                while op_stack:
                    if self.__op_order[token] > self.__op_order[op_stack[-1]]:
                        break
                    out_que.append(op_stack.pop())

                op_stack.append(token)
            elif token == '(':
                op_stack.append('(')
            elif token == ')':
                while op_stack:
                    if op_stack[-1] == '(':
                        op_stack.pop()
                    else:
                        out_que.append(op_stack.pop())
            else:
                out_que.append(token)

        while op_stack:
            out_que.append(op_stack.pop())

        return tuple(out_que)
