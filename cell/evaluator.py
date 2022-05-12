import inspect 
from .env import Env


def eval_expr(expr, env: Env):
    """
    Evaluate an expression from the abstract syntax tree
    created by the parser with a given environment

    :param: expr - the expression to evaluate
    :param: env - the environment to work in
    """

    typ = expr[0]   # the type of the expression is always the first value of the tuple

    if typ == 'number':
        # from lexer and parser, number tokens 
        # come out as ('number', <value: str>)
        # expr[1] would be the value
        return ('number', float(expr[1]))

    elif typ == 'string':
        # ('string', <value: str>)
        return ('string', expr[1])

    elif typ == 'none':
        # None special value that is injected in the global environment
        # missing or empty value
        return ('none',)

    elif typ == 'operation':
        return _operation(expr, env)

    elif typ == 'symbol':
        # from lexer and parser: ('symbol', <value: str>)
        name = expr[1]
        value = env.get(name)   # get the value from the environment
        if value is None:
            raise Exception("unknown symbol:", name)
        return value

    elif typ == 'assignment':
        # from parser: ('assignment', <lhs_token>, <rhs_token>)
        # parser code enforces lhs_token's type to be symbol

        sym_name = expr[1][1]   # get the symbol token's value
        value = eval_expr(expr[2], env) # evaluate the rhs token
        env.set(sym_name, value) # set the symbol to value in the current environment
        return value

    elif typ == 'call':
        return _function_call(expr,env)

    elif typ == 'function':
        # from parser: ('function', <list of parameters>, <list of expressions in body>)
        # creates a new child environment
        return ('function', expr[1], expr[2], Env(env))

    else:
        raise Exception('Unknown expression type')


def _operation(expr, env):
    """
    from lexer: ('operation', <operation_sym>)
    from parser: ('operation', <operation_sym: str>, <expr_1: token>, <expr_2: token>)
    expr[1] - operation symbol
    expr[2] - lhs token
    expr[3] - rhs token

    :param: expr - the operation token
    """
    operator = expr[1]
    arg1 = eval_expr(expr[2], env) # evaluate the tokens with the same environment
    arg2 = eval_expr(expr[3], env)

    if operator == '+':
        return ('number', arg1[1] + arg2[1])
    elif operator == '-':
        return ('number', arg1[1] - arg2[1])
    elif operator == '*':
        return ('number', arg1[1] * arg2[1])
    elif operator == '/':
        return ('number', arg1[1] / arg2[1])
    else:
        raise Exception('Unknown operation')


def _function_call(expr, env):
    """
    from parser: ('call', <symbol or function token>, <arguments - list of expressions>)
    """
    
    # Evaluate the symbol or function token
    func = eval_expr(expr[1], env)
    
    # Evaluate the arguments
    args = list((eval_expr(arg, env) for arg in expr[2]))
    
    if func[0] == 'function':
        # eval_expr returns ('function', <list of parameters>, <body expressions>, 
        # environment who is child of the call environment)

        params = func[1]
        _check_args(params, args)
        body_expressions = func[2]
        fn_env = func[3]
        new_env = Env(fn_env)   # creates another environment for inside the function

        # for each parameter, pair it with its corresponding argument
        for param, arg in zip(params, args):
            # parser code ensures that parameters are symbol tokens so param[1] is a string
            new_env.set(param[1],arg)

        # get the final return after all the expression in the body have been evaluated
        # (technically ignores return values of all but the last line)
        # function body is evaluated in the new environment where all the 
        # parameters and argument pairs have been set
        return eval_list(body_expressions, new_env) 
    
    elif func[0] == 'native':
        # for functions not written in Cell
        py_func = func[1]
        params = inspect.getargspec(py_func).args
        _check_args(params[1:], args)   # check the number of arguments
        return func[1](env, *args)
    
    else:
        raise Exception("not a function")


def _check_args(params, args):
    """
    Ensures that the number of arguments passed into the function
    call token is the same as the the number of parameters in the
    function token
    """
    if len(params) != len(args):
        raise Exception("wrong number of args")


def eval_list(expression_list, env):
    """
    Evaluate expressions

    :expression_list: all the expressions in the function body
    """
    return_value = ("none",) # default return is none type
    for expr in eval_iter(expression_list, env):
        return_value = expr
    return return_value


def eval_iter(expression_list, env):
    """
    Evaluate the expressions in the list

    :expression_list: - the list of expressions to evaluate
    """
    for expr in expression_list:
        yield eval_expr(expr, env)

    
        