import math

def frange(start, finish=None, step=1.):

  if finish is None:
    finish, start = start, 0.
  else:
    start = float(start)

  count = int(math.ceil(finish - start)/step)
  return (start + n*step for n in range(count))