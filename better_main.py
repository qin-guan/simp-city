from random import choice as randchoice
from json import loads as jsonload
from json import dumps as jsondump

# All game data is stored in the game state
# Game state is mutable, a copy of DEFAULT_STATE should be made
DEFAULT_STATE = {
    # Game configs
    "config": {
        # Coordinates entered by the user MUST be between these bounds
        "x_lower": ord("a"),
        "x_upper": ord("d"),
        "y_lower": 1,
        "y_upper": 4,
        # Default value for front spacing in fmt
        "fmt_front_spacing": 3
    },
    # Turn count
    "turn": 1,
    # Available buildings left
    "b_avail": {"BCH": 8, "FAC": 8, "HSE": 8, "SHP": 8, "HWY": 8},
    # Grid, uses None for default values
    "grid": [["HWY", "HWY", "HWY", None],
             [None, None, None, None],
             [None, None, None, None],
             ["HWY", None, "HWY", "HWY"]],
    # For storing buildings generated from turns
    "tmp_buildings": [None, None],
}


#     ___
#    / __)       _
#  _| |__ ____ _| |_
# (_   __)    (_   _)
#   | |  | | | || |_
#   |_|  |_|_|_| \__)

# Returns the string of a row
def fmt_row(idx, row, state=None):
    if state is None:
        state = DEFAULT_STATE
    return " " * state["config"]["fmt_front_spacing"] + "+" + "-----+" * len(row) + "\n{:>2s} |".format(
        str(idx)) + "|".join(
        "{:^5s}".format(str(v) if v is not None else "") for v in row) + "|"


# Returns the string of a grid
def fmt_grid(state=None):
    if state is None:
        state = DEFAULT_STATE
    return " " * (state["config"]["fmt_front_spacing"] + 1) + " ".join(
        "{:^5s}".format(chr(v + 65)) for v in range(len(state["grid"][0]))) + "\n" + "\n".join(
        fmt_row(idx + 1, r) for idx, r in enumerate(state["grid"])) + "\n" + " " * state["config"][
               "fmt_front_spacing"] + "+" + "-----+" * len(state["grid"][0])


# Returns the string of available buildings
def fmt_bavail(state=None):
    if state is None:
        state = DEFAULT_STATE
    return "{:20s}{}\n{:20s}{}\n".format("Building", "Remaining", len("Building") * "-",
                                         len("Remaining") * "-") + "\n".join(
        "{:20s}{}".format(b, p) for b, p in state["b_avail"].items())


# Returns the string of available points left
def fmt_points(points):
    return "\n".join(
        "{}: {} = {}".format(k, " + ".join(str(i) for i in v), sum(v)) if sum(v) > 0 else
        "{}: 0".format(k) for k, v in
        points.items())


def fmt_leaderboard(leaderboard=None):
    if leaderboard is None:
        leaderboard = []
    return "--------- HIGH SCORES ---------\n" + \
           "{:>3s} {:21s} {:>5s}\n{:>3s} {:21s} {:>5s}\n".format(
               "Pos", "Player", "Score",
               len("Pos") * "-", len("Player") * "-", len("Score") * "-") + "\n".join(
        "{:>3s} {:21s} {:>5s}".format(str(idx + 1), kv["name"], str(kv["score"]))
        for idx, kv in enumerate(leaderboard)) + "\n-------------------------------"


#  _
# (_)
#  _  ___
# | |/ _ \
# | | |_| |
# |_|\___/

# Get coordinates from user
def io_get_coord(state=None):
    if state is None:
        state = DEFAULT_STATE
    i = list(input("Build where? "))

    if not len(i) == 2 or not i[0].isalpha() or not i[1].isdigit():
        return False

    x, y = ord(i[0]), int(i[1])

    if state["config"]["x_lower"] <= x <= state["config"]["x_upper"] and \
            state["config"]["y_lower"] <= y <= state["config"]["y_upper"]:
        return [x - state["config"]["x_lower"], y - state["config"]["y_lower"]]
    else:
        return False


# Get choice from user
# i - input message
# l - lower bound (inclusive)
# u - upper bound (inclusive)
def io_get_choice(i, l, u):
    c = input(i)
    if not c.isdigit():
        return False
    c = int(c)
    if l <= c <= u:
        return c
    else:
        return False


def io_put_state(state=None):
    if state is None:
        state = DEFAULT_STATE
    with open("data", "w") as o:
        o.write(jsondump(state, sort_keys=True, indent=4))


def io_get_state():
    try:
        with open("data", "r") as i:
            return jsonload(i.read())
    except:
        return False


def io_put_leaderboard(state=None, leaderboard=None):
    if leaderboard is None:
        leaderboard = []
    if state is None:
        state = DEFAULT_STATE
    try:
        with open("leaderboard", "r") as i:
            file = jsonload(i.read())
    except:
        file = {}
    with open("leaderboard", "w") as o:
        file["{},{}".format(len(state['grid']), len(state['grid'][0]))] = leaderboard
        o.write(jsondump(file, sort_keys=True, indent=4))


def io_get_leaderboard(state=None):
    if state is None:
        state = DEFAULT_STATE
    try:
        with open("leaderboard", "r") as i:
            return jsonload(i.read())["{},{}".format(len(state['grid']), len(state['grid'][0]))]
    except:
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

def points_bch(state=None):
    if state is None:
        state = DEFAULT_STATE
    p = []
    for row in state["grid"]:
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


def points_fac(state=None):
    if state is None:
        state = DEFAULT_STATE
    fac_c = 0
    for row in state["grid"]:
        for col in row:
            if col == "FAC":
                fac_c += 1
    p = []
    if fac_c <= 4:
        p += [fac_c for _ in range(fac_c)]
    else:
        p = [4, 4, 4, 4] + [1 for _ in range(fac_c - 4)]
    return p


def points_hse(state=None):
    if state is None:
        state = DEFAULT_STATE
    p = []
    for y, row in enumerate(state["grid"]):
        for x, col in enumerate(row):
            if not col == "HSE":
                continue
            adj = game_adj(x, y, state)
            if "FAC" in adj:
                p.append(1)
                continue
            temp_p = adj.count("HSE") + adj.count("SHP") + 2 * adj.count("BCH")
            if not temp_p == 0:
                p.append(temp_p)
    return p


def points_shp(state=None):
    if state is None:
        state = DEFAULT_STATE
    p = []
    for y, row in enumerate(state["grid"]):
        for x, col in enumerate(row):
            if not col == "SHP":
                continue
            adj = game_adj(x, y, state)
            unique_c = len(list(set(adj)))
            if unique_c > 0:
                p.append(unique_c)
    return p


def points_hwy(state=None):
    if state is None:
        state = DEFAULT_STATE
    p = []
    for y, row in enumerate(state["grid"]):
        count = 1
        for x, col in enumerate(row):
            if not col == "HWY":
                continue
            if x + 1 < len(row) and row[x + 1] == "HWY":
                count += 1
            else:
                p += [count for _ in range(count)]
                count = 1
    return p


#   ____ _____ ____  _____
#  / _  (____ |    \| ___ |
# ( (_| / ___ | | | | ____|
#  \___ \_____|_|_|_|_____)
# (_____|


def game_adj(x, y, state=None):
    if state is None:
        state = DEFAULT_STATE

    grid = state["grid"]

    adj = []
    top = y - 1 if y - 1 >= 0 else False
    if top is not False and grid[top][x] is not None:
        adj.append(grid[top][x])

    bottom = y + 1 if y + 1 < len(grid) else False
    if bottom is not False and grid[bottom][x] is not None:
        adj.append(grid[bottom][x])

    left = x - 1 if x - 1 >= 0 else False
    if left is not False and grid[y][left] is not None:
        adj.append(grid[y][left])

    right = x + 1 if x + 1 < len(grid[0]) else False
    if right is not False and grid[y][right] is not None:
        adj.append(grid[y][right])

    return adj


def game_build(x, y, building, skip_validation=False, state=None):
    if state is None:
        return False
    if not skip_validation:
        d = state["grid"]

        # Building already exists
        if d[y][x] is not None:
            return False

        adj = game_adj(x, y, state)
        if len(adj) == 0:
            return False

    state["grid"][y][x] = building
    return True


# This represents a turn in the game
# Returns a number
# 0 - Completed round
# 1 - Game over
# 2 - Exit to main menu
def game_turn(points, state=None):
    if state is None:
        state = DEFAULT_STATE
    if state["turn"] == len(state["grid"]) * len(state["grid"][0]) + 1:
        return 1

    print("Turn {}".format(state["turn"]))

    print(fmt_grid(state))
    if state["tmp_buildings"][0] is None:
        state["tmp_buildings"] = game_get_buildings(state)

    print("1. Build a {}".format(state["tmp_buildings"][0]))
    print("2. Build a {}".format(state["tmp_buildings"][1]))
    print("3. See remaining buildings")
    print("4. See current score")
    print()
    print("5. Save game")
    print("0. Exit to main menu")

    while True:
        choice = io_get_choice("Your choice? ", 0, 5)
        if choice is not False:
            break
        print("Oh no! that's an invalid choice, please choose again.")

    if choice == 0:
        return 2

    elif choice == 1 or choice == 2:
        while True:
            coords = io_get_coord(state)
            if coords is not False:
                break
            print("Oh no! That's an invalid coordinate, please enter again in the form of <x><y>")

        [x, y] = coords
        ok = game_build(x, y, state["tmp_buildings"][choice - 1], state["turn"] == 1, state)

        if not ok:
            print("You must build next to an existing building.")
        else:
            state["turn"] += 1
            state["b_avail"][state["tmp_buildings"][choice - 1]] -= 1
            state["tmp_buildings"] = [None, None]

    elif choice == 3:
        print()
        print(fmt_bavail(state))

    elif choice == 4:
        p = {}
        for k, v in points.items():
            p[k] = v(state)
        print(fmt_points(p))

    elif choice == 5:
        io_put_state(state)
        print("Game saved!")

    return 0


def game_get_buildings(state=None):
    if state is None:
        state = DEFAULT_STATE
    r1 = randchoice(list(state["b_avail"].keys()))
    r2 = randchoice(list(state["b_avail"].keys()))
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

    while True:
        print("1. Start new game")
        print("2. Load saved game")
        print("3. Show high scores")
        print()
        print("0. Exit")

        while True:
            choice = io_get_choice("Your choice? ", 0, 3)
            if choice is not False:
                break
            print("Oh no! That's an invalid choice, please choose again.")

        # Exit
        if choice == 0:
            system_exit()

        # Load saved game
        if choice == 2:
            state = io_get_state()
            # If load failed
            if not state:
                state = DEFAULT_STATE.copy()

        # Show high scores
        elif choice == 3:
            state = DEFAULT_STATE.copy()
            print("Which city size's scoreboard do you want to see?")
            while True:
                x = io_get_choice("Enter number of columns: ", 1, 26)
                if x is not False:
                    break
                print("Oh no! that's an invalid choice, please choose again.")

            while True:
                y = io_get_choice("Enter number of rows: ", 1, 99)
                if y is not False:
                    break
                print("Oh no! that's an invalid choice, please choose again.")

            # Create grid
            grid = []
            for _ in range(y):
                row = []
                for _ in range(x):
                    row.append(None)
                grid.append(row)
            state["grid"] = grid

            leaderboard = io_get_leaderboard(state)
            if not leaderboard:
                io_put_leaderboard(state, [])
                leaderboard = io_get_leaderboard(state)
            print(fmt_leaderboard(leaderboard))

            continue

        else:
            # Create copy of state
            state = DEFAULT_STATE.copy()

            # print("Choose city size:")
            # print("1. Default")
            # print("2. Custom")
            # print()
            # print("0. Exit")
            #
            # while True:
            #     choice = io_get_choice("Your choice? ", 0, 2)
            #     if choice is not False:
            #         break
            #     print("Oh no! that's an invalid choice, please choose again.")
            #
            # # Exit
            # if choice == 0:
            #     system_exit()
            #
            # # Custom
            # elif choice == 2:
            #     while True:
            #         x = io_get_choice("Enter number of columns: ", 1, 26)
            #         if x is not False:
            #             break
            #         print("Oh no! that's an invalid choice, please choose again.")
            #
            #     while True:
            #         y = io_get_choice("Enter number of rows: ", 1, 99)
            #         if y is not False:
            #             break
            #         print("Oh no! that's an invalid choice, please choose again.")
            #
            #     # Set bounds for input validation
            #     state["config"]["x_upper"] = state["config"]["x_lower"] + x - 1
            #     state["config"]["y_upper"] = y
            #
            #     # Create grid
            #     grid = []
            #     for _ in range(y):
            #         row = []
            #         for _ in range(x):
            #             row.append(None)
            #         grid.append(row)
            #     state["grid"] = grid

        # Set point functions
        points = {
            "BCH": points_bch,
            "FAC": points_fac,
            "HSE": points_hse,
            "SHP": points_shp,
            "HWY": points_hwy,
        }

        while True:
            code = game_turn(points, state)
            if not code == 0:
                break

        # Game over
        if code == 1:
            print("Final layout of Simp City:")
            print(fmt_grid(state))
            p = {}  # points dictionary
            s = 0  # sum of points
            # Run all point functions
            for k, v in points.items():
                point = v(state)
                # Store points
                p[k] = point
                # Sum points
                s += sum(point)

            print(fmt_points(p))
            print("Total score: {}".format(s))

            # Get leaderboard
            leaderboard = io_get_leaderboard(state)
            if not leaderboard:
                leaderboard = []

            # Sort leaderboard by descending order
            leaderboard.sort(key=lambda i: i.get("score"), reverse=True)
            pos = -1
            for idx, item in enumerate(leaderboard):  # Check if there are smaller values in the list
                if item["score"] >= s:
                    continue
                pos = idx
                break
            # If the length of the leaderboard is less than 10 and the score is lower than all scores, the position
            # is the last
            if len(leaderboard) < 10 and pos == -1:
                pos = len(leaderboard)

            if not pos == -1:
                print("Congratulations! You made the high score board at position {}!".format(pos + 1))
                while True:
                    name = input("Please enter your name (max 20 chars): ")
                    if len(name) <= 20:
                        break
                leaderboard.insert(pos, {"name": name, "score": s})
                # Remove scores > 10
                while len(leaderboard) > 10:
                    leaderboard.pop()

                print(fmt_leaderboard(leaderboard))
                io_put_leaderboard(state, leaderboard)

            system_exit()

        # Exit to main menu
        elif code == 2:
            continue


main()
