def extract_from_name(text):
    if len(text.strip()) > 3:
        if text[0].isdigit():
            text = ".".join(text.split('.')[1:]).strip()
        text = text.split('(')
        title = text[0].strip()

        try:
            lvl = text[1].split("lvl")[0]
        except:
            try:
                lvl = text[1].split(" lvl")[0]
            except:
                lvl = "0"
        if ")" in lvl:
            lvl = lvl.split(")")[0]

        try:
            city = text[1].split(") - ")[1]
        except:
            try:
                city = text[1].split(") – ")[1]
            except:
                try:
                    city = text[1].split(")")[1].strip()
                except:
                    city = "??"
        if city.startswith("lvl – "):
            city = city[6:]
        elif city.startswith("/ Chantli - "):
            city = city[12:]
            title += "/ Chantli"
        elif city.startswith("- "):
            city = city[2:]
        if "+" in city:
            city = city.split("+")[0].strip()
        return lvl, city, title

def number_before(text, search_text):
    text = text.replace(" mln", "m").replace("mln", "m").replace("mm","m").replace(" m","m")

    cut_idx = text.find(search_text)
        
    if cut_idx < 0:
        return "0", text

    val = "0"
    i = 1
    while val.replace(",",".").replace(".","").isdigit():
        if cut_idx-i < 0:
            return val.lstrip("."), text[cut_idx+len(search_text):]

        val = text[cut_idx-i:cut_idx]

        if val in ["k", "m"]:
            mnoznik = {
                "k": 1000, "m": 1000000
            }[val]
            val, text = number_before(text, val + search_text)
            if val == "0":
                return val.lstrip("."), text
            else:
                val = str(float(val.replace(",",".")) * mnoznik).split(".")[0]
                return val.lstrip("."), text

        i += 1
    if not val == "0":
        rest1 = text[:cut_idx-i+2]
        rest2 = text[cut_idx+len(search_text):]
        return val[1:].lstrip("."), rest1 + rest2
    
    return val, text

def number_after(text, search_text):
    text = text.replace(" mln", "m").replace("mln", "m").replace("mm","m").replace(" m","m")

    cut_idx = text.find(search_text)
        
    if cut_idx < 0:
        return "0", text
    else:
        cut_idx += len(search_text)

    val = "0"
    i = 1
    while val.replace(",",".").replace(".","").isdigit():
        if cut_idx+i > len(text):
            return val, text[:cut_idx+len(search_text)]

        val = text[cut_idx:cut_idx+i]

        if val[-1] in ["k", "m"]:
            mnoznik = {
                "k": 1000, "m": 1000000
            }[val[-1]]
            val = val[:-1]
            val = str(float(val.replace(",",".")) * mnoznik).split(".")[0]
            return val, text

        i += 1

    if not val == "0":
        return val[:-1], text
    
    return val, text
    

def find_next_word(text, search_text):
    val_idx = text.find(search_text)
    if val_idx >= 0:
        val = text.split(search_text)[1].split(" ")
        text = text.split(search_text)[0] + val[1]
        val = val[0]
    else:
        val = None
    return val, text

def get_indexes_of(text, search_text):
    n = text.count(search_text)
    idx = -1
    idxs = []
    for i in range(n):
        idx = text.find(search_text, idx+len(search_text))
        idxs.append(idx)
    return idxs