from datetime import datetime as dt, timedelta
from random import randint
from time import time


def get_rand_date(config) -> dt:
    return config["start"] + timedelta(days=randint(0, config["total_days"]))


def equal(data: dt, inpt: str):
    return data.strftime("%w") == inpt or data.strftime("%a").lower() == inpt.lower()


def isleapyear(year):
    return year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)


def explain(date):
    # 2004 is a leap year and dd is sunday, 2100 is not and dd is sunday
    day = dt(2004 if isleapyear(date.year) else 2100, date.month, date.day).strftime(
        "%d %b: %w"
    )
    cent = date.year // 100
    centd, year = [2, 0, 5, 3][(cent) % 4], date.year % 100
    a, b = year // 12, year % 12
    yearstr = f"{cent*100}: {centd}, {year-b}: {a%7}, {b}: {(b+b//4)%7}"
    ans = f"({day}, {yearstr})"
    return ans


# setup
start = dt(1800, 1, 1)
end = dt(2199, 12, 31)
config = {
    "start": start,
    "end": end,
    "total_days": (end - start).days,
    "explain": True,
}


# gameplay
def oneround():
    date = get_rand_date(config)
    x = input(date.strftime("%d %B, %Y: "))

    if x == "no time!":
        exit()
    if equal(date, x):
        print("\tcorrect!")
        return True
    else:
        ans = explain(date) if config["explain"] else ""
        print("\twrong... " + date.strftime(f"%A {ans}"))
        return False


print("answer 3 in a row to access terminal")
starttime = time()
streak = 0
corr = 0
count = 0
while True:
    count += 1
    if oneround():
        corr += 1
        streak += 1
    else:
        streak = 0
    if streak == 3:
        break

t = int(time() - starttime)
print(f"time:\t{t//60} mins {t%60} seconds")
avg = t // count
print(f"avg:\t{avg//60} mins {avg%60} seconds")

with open("/home/pi/Documents/Scripts/logs/dd.log", "a") as f:
    f.write(f"\n{dt.now()}: {avg} sec, {corr}/{count}")
