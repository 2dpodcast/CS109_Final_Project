def pathget(d, path, default=None):
    """Retrieve an item at a path location within a dict.

    Created for working with deeply nested JSON objects.
    """
    try:
        return reduce(dict.__getitem__,path,d)
    except:
        return default

