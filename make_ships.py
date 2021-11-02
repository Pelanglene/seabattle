go_x = [-1, 0, 1, 0]
go_y = [0, 1, 0, -1]
used = [0] * 100
boats = [0] * 100
hboat = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
pboat = [set() for i in range(11)]


def valid(x, y):
    return -1 < x < 10 and -1 < y < 10


def dfs(node, cnt, field):
    global used
    used[node] = cnt
    x = node // 10
    y = node % 10
    for i in range(4):
        _x = x + go_x[i]
        _y = y + go_y[i]
        to = _x * 10 + _y
        if valid(_x, _y) and field[to] == '#' and not used[to]:
            dfs(to, cnt, field)


def index_maps(my_map):
    global used
    cnt = 1
    used = [0] * 100
    for i in range(100):
        if my_map[i] == '#' and not used[i]:
            dfs(i, cnt, my_map)
            cnt += 1
    for i in range(100):
        if my_map[i] != '#':
            continue
        boats[i] = used[i]
        hboat[used[i]] += 1
        pboat[used[i]].add(i)


def make(mp):
    global used, boats, hboat, pboat
    used = [0] * 100
    boats = [0] * 100
    hboat = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    pboat = [set() for j in range(11)]
    index_maps(mp)
    return boats, hboat, pboat