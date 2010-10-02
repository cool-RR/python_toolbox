import re


def searchall(pattern, string, flags=0):
    if isinstance(pattern, basestring):
        pattern = re.compile(pattern, flags=flags)
    matches = []
    start = 0
    end = len(string)
    
    while True:
        match = pattern.search(string, start, end)
        if match:
            matches.append(match)
            start = match.end()
        else:
            break
    
    return matches
        