from castus.itertools import xform_methname

def linescanner(func):
    """Decorator to convert first argument to an iterable.

    Useful for writing line-oriented scanners that will take either a
    filehandle or a string.  If the first argument passed supports
    splitlines, it will be converted to an iterable using splitlines.

    """
    def inner(*args, **kw):
        args_ary = list(args)
        args_ary[0] = xform_methname(args[0], 'splitlines', True)
        return func(*tuple(args_ary), **kw)
    return inner
