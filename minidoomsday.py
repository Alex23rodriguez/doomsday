from datetime import datetime as dt, timedelta
from random import randint


def get_rand_date(config) -> dt:
    return config["start"] + timedelta(days=randint(0, config["total_days"]))


def equal(config, data: dt, inpt: str):
    return data.strftime("%w") == inpt or data.strftime("%a").lower() == inpt.lower()


def explain(config, date):
    cent = date.year // 100
    centd, year = [2, 0, 5, 3][(cent) % 4], date.year % 100
    a, b = year // 12, year % 12
    yearstr = f"{cent*100}: {centd}, {year-b}: {a%7}, {b}: {(b+b//4)%7}"
    ans = dt(2100, date.month, date.day).strftime(f"(%d %b: %w, {yearstr})")
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

    if equal(config, date, x):
        print("\tcorrect!")
        return True
    else:
        ans = explain(config, date) if config["explain"] else ""
        print("\twrong... " + date.strftime(f"%A {ans}"))
        return False


print("answer 3 in a row to access terminal")
streak = 0
while True:
    if oneround():
        streak += 1
    else:
        streak = 0
    if streak == 3:
        break
