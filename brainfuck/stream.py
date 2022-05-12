"""
Stream that gets ready to dispense the characters using
a `pointer` attribute
"""
class PeekableStream:

    def __init__(self, char_stream):
        """
        Turns the character stream into an iterable object.
        Fills in the pointer character.

        :param: char_stream - the sequence of characters representing the source code
        """
        self.iterator = iter(char_stream)
        self._fill_pointer()


    def _fill_pointer(self):
        """
        Fills in the pointer character the stream is ready to return.
        """
        try:
            self.pointer = next(self.iterator)
        except StopIteration:
            self.pointer = None

    def dispense_pointer(self):
        """
        Returns the pointer character, and renews it with the next
        character in the stream.

        :return: the character it was ready to dispense
        """
        old_curr = self.pointer
        self._fill_pointer() # automatically changes to the next character
        return old_curr

    