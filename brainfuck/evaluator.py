class Evaluator:

    def __init__(self):
        self.arr = [0] * 30000
        self.index = 0

    def _eval_expr(self, expr):
        typ = expr[0]

        match typ:

            case 'shift_right':
                self.index += 1

            case 'shift_left':
                if self.index != 0:
                    self.index -= 1
                else:
                    raise Exception('Negative index')

            case 'increment':
                self.arr[self.index] += 1

            case 'decrement':
                self.arr[self.index] -= 1

            case 'output':
                print(chr(self.arr[self.index]), end='')

            case 'input':
                entered = ''
                while len(entered) != 1:
                    entered = input('\nInput[one character only]: ')
                self.arr[self.index] = ord(entered)

            case 'while':
                while self.arr[self.index] != 0:
                    expression_list = expr[1]
                    self.eval_iter(expression_list)


    def eval_iter(self, expression_list):
        for exp in expression_list:
            self._eval_expr(exp)


def evaluate(ast_tokens):
    evaluator = Evaluator()
    evaluator.eval_iter(ast_tokens)
