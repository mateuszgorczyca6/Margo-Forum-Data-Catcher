from download import *
import pandas as pd

if __name__ == '__main__':
    links = pd.read_csv("links.csv")
    print("Aktualnie trwa praca nad aktualizowaniem:")
    
    for i in range(len(links)):
        name, URL = links.iloc[i]
        print(f"{name}")
        soup = connect(URL)
        get_all_quests_with_rewards(soup)

    
### to add:
#   # smocze questy
#   # divide items to groups
#   # search for dependencies