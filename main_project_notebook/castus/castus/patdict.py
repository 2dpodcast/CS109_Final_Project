"""patdict - dictionaries of named regular expressions

"""

class Patdict():
    def add_regexes(self, regexes):
        for k in regexes.keys():
            self.regexes[k] = re.compile(regexes[k])

    def __init__(regexes = None):
        self.regexes = {}

        if regexes is not None:
            self.add_regexes(regexes)

    def match_pat(self, patname, s):
        """Match a given pattern by name.

        Returns a match object on success, None on failure.
        """
        return self.regexes[patname].match(s)

    def match_group(self, patname, s, groupname):
        """Given a pattern name, a string, and a group name, return the
        captured group name.  If no match is found, return None."""
        m = self.match_pat(patname, s)
        if m:
            return m.group(groupname)
        else:
            return None

    def match_str(self, s):
        """Given a string, match against all patterns in the dictionary.

        Returns all matches from the dictionary as an array of [key,
        match] pairs.
        """

        ret = []
        for k in regexes.keys():
            m = re_match_pat(k, s)
            if m:
                ret.append([k, m])

        return ret

