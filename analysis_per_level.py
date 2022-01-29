from math import floor
import numpy as np

import pandas as pd
from matplotlib import pyplot as plt

COLORS = ["#2d2d2d", "#ed7d31", "#EEEEEE", "#AAAAAA", "#666666"]

plt.rcParams.update({'figure.facecolor': COLORS[0],
                     'figure.figsize': (12, 8),
                     'figure.titlesize': 24,
                     'text.color': COLORS[1],
                     'axes.facecolor': COLORS[0],
                     'axes.edgecolor': COLORS[1],
                     'axes.labelcolor': COLORS[1],
                     'legend.fontsize': 18,
                     'xtick.color': COLORS[1],
                     'xtick.labelcolor': COLORS[1],
                     'xtick.labelsize': 18,
                     'ytick.color': COLORS[1],
                     'ytick.labelcolor': COLORS[1],
                     'ytick.labelsize': 18,
                     })


def quests_per_level(data: pd.DataFrame, data_important):
    data = data[["Lvl", "Exp"]]
    print(data_important.columns)
    data_important = data_important[["Lvl", "Nazwa"]]
    data["Lvl"] = data["Lvl"].map(lambda x: 10 * floor(x / 10) + 5)
    data_important["Lvl"] = data_important["Lvl"].map(lambda x: 10 * floor(x / 10) + 5)
    data = data.groupby("Lvl")
    data_important = data_important.groupby("Lvl")
    plt.bar(data.count().index, data.count()["Exp"], width=8, edgecolor=COLORS[1], color=COLORS[3], label="All")
    plt.bar(data_important.count().index, data_important.count()["Nazwa"], width=8, edgecolor=COLORS[1],
            color=COLORS[2], label="Important")
    plt.xlabel("Level", fontsize=18)
    plt.ylabel("# Quests", fontsize=18)
    plt.title("Number of quests", fontsize=24)
    plt.legend(fontsize=14)
    plt.savefig("Num_per_level.png")
    plt.show()


def experience_per_quest_per_level(data: pd.DataFrame):
    data = data[["Lvl", "Exp"]]
    data["Lvl"] = data["Lvl"].map(lambda x: 10 * floor(x / 10) + 5)
    data = data[data["Exp"] > 0]
    data = data[data["Lvl"] > 5]
    data = data.groupby("Lvl")
    plt.plot(data.max(), label="Maximum", color=COLORS[2])
    plt.plot(data.mean(), label="Average", color=COLORS[1])
    plt.plot(data.min(), label="Minimum", color=COLORS[2])
    plt.yscale("log")
    plt.xlabel("Level", fontsize=18)
    plt.ylabel("Experience", fontsize=18)
    plt.title("Experience per quest per level", fontsize=24)
    plt.legend(fontsize=14)
    plt.savefig("Exp_per_quest_per_level.png")
    plt.show()


def experience_per_level(data: pd.DataFrame):
    data = data[["Lvl", "Exp"]]
    data["Lvl"] = data["Lvl"].map(lambda x: 10 * floor(x / 10) + 5)
    data = data[data["Exp"] > 0]
    data = data[data["Lvl"] > 5]
    data_imp = data[data.index == "*"]
    data = data.groupby("Lvl")
    data_imp = data_imp.groupby("Lvl")
    plt.plot(data.sum()["Exp"], label="All", color=COLORS[2])
    plt.plot(data_imp.sum()["Exp"], label="Important", color=COLORS[1])
    lvls = np.array(data.sum().index)
    required = np.array(list(map(lambda x: obliczexp(x + 5, x - 5), np.array(data.sum().index))))
    plt.plot(lvls, required, "--", label="Required", color=COLORS[3])
    plt.yscale("log")
    plt.xlabel("Level", fontsize=18)
    plt.ylabel("Experience", fontsize=18)
    plt.title("Experience per level", fontsize=24)
    plt.legend(fontsize=14)
    plt.savefig("Exp_per_level.png")
    plt.show()


def experience_percent_per_level(data: pd.DataFrame):
    data = data[["Lvl", "Exp"]]
    data["Lvl"] = data["Lvl"].map(lambda x: 10 * floor(x / 10) + 5)
    data = data[data["Exp"] > 0]
    data = data[data["Lvl"] > 5]
    data_imp = data[data.index == "*"]
    data = data.groupby("Lvl")
    data_imp = data_imp.groupby("Lvl")
    lvls = np.array(data.sum().index)
    required = np.array(list(map(lambda x: obliczexp(x + 5, x - 5), np.array(data.sum().index))))
    plt.plot(lvls, 100 * np.array(data.sum()["Exp"]) / required, label="All", color=COLORS[2])
    plt.plot(lvls, 100 * np.array(data_imp.sum()["Exp"]) / required, label="Important", color=COLORS[1])
    plt.plot([lvls[0], lvls[-1]], [100, 100], '--', label="100%", color=COLORS[3])
    plt.xlabel("Level", fontsize=18)
    plt.ylabel("Part of required experience [%]", fontsize=18)
    plt.title("Part of required experience per level", fontsize=24)
    plt.legend(fontsize=14)
    plt.savefig("Exp_percent_per_level.png")
    plt.show()


def gold_per_quest_per_level(data: pd.DataFrame):
    data = data[["Lvl", "Gold"]]
    data["Lvl"] = data["Lvl"].map(lambda x: 10 * floor(x / 10) + 5)
    data = data[data["Gold"] > 0]
    data = data[data["Lvl"] > 5]
    data = data.groupby("Lvl")
    plt.plot(data.max(), label="Maximum", color=COLORS[2])
    plt.plot(data.mean(), label="Average", color=COLORS[1])
    plt.plot(data.min(), label="Minimum", color=COLORS[2])
    plt.yscale("log")
    plt.xlabel("Level", fontsize=18)
    plt.ylabel("Gold", fontsize=18)
    plt.title("Gold per quest per level", fontsize=24)
    plt.legend(fontsize=14)
    plt.savefig("Gold_per_quest_per_level.png")
    plt.show()


def rarity_items_per_level(data):
    data = data[["Lvl", "Zbroje (*)"]]
    data["Lvl"] = data["Lvl"].map(lambda x: 10 * floor(x / 10) + 5)
    data = data[data["Lvl"] > 5]
    data = data.dropna()

    def count_data(text, to_find):
        if text == "nan":
            return 0
        else:
            return text.count(to_find)

    data = data.groupby("Lvl").sum()
    levels = np.array(data.index)
    data["uni"] = data["Zbroje (*)"].map(lambda x: count_data(x, "*uni*"))
    data["hero"] = data["Zbroje (*)"].map(lambda x: count_data(x, "**hero**"))
    data["lega"] = data["Zbroje (*)"].map(lambda x: count_data(x, "***lega***"))
    plt.bar(levels - 3, data["uni"], width=3, edgecolor=COLORS[1], color=COLORS[3], label="Unique")
    plt.bar(levels, data["hero"], width=3, edgecolor=COLORS[1], color=COLORS[2], label="Heroic")
    plt.bar(levels + 3, data["lega"], width=3, edgecolor=COLORS[1], color=COLORS[1], label="Legendary")
    plt.xlabel("Level", fontsize=18)
    plt.ylabel("Count of rare equipment", fontsize=18)
    plt.title("Rare equipment per level", fontsize=24)
    plt.legend(fontsize=14)
    plt.savefig("Equipment_per_level.png")
    plt.show()


def obliczexp(l, a):
    l -= 1
    a -= 1
    c = l ** 4
    o = a ** 4
    r = c - o
    return r
