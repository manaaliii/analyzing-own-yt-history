from bs4 import BeautifulSoup
import csv
from numpy import NaN
import re

file_path = "watch-history.html"
with open(file_path, "r", encoding="utf-8") as file:
    html_code = file.read()

soup = BeautifulSoup(html_code, 'html.parser')

divs1 = soup.find_all('div', class_='content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1')
divs2 = soup.find_all('div', class_='content-cell mdl-cell mdl-cell--12-col mdl-typography--caption')
data = []


def fetchData(var):
    res = []
    for a in var:
        res.append(a.text)
        res.append(a['href'])
    return res


date_pattern = r'\d{1,2} [A-Za-z]{3} \d{4}, \d{2}:\d{2}:\d{2} [A-Za-z]{3}'
date_text = ''

for i in range(len(divs1)):
    date_text = divs1[i].get_text(strip=True).split('\n')[-1]
    a_tags = divs1[i].find_all('a')
    text = divs1[i].get_text(strip=True).split('\n')[-1]
    date_match = re.search(date_pattern, text)
    if date_match:
        date_text = date_match.group()
    isAd = divs2[i].find('b', string='Details:') is not None
    try:
        if isAd:
            for a in a_tags:
                data.append((a.text, a['href'], NaN, NaN, isAd, date_text))
        else:
            link_vid, link_vid_url, creator, creator_url = fetchData(a_tags)
            data.append((link_vid, link_vid_url, creator, creator_url, isAd, date_text))
    except ValueError:
        continue
    except AttributeError:
        # print(a_tags)
        temp = []
        for i in a_tags:
            temp.append(i)
        temp.append(NaN)
        temp.append(NaN)
        temp.append(True)
        temp.append(date_text)
        data.append(temp)

# print(data)
csv_file = 'trail1.csv'

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Video Title', 'Video URL', 'Youtube Creator', 'YT Creator URL', 'Is Ad', 'Time'])  # Write header
    writer.writerows(data)  # Write the data rows

print(f'Data has been successfully stored in {csv_file}.')
