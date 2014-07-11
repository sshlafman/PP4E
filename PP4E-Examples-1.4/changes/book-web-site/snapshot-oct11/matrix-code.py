"""
a numerically-inclined student asked for examples related to 
matrix processing (in the core language, not using NumPy which
has better built-in support for vector and matrix processing);
the following is a quick tour through some simple matrix code,
showing equivalents coded in for loops and list comprehensions;
requires Python 2.7 for some tests, one line works in 3.X only;
"""



######################################################################################
# Vectors: 1D lists (added mar-12-11)
######################################################################################


L = [1, 2, 3, 4, 5, 6]
M = [7, 8, 9, 10, 11, 12]


#-------------------------------------------------------------
# (L ** 2): print squares of all in one vector: 1 4 9 16 25 36
#-------------------------------------------------------------

for i in range(len(L)): 
    print(L[i] ** 2) 

for x in L:                                 # simpler, probably faster
    print(x ** 2)


# ---3.X only--- 
list( map(print, (x ** 2 for x in L)) )     # 3.X print(), map() generator


#------------------------------------------------------------
# (N = L ** 2): make new result vector: [1, 4, 9, 16, 25, 36]
#------------------------------------------------------------

N = [x ** 2 for x in L]                     # list comprehension
print(N)

N = []
for x in L:                                 # manual loop: often slower
    N.append(x ** 2)
print(N)

N = list(map((lambda x: x ** 2), L))        # map: need list() in 3.X only
print(N)


#
# other: generators produce results on demand
#

G = (x ** 2 for x in L)          # generator expression
print(list(G))                   # list() requests results

def gensquares(L):               # generator function
    for x in L:
        yield x ** 2

print(list(gensquares(L)))       # list() requests results


#
# other: set and dict comprehensions (3.X, 2.7)
#

print({x ** 2 for x in L})       # set:  {1, 36, 9, 16, 25, 4} in 3.X, set(...) in 2.X

print({x: x ** 2 for x in L})    # dict: {1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 6: 36}


#--------------------------------------------------------------
# (L + M): print pairwise sums of two vectors: 8 10 12 14 16 18
#--------------------------------------------------------------

for i in range(len(L)):
    print(L[i] + M[i])                      

for (x, y) in zip(L, M):                        # zip is a generator in 3.X
    print(x + y)


#----------------------------------------------------------------------
# (N = L + M): create new pairwise sums vector: [8, 10, 12, 14, 16, 18]
#----------------------------------------------------------------------

N = []
for i in range(len(L)): N.append(L[i] + M[i])
print(N)

N = []
for (x, y) in zip(L, M): N.append(x + y)         # zip is a generator in 3.X
print(N)


N = [L[i] + M[i] for i in range(len(L))]
print(N)                                 

N = [x + y for (x, y) in zip(L, M)]
print(N)                                  


#
# other similar ops
#

print([x * y for (x, y) in zip(L, M)])           # [7, 16, 27, 40, 55, 72]

print([y / x for (x, y) in zip(L, M)])           # [7.0, 4.0, 3.0, 2.5, 2.2, 2.0] (3.X)

print([y // x for (x, y) in zip(L, M)])          # [7, 4, 3, 2, 2, 2]
   
print(list( map((lambda x, y: x * y), L, M) ))   # [7, 16, 27, 40, 55, 72]



######################################################################################
# Matrixes: 2D lists (original code) 
######################################################################################


def init():
    global M, N        # reset state for new tests

    M = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]

    N = [[10, 20, 30],
         [40, 50, 60],
         [70, 80, 90]]


#---------------------------------------------------------------
# (M ** 2): print squares of one matrix: 1 4 9 16 25 36 49 64 81
#---------------------------------------------------------------

init()
for i in range(3):
    for j in range(3):
        print(M[i][j] ** 2)

for row in M:
    for col in row:                      # generalized
        print(col ** 2)


#----------------------------------------------------------------------------
# (M **= 2): in-place matrix squares: [[1, 4, 9], [16, 25, 36], [49, 64, 81]]
#----------------------------------------------------------------------------

init()
for i in range(3):
    for j in range(3):
        M[i][j] **= 2
print(M)

init()
for i in range(len(M)):                  # generalized
    for j in range(len(M[i])):
        M[i][j] **= 2
print(M)


#-------------------------------------------------------------------
# similar, but make new 1D vector: [1, 4, 9, 16, 25, 36, 49, 64, 81]
#-------------------------------------------------------------------

init()
print( [col ** 2 for row in M for col in row] )

print( [M[i][j] ** 2 for i in range(len(M)) for j in range(len(M[i]))] )


#--------------------------------------------------------------------------------
# (X = M ** 2): new 2D matrix of squares: [[1, 4, 9], [16, 25, 36], [49, 64, 81]]
#--------------------------------------------------------------------------------

X = [] 
for i in range(len(M)):
    row = []
    for j in range(len(M[i])):
        row.append(M[i][j] ** 2)
    X.append(row)
print(X)

X = [] 
for row in M:
    tmp = []
    for col in row:
        tmp.append(col ** 2)
    X.append(tmp)
print(X)


#
# nest comprehensions for 2D data
#

print( [[M[i][j] ** 2 for j in range(len(M[i]))] for i in range(len(M))] )

print( [[col ** 2 for col in row] for row in M] )


#-------------------------------------------------------------------------------------
# (X = M + N): new matrix of pairwise sums: [[11, 22, 33], [44, 55, 66], [77, 88, 99]]
#-------------------------------------------------------------------------------------

X = [] 
for i in range(len(M)):
    row = []
    for j in range(len(M[i])):
        row.append(M[i][j] + N[i][j])
    X.append(row)
print(X)

X = [] 
for (row1, row2) in zip(M, N):                      # zip is a generator in 3.X 
    tmp = []
    for (col1, col2) in zip(row1, row2):
        tmp.append(col1 + col2)
    X.append(tmp)
print(X)


#
# nest comprehensions for 2D data
#

print( [[M[i][j] + N[i][j] for j in range(3)] for i in range(3)] )

print( [[col1 + col2 for (col1, col2) in zip(row1, row2)] for (row1, row2) in zip(M, N)] )


# end