def s2i(s):
    """
    String to int
    """
    result=0
    l=len(s)
    for i in range(l):
        result+=ord(s[i])*(256**i)
    return result

def i2s(myi):
    """
    int to string
    """
    i=myi
    result=""
    k=0
    while i>=256**k:
        k+=1
    # k is the number of characters in the string
    for j in range(k-1,-1,-1):
        thing=i//(256**j)
        result=str.join("",(chr(thing),result))
        i-=thing*(256**j)
    return result



