from download import *
import pandas as pd

if __name__ == '__main__':
    links = pd.read_csv("links.csv")
    print("Aktualnie trwa praca nad aktualizowaniem:")
    
    for i in range(len(links)):
        print("Odczytywanie ustawień")
        writer = pd.ExcelWriter('test.xlsx')
        settings = pd.read_excel("test.xlsx", "Settings", index_col = 0, header = None, names = ["settings"])
        settings.to_excel(writer, "Settings", header=False)
        print("Zakończono")
        name, URL = links.iloc[i]
        print(f"{name}")
        soup = connect(URL)
        get_all_quests_with_rewards(soup, writer)
        writer.save()

    
### to add:
#   # important tasks selection settings
#   # search for dependencies
#   # changes tracker