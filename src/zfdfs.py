
def is_direct_connected(g, i1, j1, i2, j2):
    if i1 == i2:
        if j1 > j2:
            j1, j2 = j2, j1
        for j in range(j1 + 1, j2):
            if g[i1][j] > -1:
                return False
        return True
    else:
        if i1 > i2:
            i1, i2 = i2, i1
        for i in range(i1 + 1, i2):
            if g[i][j1] > -1:
                return False
        return True

def is_connected(g, i1, j1, i2, j2):
    rows = len(g)
    cols = len(g[0])

    if j1 > j2:
        i1, i2 = i2, i1
        j1, j2 = j2, j1

    if i1 == i2 or j1 == j2:
        if is_direct_connected(g, i1, j1, i2, j2):
            return True

    for i in range(0, rows):
        if i == i1:
            if g[i][j2] < 0 and is_direct_connected(g, i1, j1, i, j2) and is_direct_connected(g, i, j2, i2, j2):
                return True
        elif i == i2:
            if g[i][j1] < 0 and is_direct_connected(g, i1, j1, i, j1) and is_direct_connected(g, i, j1, i2, j2):
                return True
        else:
            if g[i][j1] < 0 and g[i][j2] < 0 and is_direct_connected(g, i1, j1, i, j1) and is_direct_connected(g, i, j1, i, j2) and is_direct_connected(g, i, j2, i2, j2):
                return True

    for j in range(0, cols):
        if j == j1:
            if g[i2][j] < 0 and is_direct_connected(g, i1, j1, i2, j) and is_direct_connected(g, i2, j, i2, j2):
                return True
        elif j == j2:
            if g[i1][j] < 0 and is_direct_connected(g, i1, j1, i1, j) and is_direct_connected(g, i1, j, i2, j2):
                return True
        else:
            if g[i1][j] < 0 and g[i2][j] < 0 and is_direct_connected(g, i1, j1, i1, j) and is_direct_connected(g, i1, j, i2, j) and is_direct_connected(g, i2, j, i2, j2):
                return True

    return False