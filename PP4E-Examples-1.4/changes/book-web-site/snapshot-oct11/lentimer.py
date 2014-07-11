"test the relative speeds of len(X) versus X.__len__()"

import time, sys

def timer(func, reps=50):
    """
    time the best of N runs of a zero-arg function;
    see also generalized timer() in the book LP4E,
    pages 509..518, in Chapter 20, Functions part
    """
    best = 2 ** 32
    for i in range(reps):
        start = time.clock()
        retval = func()
        elapsed = time.clock() - start
        if elapsed < best:
            best = elapsed
    return (best, retval)

# hoist out and equate range() time: list in 2.X, generator in 3.X
innerloop = list(range(500000))

#
# test cases: both take len of 500k list, 500k times
#
def builtinFunc():
    for i in innerloop:
        x = len(innerloop)
    return x

def underMethod():
    for i in innerloop:
        x = innerloop.__len__()
    return x

if __name__ == '__main__':
    print(sys.version.split()[0])
    for func in (builtinFunc, underMethod):
        print(func.__name__)
        print(timer(func))
