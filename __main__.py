from download import *
from analysis_per_level import *

if __name__ == '__main__':
    links = pd.read_csv("links.csv")
    print("Aktualnie trwa praca nad aktualizowaniem:")

    for i in range(len(links)):
        # print("Odczytywanie ustawień")
        writer = pd.ExcelWriter('test.xlsx')
        # settings = pd.read_excel("test.xlsx", "Settings", index_col=0, header=None, names=["settings"], engine="xlrd")
        # settings.to_excel(writer, "Settings", header=False)
        # print("Zakończono")
        name, URL = links.iloc[i]
        print(f"{name}")
        soup = connect(URL)
        get_all_quests_with_rewards(soup, writer)
        writer.save()

    all_q = pd.read_excel("test.xlsx", "All Q", index_col=0)
    q = pd.read_excel("test.xlsx", "Q", index_col=-1)
    quests_per_level(all_q, q)
    experience_per_quest_per_level(all_q)
    experience_per_level(all_q)
    experience_percent_per_level(all_q)
    gold_per_quest_per_level(all_q)
    rarity_items_per_level(all_q)

### to add:
#   # important tasks selection settings
#   # search for dependencies
#   # changes tracker
