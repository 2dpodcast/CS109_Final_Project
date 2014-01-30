"""tmpldict - dictionaries of named templates

"""

class Tmpldict():
    def add_templates(self, templates):
        for k in templates.keys():
            self.templates[k] = templates[k]

    def __init__(self, templates = None):
        self.templates = {}

        if templates is not None:
            self.add_templates(templates)

    def instantiate(self, tmplname, fmtargs):
        """Return an instantiated template."""
        return self.templates[tmplname].format(*fmtargs)
