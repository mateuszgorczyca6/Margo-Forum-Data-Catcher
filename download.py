import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from text_edit import extract_from_name

def connect(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        print(f" >>> !!! ERROR: result: {r.status_code} !!! <<< ")
    soup = bs(r.text, parser = "html.parser", features="lxml")
    return soup

def get_all_quests_with_rewards(soup):
    banned_td_headers = [
        "Jak szukać potrzebnego questa skutecznie?",
        "Spis treści",
        "Spis questów według poziomów",
        "Questy dzienne",
        "Hero Questy [dla każdej profesji] (60 lvl) – 5/6 questów - w różnych lokacjach",
        "Questy klanowe",
        "~~Spis solucji filmowych byKfighter~~(ok 80 opisów Questów)"
    ]
    banned_names = [
        "Po wykonaniu Serii zadań początkowych u Grambera możemy kontynuować dalej drogę bohatera.",
        "UWAGA!:"
    ]
    exceptions_names = {
        "Karka-han --- 22.Pomóż Tyweltowi rozwiązać jego problem 76 lvl)": [
            "76", "Pomóż Tyweltowi rozwiązać jego problem"
        ],
        "Kwieciste Przejście --- 1.": [
            "135", "Pomóż Tunii w zdobyciu goblińskich przedmiotów"
        ],
        "Kwieciste Przejście --- 2.": [
            "140", "Tygrys Tunii zgubił zaczarowaną obrożę"
        ],
        "Orcza Wyżyna --- 1.": [
            "141", "Goblińskie kopalnie stoją na skraju upadku"
        ],
        "Mirvenis-Adur --- 7. ": [
            "160", "Kowal Jaki chce stworzyć niezwykłą tarczę"
        ]
    }
    broken_city_names = [
        "Smocze Góry", 
        "Ruiny Tass Zhil", 
        "Wioska Pszczelarzy",
        "Ostoja Marzeń",
        "Nithal",
        "Przedmieścia Karka-han",
        "Nekropolia Karka-han"
    ]
    smocze_questy = [
        ["100", "Łapówka dla smoka umożliwiająca wykonywanie questów z nim"],
        ["100", "Pomóż smokowi obliczyć wartość jego skarbów na ludzki sposób"],
        ["102", "Odnajdź ukochaną zaklętego boga"],
        ["104", "Sprawdź dar, jaki smok otrzymał od pewnego kupca"],
        ["106", "Smok jest głodny i zjadłby coś nowego"],
        ["108", "Smokowi Introprodarowi odpada łuska z pancerza"],
    ]

    quests = pd.DataFrame(columns=[
        "Lvl", "Miejsce", "Nazwa"
    ])
    i = 0
    for td in soup.find_all("td", {"class": "pcont", }):
        # checking if header exists and abandon some
        td_inside = td.find("blockquote")
        if td_inside is None:
            continue

        if td_inside.find("blockquote") is None:
            quest_block = True
        else:
            quest_block = False

        td_header = td_inside.find("span")
        if td_header is None:
            continue
        td_header = td_header.text.strip()

        if not td_header in banned_td_headers:
            if quest_block:
                blockquotes = td.find_all("blockquote", recursive=False)
            else:
                blockquotes = td_inside.find_all("blockquote", recursive=False)
            for blockquote in blockquotes:
                if "======" in blockquote.text:
                    city = blockquote.find("b").text.strip()
                    if city.endswith("i okolice"):
                        city = city[:-9]
                else:
                    bs = blockquote.find_all("b")

                    quest_name = bs[0].text
                    if city + " --- " + quest_name in exceptions_names.keys():
                        lvl, title = exceptions_names[city + " --- " + quest_name]
                    else:
                        lvl, _, title = extract_from_name(quest_name)
                    
                    if title in broken_city_names:
                        city = title
                        continue

                    if not title in banned_names:
                        quests.loc[i] = [lvl, city, title]
                        i += 1

    city = "Smocze Góry"
    for quest in smocze_questy:
        lvl, title = quest
        quests.loc[i] = [lvl, city, title]
        i += 1

    print(quests)
    quests.to_excel("test.xlsx", "All Q", index=False)