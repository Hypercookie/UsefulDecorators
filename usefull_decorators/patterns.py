import weakref

from usefull_decorators.functions import attach


def Cache(cls):
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


def Singleton(strict=False):
    """
    Makes this class only have a single Instance. Adds a `getInstance` method to the class.
    If raise_error is true, an error will be raised if the class is initialized again.
    If not the calling the init method with any arguments will result in returning the
    instance and ignoring the arguments. If you want to create a new shared singleton
    with new arguments you can use the `resetInstance` class method or as a short hand
    `createNew` with the init arguments.
    """

    def singleton(cls):
        cls.__instance = None

        def __new_singleton(*args, **kwargs):
            if cls.__instance and strict:
                raise Exception(
                    "Can't create a new instance, a singleton for this class was " \
                    "already generated. ")

            if not cls.__instance:
                obj = object.__new__(cls)
                cls.__init__(*args, **kwargs)
                cls.__instance = obj
            return cls.__instance

        def getInstance():
            if not cls.__instance:
                raise Exception("You have to create a instance first")
            else:
                return cls.__instance

        def resetInstance():
            if strict:
                raise Exception("This is a strict singleton. It can not be reset")
            else:
                cls.__instance = None

        def createNew(*args, **kwargs):
            cls.resetInstance()
            obj = object.__new__(cls)
            cls.__init__(obj, *args, **kwargs)
            cls.__instance = obj
            return cls.__instance

        cls.__new__ = __new_singleton
        cls.getInstance = getInstance
        cls.resetInstance = resetInstance
        cls.createNew = createNew
        return cls

    return singleton


def builder_function(func):
    """
    Makes the decorated method return the object itself. Non-defined behaviour if used
    on non member methods. The return value of the original function is ignored.
    """

    def wrap(*args, **kwargs):
        func(*args, **kwargs)
        return args[0]

    return wrap


def Observable(func=None, attach=None):
    if not attach:
        attach = []
    if func:
        return _Observable(func, attach)
    else:
        def wrap(funct):
            return _Observable(funct, attach)

        return wrap


class _Observable:
    def __init__(self, cls, args):
        self.cls = cls
        self.attach = args
        self.obj = None

    def __call__(self, *args, **kwargs):
        self.obj = self.cls(*args, **kwargs)
        for x in self.attach:
            prpt = self.obj.__getattribute__(x[0])
            setattr(self.obj, "__" + x[0], prpt)

            def get(*qa):
                return qa[0].__getattribute__("__" + x[0])

            def set_v(*qa):
                r = qa[0].__setattr__("__" + x[0], qa[1])
                x[1](qa[1])
                return r

            def deletion(*qa, **qwa):
                return qa[0].__delattr__("__" + x[0])

            q = property(fget=get, fset=set_v, fdel=deletion)
            setattr(self.cls, x[0], q)
            # warpped_property = wrp()
        return self.obj
