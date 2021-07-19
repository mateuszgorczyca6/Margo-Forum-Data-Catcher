import pandas as pd
import requests
from bs4 import BeautifulSoup as BS
from text_edit import *



def connect(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        print(f" >>> !!! ERROR: result: {r.status_code} !!! <<< ")
    soup = BS(r.text, parser = "html.parser", features="lxml")
    return soup

def get_all_quests_with_rewards(soup, writer, settings):
    old_Q = pd.read_excel("test.xlsx", "Q")
    old_Q_byquest = old_Q.set_index("Nazwa")

    banned_td_headers = [
        "Jak szukać potrzebnego questa skutecznie?",
        "Spis treści",
        "Spis questów według poziomów",
        "Questy dzienne",
        # "Hero Questy [dla każdej profesji] (60 lvl) – 5/6 questów - w różnych lokacjach",
        "Questy klanowe",
        "~~Spis solucji filmowych byKfighter~~(ok 80 opisów Questów)"
    ]
    hero_quests_td_header = "Hero Questy [dla każdej profesji] (60 lvl) – 5/6 questów - w różnych lokacjach"
    
    td_header_before_dragon_quest = "Mythar i okolice"

    banned_names = [
        "Po wykonaniu Serii zadań początkowych u Grambera możemy kontynuować dalej drogę bohatera.",
        "UWAGA!:"
    ]
    exceptions_names = {
        "Karka-han --- 22.Pomóż Tyweltowi rozwiązać jego problem 76 lvl)": [
            "76", "Pomóż Tyweltowi rozwiązać jego problem"
        ],
        "Smocze Góry --- Smocze zadania są możliwe do wykonania w kolejności wg poziomów.": [
            "100", "Łapówka dla smoka umożliwiająca wykonywanie questów z nim"
        ]
    }
    broken_city_names = [
        "Smocze Góry", 
        "Ruiny Tass Zhil", 
        "Wioska Pszczelarzy",
        "Ostoja Marzeń",
        "Nithal",
        "Przedmieścia Karka-han",
        "Nekropolia Karka-han",
        "Hero Questy [dla każdej profesji] (60 lvl) – 5/6 questów - w różnych lokacjach"
    ]
    armor_types = [
        "Jednoręczne", "Dwuręczne", "Półtoraręczne", "Dystansowe", "Pomocnicze", 
        "Różdżki", "Laski", "Zbroje", "Hełmy", "Buty", "Rękawice", "Pierścienie",
        "Naszyjniki", "Tarcze", "Strzały"
    ]
    type_codes = {
        "1": "Jednoręczne",
        "2": "Dwuręczne",
        "3": "Półtoraręczne",
        "4": "Dystansowe",
        "5": "Pomocnicze",
        "6": "Różdżki",
        "7": "Laski",
        "8": "Zbroje",
        "9": "Hełmy",
        "10": "Buty",
        "11": "Rękawice",
        "12": "Pierścienie",
        "13": "Naszyjniki",
        "14": "Tarcze",
        "15": "Neutralne",
        "16": "Konsumpcyjne",
        "17": "Złoto",
        "18": "Klucze",
        "19": "Questowe",
        "20": "???",
        "21": "Strzały",
        "22": "Talizmany",
        "23": "Książki",
        "24": "Torby",
        "25": "Błogosławieństwa",
        "26": "Ulepszenia",
    }


    quests = pd.DataFrame(columns=[
        "*", "Lvl", "Miejsce", "Nazwa", "Exp", "Gold", "PH", "Denary", "TP", "Sklep",
        "Zbroje (*)", "Błoga", "Teleporty", "Klucze", "Talizmany", "Torby", "Other Items"
    ])

    interesting_quests = pd.DataFrame(columns=[
        "Lvl", "Miejsce", "Miejsce (*)", "Nazwa", "Czemu warto?", "Pozostałe benefity"
    ])

    i = 0
    i_interest = 0
    for td in soup.find_all("td", {"class": "pcont", }):
        # checking if header exists and if it contains quest or is quest container
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
            # hero questy
            heroQ = False
            if td_header == hero_quests_td_header:
                td_inside = td.find_all("blockquote")[1]
                heroQ = True
            
            # Smocze Questy
            dragonQ = False
            if td_header == td_header_before_dragon_quest:
                td_inside = td.find_all("blockquote",recursive=False)
                dragonQ = True

            if dragonQ:
                blockquotes = td_inside[0].find_all("blockquote")
                blockquotes.extend(td_inside[1].find_all("blockquote"))
            elif quest_block and not heroQ:
                blockquotes = td.find_all("blockquote", recursive=False)
            else:
                blockquotes = td_inside.find_all("blockquote", recursive=False)

            for blockquote in blockquotes:
                if "ZADANIE WSTRZYMANE" in blockquote.text:
                    continue

                # reading city from special blockquote
                if "======" in blockquote.text:
                    city = blockquote.find("b").text.strip()
                    if city.endswith("i okolice"):
                        city = city[:-9]
                else:
                    # hero questy
                    if heroQ:
                        if not blockquote.text.strip()[:5] == "Quest": continue
                        lvl = 60
                        title = td_inside.find("b").text + " - " + blockquote.find("b").text
                        city = "Hero Quest"

                    else:
                        bs = blockquote.find_all("b")
                        
                        # reading lvl and title from blockquote
                        quest_name = bs[0].text
                        if len(quest_name) < 5:
                            quest_name = bs[0].text + blockquote.find("u").text + bs[1].text
                        if city + " --- " + quest_name in exceptions_names.keys():
                            lvl, title = exceptions_names[city + " --- " + quest_name]
                        else:
                            lvl, _, title = extract_from_name(quest_name)
                        
                        if title in broken_city_names:
                            city = title
                            continue
                        
                        if lvl.startswith("od "):
                            lvl = lvl[3:]
                        lvl = lvl.split("-")[0]
                        lvl = int(lvl)

                    # reading nagród za questy
                    nagroda_strings = [
                        "NAGRODA:", "Nagroda:", "NAGRODA", "Nagroda", "nagrodę:", "kończymy questa",
                        "Otrzymano ", "otrzymujemy:", "Otrzymujemy "
                    ]
                    nagroda_idx = -1
                    j = 0
                    while nagroda_idx < 0:
                        nagroda_idx = blockquote.text.find(nagroda_strings[j])
                        j += 1
                        if j == len(nagroda_strings):
                            break
                    if nagroda_idx < 0:
                        nagroda_idx = 100
                    nagroda = blockquote.text[nagroda_idx + 8:].strip().replace("Otrzymano ", "")
                    nagroda = nagroda.split("punktowa")[0]

                    # exp
                    exp, _ = number_before(nagroda, " punktów doświadczenia")
                    if exp == "0":
                        exp, _ = number_before(nagroda, " expa")
                    if exp == "0":
                        exp, _ = number_after(nagroda, "Exp:")
                    if exp == "0":
                        exp, _ = number_before(nagroda, "punktów doświadczenia")
                    if exp == "0":
                        exp, _ = number_before(nagroda, " doświadczenia")
                    if exp == "0":
                        exp, _ = number_after(nagroda, "Exp na świecie publicznym (bez bonusów klanowych): ")
                    if exp == "0":
                        exp, _ = number_before(nagroda, " exp")
                    exp = int(exp)

                    # gold
                    gold, _ = number_before(nagroda, " sztuk złotychmonet")
                    if gold == "0":
                        gold, _ = number_before(nagroda, " złotychmonet")
                    if gold == "0":
                        if not "przeklętych monet" in nagroda:
                            gold, _ = number_before(nagroda, "monet")
                    if gold == "0":
                        if not "sztabkę złota" in nagroda:
                            gold, _ = number_before(nagroda, " złota")
                    if gold == "0":
                        gold, _ = number_after(nagroda, "Złoto:")

                    gold = int(gold)

                    # PH
                    PH, _ = number_before(nagroda, " punktów honoru")
                    if PH == "0":
                        PH, _ = number_before(nagroda, " PH")
                    if PH == "0":
                        PH, _ = number_before(nagroda, " ph")
                    if PH == "0":
                        PH, _ = number_before(nagroda, "ph")
                    if PH == "0":
                        PH, _ = number_after(nagroda, "PH: ")
                    if PH == "0":
                        PH, _ = number_after(nagroda, "PH:")
                    PH = int(PH)

                    # TP
                    TP, _ = find_next_word(quest_name, "teleportację do ")
                    if TP == None:
                        TP, _ = find_next_word(quest_name, "Aktywuj portal w ")
                    if TP == None:
                        TP, _ = find_next_word(quest_name, "Teleport do ")
                    if title == "Rzeki spłyną krwią.":
                        TP = "Thuzal"
                    
                    # sklep
                    sklep, _ = find_next_word(nagroda, "dostęp do sklepu ")
                    if sklep == None:
                        sklep, _ = find_next_word(nagroda, "odblokowania sklepu ")
                    if sklep == None:
                        sklep, _ = find_next_word(nagroda, "dostęp do ")

                    # denary
                    if "Denary (" in nagroda:
                        denary = nagroda.split("Denary (")[1].split("x")[0].split(")")[0].split(" sztu")[0]
                    elif " x denar" in nagroda:
                        denary, _ = number_before(nagroda, " x denar")
                    elif "denar" in nagroda:
                        denary = "1"
                    elif " denary" in nagroda:
                        denary, _ = number_before(nagroda, " denary")
                    else:
                        denary = "0"
                    denary = int(denary)

                    nagroda_txt = nagroda[:]

                    # nagroda_idx = str(blockquote).find("NAGRODA")
                    nagroda_idx = -1
                    j = 0
                    while nagroda_idx < 0:
                        nagroda_idx = str(blockquote).find(nagroda_strings[j])
                        j += 1
                        if j == len(nagroda_strings):
                            break
                    if nagroda_idx < 0:
                        nagroda_idx = 100

                    if heroQ:
                        nagroda_idx = 0

                    nagroda = BS(str(blockquote)[nagroda_idx:].split("punktowa")[0], "html.parser")


                    # itemy
                    items = nagroda.find_all("div", {"class": "itemborder"})
                    all_items = []
                    items_rare_armors = []
                    items_blogos = []
                    items_teleports = []
                    items_keys = []
                    items_talizmans = []
                    items_bags = []
                    items_other = []

                    for item in items:
                        stats = item.find("img")["stats"]
                        i_name = stats.split("|")[0].strip()
                        i_type_code = stats.split("||")[-2]
                        try:
                            i_type = type_codes[i_type_code]
                        except:
                            print(title, i_name, i_type_code)

                        # miksturki
                        if "fullheal" in stats:
                            i_HP = stats.split("fullheal=")[1].split("<")[0].split("|")[0].split(";")[0]
                            all_items.append(i_name + ": Mix(Full) [" + i_HP + "]")
                            items_other.append(i_name + ": Mix(Full) [" + i_HP + "]")

                        elif "leczy=" in stats:
                            i_HP = stats.split("leczy=")[1].split("<")[0].split("|")[0].split(";")[0]
                            if "amount" in stats:
                                i_amount = stats.split("amount=")[1].split("<")[0].split("|")[0].split(";")[0]
                                all_items.append(i_amount + " x " + i_name + ": Mix [" + str(int(i_amount) * int(i_HP)) + "]")
                                items_other.append(i_amount + " x " + i_name + ": Mix [" + str(int(i_amount) * int(i_HP)) + "]")
                            else:
                                all_items.append(i_name + ": Mix [" + i_HP + "]")
                                items_other.append(i_name + ": Mix [" + i_HP + "]")
                        
                        elif "perheal" in stats:
                            i_HP = stats.split("perheal=")[1].split("<")[0].split("|")[0].split(";")[0]
                            if "amount" in stats:
                                i_amount = stats.split("amount=")[1].split("<")[0].split("|")[0].split(";")[0]
                                all_items.append(i_amount + " x " + i_name + ": Mix [" + i_HP + "%]")
                                items_other.append(i_amount + " x " + i_name + ": Mix [" + i_HP + "%]")
                            else:
                                all_items.append(i_name + ": Mix [" + i_HP + "%]")
                                items_other.append(i_name + ": Mix [" + i_HP + "%]")

                        # armor i błogo
                        elif i_type in [*armor_types, "Błogosławieństwa"]:
                            if "unique" in stats:
                                i_rarity = " *uni*"
                            elif "heroic" in stats:
                                i_rarity = " **hero**"
                            elif "legendary" in stats:
                                i_rarity = " ***lega***"
                            else:
                                i_rarity = ""
                            if "reqp=" in stats:
                                i_prof = stats.split("reqp=")[1].split("<")[0].split("|")[0].split(";")[0].strip()
                            else:
                                i_prof = "wpbmht"
                            if i_type == "Błogosławieństwa":
                                i_type = "Błogo"
                            if i_type == "Strzały":
                                i_amount = stats.split("ammo=")[1].split("<")[0].split("|")[0].split(";")[0]
                                all_items.append(i_amount + " x " + i_name + ": " + i_type + i_rarity + " [" + i_prof + "]")
                                items_other.append(i_amount + " x " + i_name + ": " + i_type + i_rarity + " [" + i_prof + "]")
                            elif i_type == "Błogo":
                                if "amount" in stats:
                                    i_amount = stats.split("amount=")[1].split("<")[0].split("|")[0].split(";")[0]
                                else:
                                    i_amount = "1"
                                all_items.append(i_amount + " x " + i_name + ": " + i_type + i_rarity + " [" + i_prof + "]")
                                items_blogos.append(i_amount + " x " + i_name + ": " + i_type + i_rarity + " [" + i_prof + "]")
                            else:
                                all_items.append(i_name + ": " + i_type + i_rarity + " [" + i_prof + "]")
                                if not i_rarity == "":
                                    items_rare_armors.append(i_name + ": " + i_type + i_rarity + " [" + i_prof + "]")
                                else:
                                    items_other.append(i_name + ": " + i_type + i_rarity + " [" + i_prof + "]")

                        # teleport
                        elif "teleport=" in stats:
                            i_tp = stats.split("opis=")[1].split("<")[0].split("|")[0].split(";")[0].strip()
                            if "amount" in stats:
                                i_amount = stats.split("amount=")[1].split("<")[0].split("|")[0].split(";")[0]
                                if i_name in nagroda_txt:
                                    try:
                                        i_amount = nagroda_txt.split(i_name + " (")[1].split(" ")[0].split("x")[0]
                                    except:
                                        pass
                                all_items.append(i_amount + " x " + i_name + ": " + "TP [" + i_tp + "]")
                                items_teleports.append(i_amount + " x " + i_name + ": " + "TP [" + i_tp + "]")
                            else:
                                all_items.append(i_name + ": " + "TP [" + i_tp + "]")
                                items_teleports.append(i_name + ": " + "TP [" + i_tp + "]")
                        
                        # złoto
                        elif i_type == "Złoto":
                            i_gold = stats.split("gold=")[1].split("<")[0].split("|")[0].split(";")[0].strip()
                            all_items.append(i_name + ": " + "Gold [" + i_gold + "]")
                            gold += int(i_gold)

                        # klucze
                        elif i_type == "Klucze":
                            try:
                                i_place = stats.split("opis=")[1].split("<")[0].split("|")[0].split(";")[0].strip()
                            except:
                                i_place = i_name
                            all_items.append(i_name + ": " + "Klucz [" + i_place + "]")
                            items_keys.append(i_name + ": " + "Klucz [" + i_place + "]")

                        # talizmany
                        elif i_type == "Talizmany":
                            if "respred" in stats:
                                i_res = True
                                i_respred = stats.split("respred=")[1].split("<")[0].split("|")[0].split(";")[0].strip()
                            else:
                                i_res = False
                            if "afterheal" in stats:
                                i_he = True
                                i_heal = stats.split("afterheal=")[1].split("<")[0].split("|")[0].split(";")[0].strip()
                                i_heal = i_heal.split(",")
                                i_heal_chance = i_heal[0]
                                i_heal_amount = i_heal[1]
                            else:
                                i_he = False
                            text = i_name + ": " + "Talizman ["
                            if i_res:
                                text += "czas trupa -" + i_respred + "%"
                                if i_he:
                                    text += "; "
                            if i_he:
                                text += "leczy: " + i_heal_amount + ", szansa: " + i_heal_chance + "%"
                            text += "]"
                            all_items.append(text)
                            items_talizmans.append(text)

                        # torby
                        elif i_type == "Torby":
                            i_bag = stats.split("bag=")[1].split("<")[0].split("|")[0].split(";")[0].strip()
                            if "btype=18" in stats:
                                all_items.append(i_name + ": " + "Torba [" + i_bag + ", klucze]")
                                items_bags.append(i_name + ": " + "Torba [" + i_bag + ", klucze]")
                            else:
                                all_items.append(i_name + ": " + "Torba [" + i_bag + "]")
                                items_bags.append(i_name + ": " + "Torba [" + i_bag + "]")

                        # pozostałe
                        else:
                            all_items.append(i_name)
                            items_other.append(i_name)

                    # nieznane itemy
                    broken_items = get_indexes_of(nagroda_txt, "ITEM#")
                    for idx in broken_items:
                        txt = nagroda_txt[idx:]
                        all_items.append(txt.split(".")[0])
                        items_other.append(txt.split(".")[0])

                    interesting_items = [*items_rare_armors, *items_blogos, *items_teleports, *items_keys, *items_talizmans, *items_bags]
                    other_items = items_other[:]
                    
                    all_items = "; ".join(all_items)
                    items_rare_armors = "; ".join(items_rare_armors)
                    items_blogos = "; ".join(items_blogos)
                    items_teleports = "; ".join(items_teleports)
                    items_keys = "; ".join(items_keys)
                    items_talizmans = "; ".join(items_talizmans)
                    items_bags = "; ".join(items_bags)
                    items_other = "; ".join(items_other)

                    # god reward marker
                    interesting = False
                    if not all_items == items_other or denary > 0 or not TP is None or not sklep is None:
                        interesting = True
                    
                    if not title in banned_names:
                        quests.loc[i] = [{True: "*", False: ""}[interesting], lvl, city, title, exp, gold, PH, denary, TP, sklep,
                        items_rare_armors, items_blogos, items_teleports, items_keys, items_talizmans, items_bags, items_other]
                        i += 1
                        if interesting:
                            reward_good = []
                            if denary > 0:
                                reward_good.append("Denary: " + str(denary) + "; ")
                            if not sklep is None:
                                reward_good.append("Sklep: " + sklep + "; ")
                            if not TP is None:
                                reward_good.append("TP: " + TP + "; ")
                            reward_good.extend(interesting_items)
                            reward_good = "; ".join(reward_good)

                            reward_other = []
                            if exp > 0:
                                reward_other.append("Exp: " + str(exp) + " ")
                            if gold > 0:
                                reward_other.append("Gold: " + str(gold) + " ")
                            if PH > 0:
                                reward_other.append("PH: " + str(PH) + " ")
                            reward_other.extend(other_items)
                            reward_other = "; ".join(reward_other)
                            
                            interesting_quests.loc[i_interest] = [
                                lvl, city, old_Q_byquest["Miejsce (*)"][title], title, reward_good, reward_other
                            ]
                            i_interest += 1

    quests = quests.sort_values("Nazwa").sort_values("Miejsce").sort_values("Lvl")
    interesting_quests = interesting_quests.sort_values("Nazwa").sort_values("Miejsce").sort_values("Lvl")

    
    quests.to_excel(writer, "All Q", index=False)
    interesting_quests.to_excel(writer, "Q", index=False)
    print("--- ZAKOŃCZONO ---")