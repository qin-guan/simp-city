from random import choice as randchoice

DEFAULT_GRID = [[None, None, None, None],
                [None, None, None, None],
                [None, None, None, None],
                [None, None, None, None]]
DEFAULT_X_LOWER = ord("a")  # 97
DEFAULT_X_UPPER = ord("d")  # 100
DEFAULT_Y_LOWER = 1
DEFAULT_Y_UPPER = 4
DEFAULT_BAVAIL = {"BCH": 8, "FAC": 8, "HSE": 8, "SHP": 8, "HWY": 8}
DEFAULT_GAME_STATE = {
    "turn": 1,
    "bavail": DEFAULT_BAVAIL.copy(),
    "data": DEFAULT_GRID[:]
}


#     ___
#    / __)       _
#  _| |__ ____ _| |_
# (_   __)    (_   _)
#   | |  | | | || |_
#   |_|  |_|_|_| \__)

def fmt_row(idx, row):
    return "  +" + "-----+" * len(row) + "\n{} |".format(idx) + "|".join(
        "{:^5s}".format(str(v) if v is not None else "") for v in row) + "|"


def fmt_grid(grid=None):
    if grid is None:
        grid = DEFAULT_GRID
    return "   " + " ".join("{:^5s}".format(chr(v + 65)) for v in range(len(grid[0]))) + "\n" + "\n".join(
        fmt_row(idx + 1, r) for idx, r in enumerate(grid)) + "\n  +" + "-----+" * len(grid[0])


def fmt_bavail(bavail):
    return "{:20s}{}\n{:20s}{}\n".format("Building", "Remaining", len("Building") * "-",
                                         len("Remaining") * "-") + "\n".join(
        "{:20s}{}".format(b, p) for b, p in bavail.items())


def fmt_points(points):
    return "\n".join(
        "{}: {} = {}".format(k, " + ".join(str(i) for i in v), sum(v)) if sum(v) > 0 else
        "{}: 0".format(k) for k, v in
        points.items())


#  _
# (_)
#  _  ___
# | |/ _ \
# | | |_| |
# |_|\___/

def io_get_coord(x1=DEFAULT_X_LOWER, x2=DEFAULT_X_UPPER, y1=DEFAULT_Y_LOWER, y2=DEFAULT_Y_UPPER):
    i = list(input("Build where? "))
    if not len(i) == 2 or not i[0].isalpha() or not i[1].isdigit():
        return False
    x, y = ord(i[0]), int(i[1])
    if x1 <= x <= x2 and y1 <= y <= y2:
        return [x, y]
    else:
        return False


def io_get(i, l, u):
    c = input(i)
    if not c.isdigit():
        return False
    c = int(c)
    if l <= c <= u:
        return c
    else:
        return False


#                    _
#   ___ _   _  ___ _| |_ _____ ____
#  /___) | | |/___|_   _) ___ |    \
# |___ | |_| |___ | | |_| ____| | | |
# (___/ \__  (___/   \__)_____)_|_|_|
#      (____/

def system_exit():
    print("Goodbye!")
    exit()


#              _
#             (_)       _
#  ____   ___  _ ____ _| |_  ___
# |  _ \ / _ \| |  _ (_   _)/___)
# | |_| | |_| | | | | || |_|___ |
# |  __/ \___/|_|_| |_| \__|___/
# |_|

def points_bch(grid=None):
    if grid is None:
        grid = DEFAULT_GRID
    p = []
    for row in grid:
        if "BCH" not in row:
            continue
        for idx, col in enumerate(row):
            if not col == "BCH":
                continue
            if idx == 0 or idx == 3:
                p.append(3)
            else:
                p.append(3)
    return p


def points_fac(grid=None):
    if grid is None:
        grid = DEFAULT_GRID
    fac_c = 0
    for row in grid:
        for col in row:
            if col == "FAC":
                fac_c += 1
    p = []
    if fac_c <= 4:
        p += [fac_c for _ in range(fac_c)]
    else:
        p = [4, 4, 4, 4] + [1 for _ in range(fac_c - 4)]
    return p


def points_hse(grid=None):
    if grid is None:
        grid = DEFAULT_GRID
    p = []
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if not col == "HSE":
                continue
            adj = game_adj(x + DEFAULT_X_LOWER, y + DEFAULT_Y_LOWER, grid)
            if "FAC" in adj:
                p.append(1)
                continue
            temp_p = adj.count("HSE") + adj.count("SHP") + 2 * adj.count("BCH")
            if not temp_p == 0:
                p.append(temp_p)
    return p


def points_shp(grid=None):
    if grid is None:
        grid = DEFAULT_GRID
    p = []
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if not col == "SHP":
                continue
            adj = game_adj(x + DEFAULT_X_LOWER, y + DEFAULT_Y_LOWER, grid)
            unique_c = len(list(set(adj)))
            if unique_c > 0:
                p.append(unique_c)
    return p


def points_hwy(grid=None):
    if grid is None:
        grid = DEFAULT_GRID
    p = []
    for row in enumerate(grid):
        temp_p = row.count("HWY")
        if not temp_p == 0:
            p.append(temp_p)
    return p


#   ____ _____ ____  _____
#  / _  (____ |    \| ___ |
# ( (_| / ___ | | | | ____|
#  \___ \_____|_|_|_|_____)
# (_____|


def game_adj(x, y, grid=None):
    if grid is None:
        grid = DEFAULT_GRID

    adj = []
    top = y - DEFAULT_Y_LOWER - 1 if y - DEFAULT_Y_LOWER - 1 >= 0 else False
    if top is not False and grid[top][x - DEFAULT_X_LOWER] is not None:
        adj.append(grid[top][x - DEFAULT_X_LOWER])

    bottom = y - DEFAULT_Y_LOWER + 1 if y - DEFAULT_Y_LOWER + 1 < DEFAULT_Y_UPPER else False
    if bottom is not False and grid[bottom][x - DEFAULT_X_LOWER] is not None:
        adj.append(grid[bottom][x - DEFAULT_X_LOWER])

    left = x - DEFAULT_X_LOWER - 1 if x - DEFAULT_X_LOWER - 1 >= 0 else False
    if left is not False and grid[y - DEFAULT_Y_LOWER][left] is not None:
        adj.append(grid[y - DEFAULT_Y_LOWER][left])

    right = x - DEFAULT_X_LOWER + 1 if x - DEFAULT_X_LOWER + 1 <= DEFAULT_X_UPPER - DEFAULT_X_LOWER else False
    if right is not False and grid[y - DEFAULT_Y_LOWER][right] is not None:
        adj.append(grid[y - DEFAULT_Y_LOWER][right])

    return adj


def game_build(x, y, building, skip_validation=False, state=None):
    if state is None:
        return False
    if not skip_validation:
        d = state["data"]
        # Building already exists
        if d[y - DEFAULT_Y_LOWER][x - DEFAULT_X_LOWER] is not None:
            return False

        adj = game_adj(x, y, state["data"])
        if len(adj) == 0:
            return False

    state["data"][y - DEFAULT_Y_LOWER][x - DEFAULT_X_LOWER] = building
    return True


def game_turn(points, state=None):
    if state is None:
        state = DEFAULT_GAME_STATE
    print("Turn {}".format(state["turn"]))
    print(fmt_grid(state["data"]))
    rs = game_get_buildings()
    print("1. Build a {}".format(rs[0]))
    print("2. Build a {}".format(rs[1]))
    print("3. See remaining buildings")
    print("4. See current score")
    print()
    print("5. Save game")
    print("0. Exit to main menu")
    while True:
        choice = io_get("Your choice? ", 0, 5)
        if choice is not False:
            break
        print("Oh no! that's an invalid choice, please choose again.")
    if choice == 0:
        return True
    elif choice == 1 or choice == 2:
        while True:
            coords = io_get_coord()
            if coords is not False:
                break
            print("Oh no! That's an invalid coordinate, please enter again in the form of <x><y>")

        [x, y] = coords
        ok = game_build(x, y, rs[choice - 1], state["turn"] == 1, state)
        if not ok:
            print("You must build next to an existing building.")
        else:
            state["turn"] += 1
            state["bavail"][rs[choice - 1]] -= 1
            if state["turn"] == len(DEFAULT_GRID) * len(DEFAULT_GRID[0]) + 1:
                return True

    elif choice == 3:
        print()
        print(fmt_bavail(state["bavail"]))

    elif choice == 4:
        p = {}
        for k, v in points.items():
            p[k] = v(state["data"])
        print(fmt_points(p))

    else:
        return True


def game_get_buildings():
    r1 = randchoice(list(DEFAULT_BAVAIL.keys()))
    r2 = randchoice(list(DEFAULT_BAVAIL.keys()))
    return [r1, r2]


#              _
#             (_)
#  ____  _____ _ ____
# |    \(____ | |  _ \
# | | | / ___ | | | | |
# |_|_|_\_____|_|_| |_|

def main():
    print("Welcome, mayor of Simp City!")
    print("----------------------------")
    print("1. Start new game")
    print("2. Load saved game")
    print()
    print("0. Exit")
    while True:
        choice = io_get("Your choice? ", 0, 2)
        if choice is not False:
            break
        print("Oh no! That's an invalid choice, please choose again.")
    if choice == 0:
        system_exit()
    elif choice == 1:
        state = DEFAULT_GAME_STATE.copy()
        points = {
            "BCH": points_bch,
            "FAC": points_fac,
            "HSE": points_hse,
            "SHP": points_shp,
            "HWY": points_hwy,
        }
        while True:
            done = game_turn(points, state)
            if done:
                break

        if state["turn"] == len(DEFAULT_GRID) * len(DEFAULT_GRID[0]) + 1:
            print("Final layout of Simp City:")
            print(fmt_grid(state["data"]))
            p = {}
            s = 0
            for k, v in points.items():
                point = v(state["data"])
                p[k] = point
                s += sum(point)

            print(fmt_points(p))
            print("Total score: {}".format(s))

        system_exit()
    else:
        print("not implemented")


main()
