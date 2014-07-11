# a numerically-inclined student asked for examples related
# to matrix processing (in the core language, not using NumPy);
# the following is a quick tour through some simple matrix code,
# showing equivalents coded in for loops and list comprehensions;

def init():
    global M, N
    M = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]

    N = [[10, 20, 30],
         [40, 50, 60],
         [70, 80, 90]]

init()
for row in M:
    for col in row:
        print(col ** 2)

for i in range(3):
    for j in range(3):
        print(M[i][j] ** 2)

init()
for i in range(3):
    for j in range(3):
        M[i][j] **= 2
print(M)

init()
for i in range(len(M)):
    for j in range(len(M[i])):
        M[i][j] **= 2
print(M)

init()
print( [col ** 2 for row in M for col in row] )

print( [M[i][j] ** 2 for i in range(len(M)) for j in range(len(M[i]))] )

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


print( [[M[i][j] ** 2 for j in range(len(M[i]))] for i in range(len(M))] )

print( [[col ** 2 for col in row] for row in M] )


X = [] 
for i in range(len(M)):
    row = []
    for j in range(len(M[i])):
        row.append(M[i][j] + N[i][j])
    X.append(row)
print(X)

X = [] 
for (row1, row2) in zip(M, N):
    tmp = []
    for (col1, col2) in zip(row1, row2):
        tmp.append(col1 + col2)
    X.append(tmp)
print(X)

print( [[M[i][j] + N[i][j] for j in range(3)] for i in range(3)] )

print( [[col1 + col2 for (col1, col2) in zip(row1, row2)] for (row1, row2) in zip(M, N)] )

