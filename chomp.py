import json
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://www.chompveganeatery.com/meal-prep-service"

html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")

months = ['jan ', 'feb ', 'marc ', 'apr ', 'may ', 'june ', 'july ', 'aug ', 'sept ', 'oct ', 'nov ', 'dec ']


def get_entries(menu_data, start_printing):
    all_entries = []
    if type(menu_data) is dict:
        for (key, value) in menu_data.items():
            entry, new_start_printing = get_entries(value, start_printing)
            if not start_printing and new_start_printing:
                start_printing = new_start_printing
            if len(entry) > 0:
                all_entries.extend(entry)
        return all_entries, start_printing
    elif type(menu_data) is list:
        for index, entry in enumerate(menu_data):
            entry, new_start_printing = get_entries(entry, start_printing)
            if not start_printing and new_start_printing:
                start_printing = new_start_printing
            if len(entry) > 0:
                all_entries.extend(entry)
        return all_entries, start_printing
    elif type(menu_data) is bool or type(menu_data) is int or menu_data is None:
        return [], start_printing

    for month in months:
        if month in menu_data.lower():
            start_printing = True
            break
    if start_printing:
        return menu_data, start_printing
    else:
        return [], start_printing


# f = open("/home/jace/siteData")
# json_file = json.load(f)
for script in soup(["script"]):
    if "BOOTSTRAP_STATE_" in script.next:
        # print("".join(get_entries(json_file, False)[0]))
        print(
            "".join(
                get_entries(
                    json.loads(script.contents[0].strip().replace("window.__BOOTSTRAP_STATE__ = ", "")[:-1]),
                    False
                )[0]
            )
        )
