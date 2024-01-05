import json

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def get_item_id(url, ua) -> int:
    resp = requests.get(url, headers={'User-Agent': ua})
    print(url, resp.status_code)
    soup = BeautifulSoup(resp.text, 'html.parser')
    try:
        id = int(soup.find('table', class_='stats-table').find('a').text)
        return id
    except:
        return 0


with open('skinsLinksDictTest.json', 'r', encoding='utf-8') as f:
    skinsLinksDict = json.load(f)
    f.close()

resJson = list()

# for item in skinsLinksDict.values():
#     itemDict = {}
#     for key, value in item.items():
#         itemDict["Item Shortname"] = key
#         idList = list()
#         for i in value:
#             userAgent = UserAgent().random
#             idList.append(get_item_id(i['href'], userAgent))
#         itemDict["Skins"] = idList
#     resJson.append(itemDict)


for weapon, weapon_details in skinsLinksDict.items():
    for shortname, skins in weapon_details.items():
        userAgent = UserAgent().random
        skinsIdsWithZero = [get_item_id(skin["href"], userAgent) for skin in skins]
        while 0 in skinsIdsWithZero:
            skinsIdsWithZero.remove(0)
        itemDict = {
            "Item Shortname": shortname,
            "Permission": "",
            "Skins": skinsIdsWithZero
        }
        if len(itemDict['Skins']) > 0:
            resJson.append(itemDict)

resJson = {"Skins": resJson}

with open('resJsonTest.json', 'w', encoding='utf-8') as f:
    json.dump(resJson, f)
    f.close()
