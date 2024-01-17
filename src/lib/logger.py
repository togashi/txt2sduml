from . import verbosity

class Logger:
    ''' ロガー '''
    
    def __init__(self, verbosity = 0):
        self.verbosity = verbosity
    
    def error(self, *args, **kwargs):
        print(*args, **kwargs)
    
    def warn(self, *args, **kwargs):
        print(*args, **kwargs)
    
    def log(self, *args, **kwargs):
        print(*args, **kwargs)

    def info(self, *args, **kwargs):
        if self.verbosity >= verbosity.INFO:
            print(*args, **kwargs)

    def debug(self, *args, **kwargs):
        if self.verbosity >= verbosity.DEBUG:
            print(*args, **kwargs)

    def trace(self, *args, **kwargs):
        if self.verbosity >= verbosity.TRACE:
            print(*args, **kwargs)
