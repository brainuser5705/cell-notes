from stream import PeekableStream

class Parser:

    def __init__(self, token_stream):
        self.tokens = token_stream


    def next_expression(self):
        
        typ = self.tokens.pointer
        #print('type: ' + typ)

        self.tokens.dispense_pointer()

        match typ:

            case 'start_while':

                expressions_list = self._get_multiple_expressions()
                return ('while',expressions_list)

            case 'end_while':
                raise Exception(" ']' does not have matching '[' ")

            case _:
                return (typ,)    # have to do this because we already dispense the pointer
                # single element tuple

    def _get_multiple_expressions(self):

        expressions = []

        typ = self.tokens.pointer

        if typ != 'end_while':

            exp_parser = Parser(self.tokens)
            #print('Created new parser')

            while typ != 'end_while':

                exp = exp_parser.next_expression()
                #print('expression: ' + exp)
        
                if exp is not None:
                    #print("expression: " + exp)
                    expressions.append(exp)
                else:
                    raise Exception(" Missing ']' ")

                typ = exp_parser.tokens.pointer

            #print('Done with new parser')

        self.tokens.dispense_pointer()  # ignore the ']'
                
        return expressions
        
def parse(token_stream):
    parser = Parser(PeekableStream(token_stream))
    while parser.tokens.pointer is not None:
        expression = parser.next_expression()
        if expression is not None:
            yield expression

