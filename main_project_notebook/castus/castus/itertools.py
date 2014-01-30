def xform_methname(x, methname, *args):
    """If x supports methname return x.methname(*args), else return x."""
    if hasattr(x, methname):
        return getattr(x, methname)(*args)
    else:
        return x
