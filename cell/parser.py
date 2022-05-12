from .stream import PeekableStream


class Parser:

    def __init__(self, token_stream, stop_at):
        """
        Converts token_stream to Peekable stream and
        sets the character at which to stop parsing
        current expression

        :param: token_stream - the stream of tokens
        :param: stop_at - the character to stop parsing at
        """
        self.tokens = token_stream
        self.stop_at = stop_at

    
    def next_expression(self, prev_token):
        """
        Parse the next expression given the previous token
        for context. Note: if the previous token is None, then
        the expression has no context and we are parsing the
        first token that will give us the context

        :param: prev_token - the previous token
        """

        # If the next token is None and no semi-colon has been reached
        self._premature_end(self.stop_at)

        # Get the type and value of the pointer token
        typ, value = self.tokens.pointer

        if typ in self.stop_at:
            # If the pointer token is the stop_at character, then expression is complete
            # Note: have to put before dispense_pointer() otherwise it will move the token prematurely
            # and mess with _parameters_list()
            return prev_token

        # Move on to the next token (can't put at end because of raising exception)
        self.tokens.dispense_pointer()
        
        if typ in ('number', 'string', 'symbol') and prev_token is None:
            # This is the first token since the previous token is None, we continue parsing
            return self.next_expression((typ, value))

        elif typ == 'operation':
            # Operation syntax tree, the lhs is the previous token
            rhs = self.next_expression(None)    # rhs is a new expression
            return self.next_expression(('operation', value, prev_token, rhs))

        elif typ == '=':
            # Assignment syntax tree, the lhs is the previous token
            if prev_token[0] != 'symbol': # check type of lhs - must be a symbol token
                raise Exception('You can only assign to a symbol.')
            rhs = self.next_expression(None)
            return self.next_expression(('assignment', prev_token, rhs))

        elif typ == '(':
            # Calling function, the name of function is the previous token

            # the arguments of the function can be expressions as well
            args = self._multiple_expressions(',',')')

            # allows for multiple function calls (ex. divide_by(3)(12) => 4)
            return self.next_expression(('call', prev_token, args)) 

        elif typ == '{':
            # Get the parameters of the function defintion
            # params and body is list
            params = self._parameters_list()
            body = self._multiple_expressions(';', '}')
            return self.next_expression(('function', params, body))

        else:
            raise Exception('Unexpected token:', str((typ,value)))


    def _multiple_expressions(self, sep_char, end_char):
        """"
        Parses expression separated by separator character and
        stop parsing when end character is reached
        
        :param: sep_char - the character to separate by
        :param: end_char - the character to stop parsing at
        """
        expressions = []

        self._premature_end(end_char)

        typ = self.tokens.pointer[0]

        if typ == end_char:
            # If the end character is reached, ignore it and return expressions list
            self.tokens.dispense_pointer()

        else:
            # Create a parser and get every argument/expression
            arg_parser = Parser(self.tokens, (sep_char, end_char))  # sep is in the stop_at
            
            while typ != end_char:
                
                exp = arg_parser.next_expression(None)
                if exp is not None:
                    expressions.append(exp)
                
                typ = self.tokens.pointer[0]    # updates type of the pointer token, if correctly written, this should be a ','
                
                self.tokens.dispense_pointer()  # move on the next token in the outer parser
                self._premature_end(end_char) # check to see if the next token is None

        return expressions


    def _parameters_list(self):
        """
        Parses parameters of function definition
        """

        if self.tokens.pointer[0] != ':':   
            # Takes no arguments
            return []

        self.tokens.dispense_pointer()  # do nothing with the colon
        typ = self.tokens.pointer[0]    # and get the pointer token

        if typ != '(':
            # Missing '('
            raise Exception('":" must be followed by "(" in a function definition')
        
        self.tokens.dispense_pointer() # do nothing with the '('

        parameters = self._multiple_expressions(',', ')')
        for param in parameters:
            # check if type of each parameter is valid
            if param[0] != 'symbol':
                raise Exception('Only symbols are allowed in function parameter list')
        
        return parameters 

    def _premature_end(self, expected):
        """
        Checks if the next token is None
        """
        if self.tokens.pointer is None:
            raise Exception("Hit EOF before", expected)


def parse(token_stream):
    """
    Creates a parser for the token stream and creates a
    nested syntax tree
    
    :param: token_stream - the stream of tokens to parse
    """
    parser = Parser(PeekableStream(token_stream), ';')  # have to set to PeekableStream here
    while parser.tokens.pointer is not None:
        expression = parser.next_expression(None)
        if expression is not None:
            yield expression
        parser.tokens.dispense_pointer() # ignores ;, Move on to start of next expression
