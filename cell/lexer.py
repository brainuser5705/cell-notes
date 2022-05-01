from .stream import PeekableStream
from re import match


def _scan(first_char, stream: PeekableStream, allowed):
    """
    Continue building return until unallowed character is reached.

    :param: first_char - the first character of the return
    :param: stream - the stream of characters
    :param: allowed - the regular expression of allowed characters
    """
    ret = first_char
    next_char = stream.pointer

    while next_char is not None and match(allowed, next_char):
        ret += stream.dispense_pointer()
        next_char = stream.pointer

    return ret


def _scan_string(end_type, stream: PeekableStream):
    """
    Continue building string until end quote is reached

    Note: the first_char like in _scan() is not present
    because we do not need to keep the starting quote

    :param: end_type - the end quote for the string
    :param: stream - the stream of characters
    """
    string = '' 
    next_char = stream.pointer

    while next_char != end_type:
        c = stream.dispense_pointer()
        if c is None:
            raise Exception("Run off string")
        string += c
        next_char = stream.pointer

    stream.dispense_pointer()   # dispense and ignore the ending quote

    return string


def lex(char_stream):
    """
    Converts sequence of characters into a Peekable Stream
    and generates tokens based on lexemes of language
    """
    stream = PeekableStream(char_stream)
    while stream.pointer is not None:
        dis_char = stream.dispense_pointer()    # gets the pointer character from the stream
        
        # newline is ignore
        if dis_char in " \n":
            pass

        # variables can only start with underscores or characters
        # _scan() is called to continue to stream characters
        elif match('[_a-zA-Z]', dis_char):
            yield ('symbol', _scan(dis_char, stream, '[_a-zA-Z0-9]'))

        # numbers also need to continue to stream characters
        elif match('[.0-9]', dis_char):
            yield ('number', _scan(dis_char, stream, '[.0-9]')) # fix this so that it does do it again for decimals?

        # strings continue streaming only if the quotes match
        elif dis_char in ('"',"'"):
            yield ('string', _scan_string(dis_char, stream))

        # operations
        elif dis_char in '+-*/':
            yield ('operation', dis_char)

        # special characters
        elif dis_char in '(){},;=:':
            yield (dis_char, '')

        else:
            raise Exception('Unexpected character: "' + dis_char + '".')