class Env:

    def __init__(self, parent_env=None, stdin=None, stdout=None, stderr=None):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        
        # assign the parent environment
        self.parent_env = parent_env
        if parent_env is not None:
            assert stdin is None
            assert stdout is None
            assert stderr is None
            self.stdin = parent_env.stdin
            self.stdout = parent_env.stdout
            self.stderr = parent_env.stderr

        # the symbol names and value pairs in the environment
        self.items = dict()
        

    def get(self, name):

        if name in self.items:
            # see if symbol is defined in local environment
            return self.items[name]
        elif self.parent_env is not None:
            # see if symbol is defined in outer environment recursively
            return self.parent_env.get(name)
        else:
            # gives up at global environment (which has None for parent_env)
            return None 


    def set(self, name, value):
        # newly defined symbols are definend inthe local environment
        self.items[name] = value