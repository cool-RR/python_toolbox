stringsaverlibrary=[]

def s2i(s):
    """
    String to int
    """
    global stringsaverlibrary
    if s in stringsaverlibrary:
        return stringsaverlibrary.index(s)
    else:
        stringsaverlibrary+=[s]
        return stringsaverlibrary.index(s)


def i2s(i):
    """
    int to string
    """
    return stringsaverlibrary[i]
