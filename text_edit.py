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
                lvl = "??"
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