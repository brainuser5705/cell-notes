from stream import PeekableStream

def lex(char_stream):
    """
    Converts sequence of characters into a PeekableStream
    and generates tokens
    
    :param: char_stream - the sequence of characters
    """

    stream = PeekableStream(char_stream)

    while stream.pointer is not None:
        char = stream.dispense_pointer()

        match char:
            case '>':
                yield ('shift_right')
            case '<':
                yield ('shift_left')
            case '+':
                yield ('increment')
            case '-':
                yield ('decrement')
            case '.':
                yield ('output')
            case ',':
                yield ('input')
            case '[':
                yield ('start_while')
            case ']':
                yield ('end_while')
            case _:
                pass

