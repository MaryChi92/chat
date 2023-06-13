import inspect
import logging
import sys
import traceback


class Log:

    def __init__(self):
        self.name = str(sys.argv[0].split('.')[0])
        self.logger = logging.getLogger(self.name)

    def __call__(self, func_to_log):
        def wrapper(*args, **kwargs):
            res_of_func = func_to_log(*args, **kwargs)
            self.logger.info(f'Function {func_to_log.__name__} was called - args: {args}, kwargs: {kwargs}. '
                             f'It was called from function {traceback.format_stack()[0].strip().split()[-1]}', stacklevel=2)
            return res_of_func
        return wrapper
