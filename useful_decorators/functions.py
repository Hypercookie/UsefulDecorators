import functools


class _GenericInfix:
    def __init__(self, function):
        self.function = function
        self.first = None
        self.second = None

    def __or__(self, other):
        return self.function(self.first, other)

    def __ror__(self, other):
        self.first = other
        return self


def infix(func):
    return _GenericInfix(func)


def attach(func, *args, **kwargs):
    """
    Attaches another function after the function decorated with this is run.
    Arguments can be passed to the attached function by using
    `@attach(func,a1,a2,a3=xy...)`
    """

    def attach_c(f):
        @functools.wraps(f)
        def attach_cc(*f1, **f2):
            res = f(*f1, **f2)
            func(*args, **kwargs)
            return res

        return attach_cc

    return attach_c


def prepend(func, *args, **kwargs):
    """
    Runs another function before the function decorated with this is run.
    Arguments can be passed to the prepended function by using
    `@prepend(func,a1,a2,a3=xy...)`
    """

    def prepend_c(f):
        @functools.wraps(f)
        def prepend_cc(*f1, **f2):
            func(*args, **kwargs)
            return f(*f1, **f2)

        return prepend_cc

    return prepend_c


def chain(func, *args, **kwargs):
    """
    Feeds the output of the function _with_ the decorator
    to the (first) input of the specified method. Additional arguments can be passed to
    the receiving function by using `chain(func,a1,a2,a3=xy...)`
    """

    def chain_c(f):
        def chain_cc(*f1, **f2):
            return func(f(*f1, **f2), *args, **kwargs)

        return chain_cc

    return chain_c
