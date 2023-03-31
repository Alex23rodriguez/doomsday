from threading import Timer
from time import time
from collections.abc import Callable


def setTimeout(fn, secs, *args, **kwargs):
    t = Timer(secs, fn, args=args, kwargs=kwargs)
    t.start()


def countdown_done(game: "Game"):
    game.timeup = True
    print("\n\r-------TIME'S UP!!-------")  # , end="")


gamemodestr = """t: timed mode. game ends when timer runs out
n: number of questions mode. game ends when a certain number of questions, regardless of right or wrong answer
s: score mode. game ends when a certain score is reached
m: mistake mode. game ends when a certain number of errors are made
c: consecutive mode. game ends after correctly answering n questions in a row
mode: """, [
    "t",
    "n",
    "s",
    "m",
    "c",
]


def getmainmode():
    # main game mode
    print("enter mode:")
    prompt, ans = gamemodestr
    mode = input(prompt)
    while mode not in ans:
        print("\noption not found")
        mode = input("mode: ")
    print()

    # parameter for main game mode
    if mode == "t":
        param = getparam("Enter max time in minutes", int)
    elif mode == "n":
        param = getparam("Enter max questions", int)
    elif mode == "s":
        param = getparam("Enter max score", int)
    elif mode == "m":
        param = getparam("Enter max mistakes", int)
    elif mode == "c":
        param = getparam("Enter num of consecutive answers", int)
    else:
        raise Exception("submode not found")
    return mode, param


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


class Game:
    def __init__(self, update: Callable[[], bool], greeting="Welcome!"):
        self.greeting = greeting
        self.update = update
        self._reset()

    def _reset(self):
        self.score = 0
        self.mistakes = 0
        self.streak = 0
        self.starttime = time()

        self.timeup = False

    def start(self):
        self._reset()
        self.gamemode, self.param = getmainmode()

        if self.gamemode == "t":
            setTimeout(countdown_done, self.param * 60, self)

        while not self._done():
            correct = self.update()
            if not self.timeup:
                if correct:
                    self.score += 1
                    self.streak += 1
                else:
                    self.mistakes += 1
                    self.streak = 0
            else:
                print("ans not added because timeout")  ## TODO remove line

        print("===stats===")
        t = int(time() - self.starttime)
        print(f"time:\t{t//60} mins {t%60} seconds")
        print(f"score:\t{self.score}")
        print(f"errors:\t{self.mistakes}")

    def _done(self):
        return (
            (self.gamemode == "t" and self.timeup)
            or (self.gamemode == "s" and self.param == self.score)
            or (self.gamemode == "m" and self.param == self.mistakes)
            or (self.gamemode == "n" and self.param == self.score + self.mistakes)
            or (self.gamemode == "c" and self.param == self.streak)
        )
