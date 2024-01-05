import json

import requests
from bs4 import BeautifulSoup

with open('rustlab.html', 'r', encoding='utf-8') as f:
    data = f.read()
    f.close()
soup = BeautifulSoup(data, 'html.parser')

skinsSelectorTabs = soup.find('div', id="skins-selector-tabs")
skinsSelectorTabsSpansList = [i['data-page'] for i in skinsSelectorTabs.find_all('span')][:-4]
print(skinsSelectorTabsSpansList)

skinsLinksDict = dict()
count = 0
for i in skinsSelectorTabsSpansList:
    skinsLinksDict[i] = {}
    for itemGroup in [j['title'] for j in soup.find('div', {'data-category': i}).find_all('span', class_='item-group')]:
        # print(itemGroup)
        itemGroupSkins = list()
        for skin in soup.find('div', id='wrappah').find_all('a', {'data-item': itemGroup}):
            # print(skin)
            itemGroupSkins.append({'name': skin['data-name'], 'href': skin['href'].replace('//', 'https://')})
            count += 1
        skinsLinksDict[i][itemGroup] = itemGroupSkins

with open('skinsLinksDict.json', 'w', encoding='utf-8') as f:
    json.dump(skinsLinksDict, f)
    f.close()


print(count)
print(skinsLinksDict)
