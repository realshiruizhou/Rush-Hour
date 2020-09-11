from collections import deque
import time
size = 6
count = 0
ref = "ABCDEFGHIJKLMNO"


class Node:
    def __init__(self, state, path_length):
        self.path_length = path_length
        self.state = state

    def get_path_length(self):
        return self.path_length

    def get_state(self):
        return self.state


def display(state):
    count = 1
    for a in state:
        if count % size == 0:
            print(a + " ")
        else:
            print(a + " ", end="", flush=True)
        count += 1


def get_coordinate(index):
    x = index // size
    y = index % size
    return x, y


def get_index(x, y):
    index = 0
    index += size * x
    index += y
    return index


def add_red(state, col):
    i = get_index(2, col)
    b = state
    for a in range(0, 2):
        b = add(b, i - a, "R")
    return b


def add_horizontal(state, row, col, length):
    i = get_index(row, col)
    b = state
    for a in range(0, length):
        b = add(b, i - a, ref[count])
    return b


def add_vertical(state, row, col, length):
    b = state
    for a in range(0, length):
        n = get_index(row + a, col)
        b = add(b, n, ref[count])
    return b


def add(state, ind, letter):
    temp = list(state)
    temp[ind] = letter
    return ''.join(temp)


def get_children(state):
    children = []
    for a in range(0, size * size):
        eligible = set()
        if state[a] == "0":
            continue
        (x, y) = get_coordinate(a)
        if (x + 1) < size and (x - 1) >= 0:
            if state[get_index(x + 1, y)] == state[a] and state[get_index(x - 1, y)] == "0":
                eligible.add("up")
            elif state[get_index(x - 1, y)] == state[a] and state[get_index(x + 1, y) == "0"]:
                eligible.add("down")
        if (y - 1) >= 0 and (y + 1) < size:
            if state[get_index(x, y - 1)] == state[a] and state[get_index(x, y + 1) == "0"]:
                eligible.add("right")
            if state[get_index(x, y + 1)] == state[a] and state[get_index(x, y - 1) == "0"]:
                eligible.add("left")
        if "right" in eligible:
            count = 1
            while y + count < size and state[get_index(x, y + count)] == "0":
                children.append(move_right(state, a, get_index(x, y + count)))
                count += 1
        if "left" in eligible:
            count = 1
            while y - count >= 0 and state[get_index(x, y - count)] == "0":
                children.append(move_left(state, a, get_index(x, y - count)))
                count += 1
        if "down" in eligible:
            count = 1
            while x + count < size and state[get_index(x + count, y)] == "0":
                children.append(move_down(state, a, get_index(x + count, y)))
                count += 1
        if "up" in eligible:
            count = 1
            while x - count >= 0 and state[get_index(x - count, y)] == "0":
                children.append(move_up(state, a, get_index(x - count, y)))
                count += 1
    return children


def move_left(state, c, n):
    letter = state[c]
    move = state
    l = 2
    move = erase(move, c)
    move = erase(move, c + 1)
    if c + 2 < size and state[c + 2] == letter:
        l += 1
        move = erase(move, c + 2)
    for a in range(0, l):
        move = add(move, n + a, letter)
    return move


def move_down(state, c, n):
    letter = state[c]
    move = state
    l = 2
    move = erase(move, c)
    move = erase(move, c - size)
    if c - (size * 2) >= 0 and state[c - (size * 2)] == letter:
        l += 1
        move = erase(move, c - (size * 2))
    for a in range(0, l):
        move = add(move, n - (a * size), letter)
    return move


def move_up(state, c, n):
    letter = state[c]
    move = state
    l = 2
    move = erase(move, c)
    move = erase(move, c + size)
    if c + (size * 2) < 36 and state[c + (size * 2)] == letter:
        l += 1
        move = erase(move, c + (size * 2))
    for a in range(0, l):
        move = add(move, n + (a * size), letter)
    return move


def move_right(state, c, n):
    letter = state[c]
    move = state
    l = 2
    move = erase(move, c)
    move = erase(move, c - 1)
    if c - 2 >= 0 and state[c + 2] == letter:
        l += 1
        move = erase(move, c - 2)
    for a in range(0, l):
        move = add(move, n - a, letter)
    return move


def erase(state, e):
    temp = list(state)
    temp[e] = "0"
    return ''.join(temp)


def bfs(state):
    start = Node(state, 0)
    fringe = deque()
    fringe.appendleft(start)
    visited = set()
    while len(fringe) != 0:
        v = fringe.pop()
        if v.get_state() in visited:
            continue
        visited.add(v.get_state())
        if v.get_state()[17] == "R":
            return v.get_path_length()
        c = get_children(v.get_state())
        temp = []
        for e in c:
            add = Node(e, v.get_path_length() + 1)
            temp.append(add)
        for a in range(0, len(c)):
            fringe.appendleft(temp[a])


# "00000000000E000RREBBBD0E00CDAA00CD00"
board = "0ABB000ACC0DRREF0D00EFGGH0EIIJHLLL0J"
display(board)
start = time.perf_counter()
steps = bfs(board)
end = time.perf_counter()
print(str(steps) + " " + str(end - start))
