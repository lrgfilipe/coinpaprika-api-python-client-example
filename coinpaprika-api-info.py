from coinpaprika import client as Coinpaprika
from termcolor import colored
import time
import os

client = Coinpaprika.Client()


FAVORITES = ["BTC", "XRP"]


def get_col (x, n = 10, color = "white", bgcolor = ""):
    if bgcolor:
        return colored(str(x).ljust(n), color, bgcolor)
    else:
        return colored(str(x).ljust(n), color)

def get_col_with_color (x, n = 10, s = "%"):
    return colored(str(s + " " + str(x)).ljust(n), "red" if x < 0 else "green")

def get_vals (coin):
    today_ticker = client.today(coin["id"])[0]
    ticker = client.ticker(coin["id"])
    return {
        "symbol": coin["symbol"],
        "today": {
            "val": round(today_ticker["close"],3),
            "dif": round(today_ticker["close"] - today_ticker["open"],3),
            "pct": round(100 - today_ticker["open"] * 100 / today_ticker["close"],2)
        },
        "days7": { "pct": ticker["quotes"]["USD"]["percent_change_7d"] },
        "days30": { "pct": ticker["quotes"]["USD"]["percent_change_30d"] }
    }

def print_time():
    print("# " + time.strftime('%X'))

def print_header (title):
    print("# ---------------------------------------------------------------------------")
    print("# " + get_col(title, 10, "yellow"), get_col("USD", 9), get_col("TODAY", 24), get_col("7 DAYS", 10), get_col("30 DAYS ", 10),  sep=' | ')
    print("# ---------------------------------------------------------------------------")

def print_line(x):
    print("# " +
        get_col(x["symbol"]),
        get_col(x["today"]["val"], 9),
        get_col_with_color(x["today"]["dif"], 13, "USD"),
        get_col_with_color(x["today"]["pct"], 8),
        get_col_with_color(x["days7"]["pct"], 10),
        get_col_with_color(x["days30"]["pct"], 7),
        sep=' | ')

try:
    while True:
        xs = client.coins()
        os.system('cls' if os.name == 'nt' else 'clear')
        print("# ---------------------------------------------------------------------------")
        print_time()
        print_header("FAVORITES")     
        for item in [get_vals(x) for x in xs if x["symbol"] in FAVORITES]:
            print_line(item)
        print_header("TOP 10")
        for item in [get_vals(x) for x in xs[:10]]:
            print_line(item)
        print("# ---------------------------------------------------------------------------")
        time.sleep(30) # new data every 30 sec
except KeyboardInterrupt:
    pass


