import sys

def die(s=None):
    """Print a string on stderr and exit with a failing status code."""
    if s is not None:
        sys.stderr.write("{}\n".format(s))
    sys.exit(1)
