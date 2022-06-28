import weakref


def cache(cls):
    """
    If the class initialized with the same arguments in its init method a second time,
    a cached version is returned. Creates two new class methods:
    `cls.__clear_cache` which clears the current cache (note that the objects stay
    intact)
    `cls.__create_no_cache` creates an object and ignores the cache. (Can be used to
    get a new object even if an old on is cached)
    """
    cls.__cache = weakref.WeakValueDictionary()

    def __new_cache__(*args, **kwargs):
        obj = cls.__cache.get(
            args[1:] + tuple((x, kwargs[x]) for x in kwargs.keys()))
        if obj is None:
            obj = object.__new__(cls)
            cls.__cache[
                args[1:] + tuple((x, kwargs[x]) for x in kwargs.keys())] = obj
            cls.__init__(*args, **kwargs)
        return obj

    def __clear_cache():
        cls.__cache = weakref.WeakValueDictionary()

    def __create_no_cache(*args, **kwargs):
        obj = object.__new__(cls)
        cls.__init__(obj, *args, **kwargs)
        return obj

    cls.__new__ = __new_cache__
    cls.__clear_cache = __clear_cache
    cls.__nc = __create_no_cache
    return cls


def attach(func, *args, **kwargs):
    """
    Attaches another function after the function decorated with this is run.
    Arguments can be passed to the attached function by using
    `@attach(func,a1,a2,a3=xy...)`
    """

    def attach_c(f):
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
