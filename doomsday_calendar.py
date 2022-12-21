from time import time
from typing import List
from datetime import datetime as dt, timedelta
from random import randint

from threading import Timer

###

# important dates:
#   2000s: Tuesday   (2)
#   2100s: Sunday    (0)
#   1800s: Friday    (5)
#   1900s: Wednesday (3)


def setTimeout(fn, secs, *args, **kwargs):
    t = Timer(secs, fn, args=args, kwargs=kwargs)
    t.start()


def countdown_done():
    global timeup, endtime
    endtime = time()
    timeup = True
    print("\n\r-------TIME'S UP!!-------")  # , end="")


###
modestr = """n: normal mode. guess a full date (default)
d: date only mode
y: year only mode
mode: """

submodestr = """n: normal mode. guess random dates for the current year and next year (default)
c: custom mode. guess random dates for custom range.
w: wide mode. guess random dates this century and the previous one
e: extreme mode. guess random dates between the year 1753 and 3000
mode: """

gamemodestr = """t: timed mode. game ends when timer runs out (default)
n: number of questions mode. game ends when a certain number of questions, regardless of right or wrong answer.
s: score mode. game ends when a certain score is reached
m: mistake mode. game ends when a certain number of errors are made 
mode: """


def getmode(ans: List[str], prompt: str):
    ans += [""]
    mode = input(prompt)
    while mode not in ans:
        print("\noption not found")
        mode = input(prompt)
    if mode == "":
        mode = ans[0]
    print()
    return mode


def getparam(prompt: str, validfunc):
    ans = None
    while ans is None:
        ans = input(prompt + ": ")
        try:
            ans = validfunc(ans)
        except Exception:
            print("invalid parameter")
            ans = None
    return ans


###


def year_range_validator(inp: str):
    x, y = inp.split(",")
    x, y = x.strip(), y.strip()
    x, y = int(x), int(y)
    return x, y


###


def main():
    print("Welcome to Doomsday Trainer")
    print("enter mode:")
    mode = getmode(["n", "d", "y"], modestr)

    if mode != "d":
        submode = getmode(["n", "c", "w", "e"], submodestr)
    else:
        submode = "d"

    if submode == "n":
        x = dt.now().year
        y = x + 1
    elif submode == "c":
        x, y = getparam(
            "enter years separated by a comma (inclusive range)",
            year_range_validator,
        )
    elif submode == "w":
        x, y = (1900, 2099)
    elif submode == "d":
        x, y = (2100, 2100)  # this year is chosen because doomsday falls on a friday
    elif submode == "e":
        x, y = (1753, 3000)
    else:
        raise Exception("submode not found")

    gamemode = getmode(["t", "n", "s", "m"], gamemodestr)

    if gamemode == "t":
        param = getparam("Enter max time in minutes", int)
    elif gamemode == "n":
        param = getparam("Enter max questions", int)
    elif gamemode == "s":
        param = getparam("Enter max score", int)
    elif gamemode == "m":
        param = getparam("Enter max mistakes", int)
    else:
        raise Exception("submode not found")

    d1, d2 = dt(x, 1, 1), dt(y, 12, 31)
    config = {
        "mode": mode,
        "submode": submode,
        "gamemode": gamemode,
        "start": d1,
        "end": d2,
        "total_days": (d2 - d1).days,
    }

    setup(config, param)
    while not done(config) and not timeup:
        update(config)

    print("===stats===")
    t = int(time() - starttime)
    print(f"time:\t{t//60} mins {t%60} seconds")
    print(f"score:\t{score}")
    print(f"errors:\t{mistakes}")


### general gameplay functions


def setup(config, param):
    global score, mistakes, starttime, endpoints, timeup

    gamemode = config["gamemode"]
    score = 0
    mistakes = 0
    timeup = False
    starttime = time()
    if gamemode == "t":
        setTimeout(countdown_done, param * 60)
        # endtime = starttime + param * 60
    else:
        endpoints = param


def done(config):
    global score, endpoints, timeup
    gamemode = config["gamemode"]
    if gamemode == "t" and timeup:
        return True
    elif gamemode == "s" and score == endpoints:
        return True
    elif gamemode == "m" and mistakes == endpoints:
        return True
    elif gamemode == "n" and mistakes + score == endpoints:
        return True
    return False


def update(config):
    """Defines functionality of the game"""
    global score, mistakes, timeup

    mode = config["mode"]
    # get random date and player input
    date = get_rand_date(config)
    if mode == "d":
        x = input(date.strftime("%d %B: "))
    elif mode == "n":
        x = input(date.strftime("%d %B, %Y: "))
    elif mode == "y":
        date = dt(date.year, 4, 4)  # get doomsday for that year
        x = input(date.strftime("%Y: "))
    else:
        raise Exception("mode not found")

    # check if on time before updating stats
    if timeup:
        return

    # update stats
    if equal(config, date, x):
        score += 1
        print("\tcorrect!")
    else:
        mistakes += 1
        print("\twrong... " + date.strftime("%A"))


def equal(config, data: dt, inpt: str):
    return data.strftime("%w") == inpt or data.strftime("%a").lower() == inpt.lower()


### specific gameplay functions


def get_rand_date(config) -> dt:
    return config["start"] + timedelta(days=randint(0, config["total_days"]))


###

if __name__ == "__main__":
    main()
